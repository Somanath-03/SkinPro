import os
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
def api_call(image_path):
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    train_datagen = ImageDataGenerator(rescale=1./255,
                                    shear_range=0.2,
                                    zoom_range=0.2,
                                    horizontal_flip=True)

    training_set = train_datagen.flow_from_directory('C:/Users/Spsom/VscodeProjects/college/special_topics/dataset/training',
                                                    target_size=(64, 64),
                                                    batch_size=32,
                                                    class_mode='categorical')

    test_datagen = ImageDataGenerator(rescale=1./255)

    test_set = test_datagen.flow_from_directory('C:/Users/Spsom/VscodeProjects/college/special_topics/dataset/test',
                                                target_size=(64, 64),
                                                batch_size=32,
                                                class_mode='categorical')
    cl=training_set.class_indices
    print(cl)

    cnn = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=(64, 64, 3)),
        tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
        tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'),
        tf.keras.layers.MaxPool2D(pool_size=2, strides=2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=128, activation='relu'),
        tf.keras.layers.Dense(units=training_set.num_classes, activation='softmax')
    ])

    cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    cnn.fit(x=training_set, validation_data=test_set, epochs=30)
    cnn.save('./model_pred.h5')
    
    cnn = load_model('C:/Users/Spsom/VscodeProjects/college/special_topics/model_pred.h5')
    import numpy as np
    from keras.preprocessing import image
    test_image = image.load_img(image_path, target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = cnn.predict(test_image)
    class_indices = {'acne': 0, 'blackheads': 1, 'dark_spots': 2, 'dry_skin': 3, 'eye_bags': 4, 'normal_skin': 5, 'oily_skin': 6, 'pores': 7, 'skin_redness': 8}
    predicted_class = list(class_indices.keys())[np.argmax(result)]
    print("Predicted class:", predicted_class)
    print(predicted_class)
    return predicted_class


api_call("C:/Users/Spsom/VscodeProjects/college/special_topics/uploads/acne2943.jpg")