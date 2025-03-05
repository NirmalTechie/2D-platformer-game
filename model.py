import tensorflow as tf

def load_model():
    model = tf.keras.models.load_model("models/anti_spoofing_model.h5")  # Load pre-trained model
    return model
