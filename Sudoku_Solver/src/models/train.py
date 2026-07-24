import os
import sys

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from model import build_model

MODEL_OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "mnist_cnn.keras")
FONT_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "font_digits.npz")

def load_data():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    return (x_train, y_train), (x_test, y_test)

def load_font_digits(test_holdout):
    data = np.load(FONT_DATA_PATH)
    images = np.expand_dims(data["images"].astype("float32") / 255.0, -1)
    labels = data["labels"]
    font_ids = data["font_ids"]

    unique_fonts = np.unique(font_ids)
    rand = np.random.default_rng(0)
    rand.shuffle(unique_fonts)
    n_test_fonts = max(1, int(len(unique_fonts) * test_holdout))
    test_fonts = set(unique_fonts[:n_test_fonts])

    test_mask = np.isin(font_ids, list(test_fonts))
    return (images[~test_mask], labels[~test_mask]), (images[test_mask], labels[test_mask])

def train(epochs=150, batch_size=120):
    (x_train_m, y_train_m), (x_test_m, y_test_m) = load_data()
    (x_train_f, y_train_f), (x_test_f, y_test_f) = load_font_digits(.15)
    x_train = np.concatenate((x_train_m, x_train_f))
    y_train = np.concatenate((y_train_m, y_train_f))

    # quick shuff to make sure the fonts aren't at the end
    idx = np.arange(len(x_train))
    np.random.default_rng(67).shuffle(idx)
    x_train = x_train[idx]
    y_train = y_train[idx]


    model = build_model()
    model.summary()

    early_stop = EarlyStopping(
        monitor="val_accuracy", patience=5, restore_best_weights=True
    )

    history = model.fit(
        x_train, y_train,
        validation_split=0.1,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stop],
    )

    mnist_loss, mnist_acc = model.evaluate(x_test_m, y_test_m, verbose=0)
    print(f"\nTest accuracy: {mnist_acc:.4f}")
    print(f"Test loss: {mnist_loss:.4f}")

    font_loss, font_acc = model.evaluate(x_test_f, y_test_f, verbose=0)
    print(f"\nTest accuracy: {font_acc:.4f}")
    print(f"Test loss: {font_loss:.4f}")

    os.makedirs(os.path.dirname(MODEL_OUT_PATH), exist_ok=True)
    model.save(MODEL_OUT_PATH)

    return model, history


if __name__ == "__main__":
    train()