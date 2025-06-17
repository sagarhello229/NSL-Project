import cv2
import numpy as np

def resize_image(image, size=(96, 96)):
    """
    Resize image to given size.
    """
    return cv2.resize(image, size)

def normalize_image(image):
    """
    Normalize pixel values to [0,1].
    """
    return image.astype(np.float32) / 255.0

def rotate_image(image, angle):
    """
    Rotate image by angle (degrees).
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    return rotated

def shear_image(image, shear_factor=0.15):
    """
    Shear image by shear_factor.
    """
    (h, w) = image.shape[:2]
    M = np.array([[1, shear_factor, 0],
                  [0, 1, 0]], dtype=np.float32)
    sheared = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    return sheared

def zoom_image(image, zoom_factor=0.15):
    """
    Zoom image by zoom_factor.
    zoom_factor: fraction to zoom in/out (e.g. 0.15 means up to 15%)
    """
    if zoom_factor == 0:
        return image

    h, w = image.shape[:2]
    zoom = 1 + np.random.uniform(-zoom_factor, zoom_factor)

    new_h, new_w = int(h * zoom), int(w * zoom)

    resized = cv2.resize(image, (new_w, new_h))

    if zoom < 1:
        
        pad_h = (h - new_h) // 2
        pad_w = (w - new_w) // 2
        padded = cv2.copyMakeBorder(resized, pad_h, h - new_h - pad_h, pad_w, w - new_w - pad_w,
                                    cv2.BORDER_REPLICATE)
        return padded
    else:
        #original size lai crop garne
        start_h = (new_h - h) // 2
        start_w = (new_w - w) // 2
        cropped = resized[start_h:start_h + h, start_w:start_w + w]
        return cropped

def shift_image(image, width_shift_range=0.2, height_shift_range=0.2):
    """
    Shift image horizontally and vertically by fraction of width and height.
    """
    h, w = image.shape[:2]
    max_dx = w * width_shift_range
    max_dy = h * height_shift_range

    dx = np.random.uniform(-max_dx, max_dx)
    dy = np.random.uniform(-max_dy, max_dy)

    M = np.float32([[1, 0, dx], [0, 1, dy]])
    shifted = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_REPLICATE)
    return shifted

def augment_image(image):
    """
    Apply augmentation similar to ImageDataGenerator parameters.
    Order: rotate -> shear -> zoom -> shift
    """
    image = rotate_image(image, angle=np.random.uniform(-10, 10))
    image = shear_image(image, shear_factor=np.random.uniform(-0.15, 0.15))
    image = zoom_image(image, zoom_factor=0.15)
    image = shift_image(image, width_shift_range=0.2, height_shift_range=0.2)
    return image