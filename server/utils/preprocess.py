import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Augmentation parameters for training
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

test_datagen = ImageDataGenerator(rescale=1./255)

def preprocess_image(image, target_size=(96, 96), for_training=False):
    """
    Resize, convert color, normalize and optionally augment image.
    
    Args:
        image (numpy.ndarray): Input image (BGR format from OpenCV)
        target_size (tuple): Desired size (width, height)
        for_training (bool): Whether to apply augmentation

    Returns:
        numpy.ndarray: Preprocessed image with shape (1, H, W, 3)
    """
    image = cv2.resize(image, target_size)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    if for_training:
        image = next(train_datagen.flow(image, batch_size=1, shuffle=False))

    return image
