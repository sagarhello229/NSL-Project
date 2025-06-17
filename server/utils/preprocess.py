import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# augmentation gareko
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    shear_range=0.15,
    zoom_range=0.15,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=False,
    fill_mode='nearest'
)

# test-time preprocessing
test_datagen = ImageDataGenerator(rescale=1./255)

def preprocess_image(image, target_size=(96, 96), for_training=False):
    image = cv2.resize(image, target_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.expand_dims(image, axis=0)  

    if for_training:
        image = next(train_datagen.flow(image, batch_size=1))
    else:
        image = image.astype("float32") / 255.0 

    return image  
