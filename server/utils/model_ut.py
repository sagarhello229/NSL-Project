from tensorflow.keras.models import Sequential, load_model as keras_load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
from tensorflow.keras.optimizers import Adam

def build_cnn_model(input_shape=(96, 96, 3), num_classes=36):
    """
    Build and return CNN model based on provided architecture.
    """
    model = Sequential([
        Input(shape=input_shape),

        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),

        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),

        Flatten(),
        Dense(128, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    return model

def compile_model(model, learning_rate=0.001):
    """
    Compile model with Adam optimizer and categorical crossentropy loss.
    """
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def save_model(model, filepath):
    """
    Save Keras model to file.
    """
    model.save(filepath)

def load_model(filepath):
    """
    Load Keras model from file.
    """
    return keras_load_model(filepath)

def predict_label(model, input_data):
    """
    Predict label index from model output.
    input_data should be batch of images (numpy array).
    """
    preds = model.predict(input_data)
    return preds.argmax(axis=-1)[0]
