from flask import Flask, render_template,jsonify ,redirect, url_for, session, request
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from keras.models import load_model
from keras.preprocessing import image
import numpy as np


app = Flask(__name__)
app.secret_key = 'secretkey'  # Needed for session management
UPLOAD_FOLDER = 'C:/Users/Spsom/VscodeProjects/college/special_topics/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='rdbms_proj',
            user='root',
            password='2034'
        )
        """cursor = connection.cursor(dictionary=True)
        cursor.execute('''
                       create trigger newuser 
                        after insert on history 
                        for each row
                        begin
                        insert into cart values(new.id,'');
                        end;
                        ''')"""
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def api_call(image_path):
    # load the machine learning model
    cnn = load_model('C:/Users/Spsom/VscodeProjects/college/special_topics/model_pred.h5')
    test_image = image.load_img(image_path, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    # predictor predict the model and returns the predticted class 
    result = cnn.predict(test_image)
    class_indices = {'Acne': 0, 'Blackheads': 1, 'Dark Spots': 2, 'Dry Skin': 3, 'Eye Bags': 4, 
                     'Normal Skin': 5, 'Oily Skin': 6, 'Pores': 7, 'Redness': 8}
    predicted_class = list(class_indices.keys())[np.argmax(result)]
    print("Predicted class: ", predicted_class)
    # the predicted class is routed to another function for better code re-usability
    return predicted_class



# function to make sure only images are getting saved
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# function to retreive data for the analysis part and render webpage
@app.route('/getdata1', methods=['POST'])
def getdata1():
    # to check if user has logged in 
    username = session["username"]
    sql = "SELECT id FROM users where username=%s;"
    data = (username,)
    connection = get_db_connection()
    # to save the image recieved from the frontend
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
        # if all data is recieved 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print("file downloaded")

        # checks for connection with the database 
        # requests data to be rendered to frontend
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql,data)
            id=cursor.fetchone()
            # for updating the history of the patient
            sql = "UPDATE history SET values_list = CONCAT(values_list, %s) WHERE id = %s;"
            api_data = api_call(filepath)
            data = (str(api_data)+",", id['id'])  # Convert api_data to string for concatenation
            cursor.execute(sql, data)
            connection.commit()
            # to retrieve data for the disease analysed
            sql = f"select disease_info,treatment,dietary_plan from diseases where name = %s;"
            cursor.execute(sql,(api_data,))
            # returns in the form of an array 
            info = cursor.fetchone()
            return render_template("./page2/index.html",data1 = api_data,data=getpastdata(str(session['username'])),
                                   prob_info=info['disease_info'],treatment =info['treatment'],plan = info['dietary_plan']) 
    


# past-data = data
# function to get past data of the user
def getpastdata(username):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        sql = "SELECT id FROM users where username=%s;"
        data = (username,)
        cursor.execute(sql,data)
        id=cursor.fetchone()["id"]
        sql = "SELECT values_list FROM history WHERE id = %s;"
        data = (id,)
        cursor.execute(sql, data)
        data = cursor.fetchall()
        data = dict(data[0])
        # data is stored in the form of csv
        data = data["values_list"].split(",")
        if data == [""]:
            data=["No past data available"]
        return data

# main weboage routing function
@app.route("/")
def index():
    return render_template("./main/index.html")

# second webpage(analysis webpage) routing function
@app.route("/redirect_page_2")
def redirect_page_2():
    return render_template("./page2/index.html",data1 = "No available data, Please upload an image ",
                           data=getpastdata(str(session['username'])))

# login function and for checking if user is already registered or not
@app.route('/login', methods=['GET', 'POST'])
def login():
    login = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                session['username'] = username
                login = "login successfull"
                return redirect(url_for('redirect_page_2'))
            else:
                login = "Invalid credentials"
    return render_template('./login/login.html',login=login)

#register function to register user
@app.route('/register', methods=['GET', 'POST'])
def register():
    login = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s ", (username,))
            user = cursor.fetchone()
            if user:
                login =  'You are an exisiting user.'
            else:
                login =  'register Successfull'
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()
                session['username'] = username
                return redirect(url_for('redirect_page_2'))

    return render_template('./login/register.html',login = login)

# function to logout 
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

#function to start the run 
if __name__ == '__main__':
    app.run(debug=True)
