# 🧴 SkinPro - Facial Skin Disease Detection & Consultation Website

SkinPro is an intelligent, web-based dermatology assistant that uses deep learning (CNNs) to detect 9 facial skin conditions from uploaded images. The platform provides personalized treatment suggestions and dietary plans based on predictions, helping users manage skin health without the need for frequent dermatologist visits.

---

## 🌟 Features

- 🧠 **CNN-based Disease Detection**: Detects skin conditions like acne, dark spots, blackheads, etc.
- 🩺 **Personalized Treatment Suggestions**: Recommends medicine and skincare routines.
- 🥗 **Dietary Plan Recommendations**: Customized food plans for each condition.
- 📸 **Image Upload and Analysis**: Easy interface for uploading and getting results.
- 🧾 **User Authentication**: Register, login, and track diagnosis history.
- 🗃️ **MySQL Integration**: Stores user data, medical history, and disease information.

---

## 🔧 Tech Stack

| Layer | Technologies |
|-------|--------------|
| 💻 Frontend | HTML5, CSS3, JavaScript |
| 🧠 ML Model | Python, TensorFlow, Keras |
| 🌐 Backend | Flask |
| 🗄️ Database | MySQL |
| 📦 Libraries | NumPy, Pandas, OpenCV, Keras, TensorFlow |

---

## 🏥 Supported Skin Conditions

1. Acne  
2. Blackheads  
3. Dark Spots  
4. Dry Skin  
5. Eye Bags  
6. Normal Skin  
7. Oily Skin  
8. Pores  
9. Skin Redness  

---

## 📁 Project Structure

```bash
skinpro/
├── file_editor.py         # Processes and classifies training data images
├── main.py                # CNN model training and prediction script
├── server.py              # Flask application with API and routing
├── model_pred.h5          # Trained Keras model file
├── ACNE.docx              # Contains medical and dietary info for diseases
├── templates/             # HTML templates (login, results, etc.)
├── static/                # Static files (CSS, JS, images)
└── README.md              # Project documentation
````

---

## 🧪 Model Overview

CNN architecture used:

```text
Input: (64x64x3)
↓ Conv2D + ReLU
↓ MaxPooling2D
↓ Conv2D + ReLU
↓ MaxPooling2D
↓ Flatten
↓ Dense (128) + ReLU
↓ Dense (9) + Softmax
Output: Skin Condition
```

Model is trained using `ImageDataGenerator` for data augmentation and saved as `model_pred.h5`.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/skinpro.git
cd skinpro
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL

Create a MySQL database named `rdbms_proj` with tables:

* `users (id, username, password)`
* `history (id, values_list)`
* `diseases (name, disease_info, treatment, dietary_plan)`

You can use the content in `ACNE.docx` to populate the `diseases` table.

### 4. Run the Server

```bash
python server.py
```

Then open your browser and go to `http://127.0.0.1:5000/`.

---

## 📤 Upload Flow

1. Register/Login
2. Upload an image of your face
3. Backend predicts disease using `model_pred.h5`
4. Fetches treatment & dietary advice from DB
5. Stores and displays results and history

---

## 🧠 Training Workflow

To train your own model:

1. Organize your image dataset using `file_editor.py`
2. Use `main.py` to train and save the CNN model
3. The model will be saved as `model_pred.h5` and used by the Flask backend

---
## 🙋‍♀️ Authors & Contributors 

1.Venkata Somanath Meda
2.Samarth Shenoy
3.Shilpi Singh 

