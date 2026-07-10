import os
import sys

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from model import build_model

MODEL_OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "mnist_cnn.keras")


def load_data():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    return (x_train, y_train), (x_test, y_test)


def train(epochs=150, batch_size=120):
    (x_train, y_train), (x_test, y_test) = load_data()

    model = build_model()
    model.summary()

    early_stop = EarlyStopping(
        monitor="val_accuracy", patience=3, restore_best_weights=True
    )

    history = model.fit(
        x_train, y_train,
        validation_split=0.1,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stop],
    )

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nTest accuracy: {test_acc:.4f}")
    print(f"Test loss: {test_loss:.4f}")

    os.makedirs(os.path.dirname(MODEL_OUT_PATH), exist_ok=True)
    model.save(MODEL_OUT_PATH)

    return model, history


if __name__ == "__main__":
    train()