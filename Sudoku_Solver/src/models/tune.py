from train import combined_training
from model import build_model
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
import optuna

x_train, y_train = combined_training()

def objective(trial):
    learning_rate = trial.suggest_float("learning_rate", .0001, 0.01, log=True)
    batch_size = trial.suggest_categorical("batch_size", [32, 64, 120, 256])

    model = build_model()
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    early_stop = EarlyStopping(
        monitor="val_accuracy", patience=3, restore_best_weights=True
    )

    history = model.fit(
        x_train,
        y_train,
        validation_split=0.1,
        epochs=10,
        batch_size=batch_size,
        callbacks=[early_stop],
        verbose=1,
    )

    return max(history.history["val_accuracy"])

if __name__ == "__main__":
    study = optuna.create_study(direction="maximize", pruner=optuna.pruners.MedianPruner(n_warmup_steps=3))
    study.optimize(objective, n_trials=10)

    print(f"  Best Val Accuracy: {study.best_value:.4f}")
    print(f"  Optimal Learning Rate: {study.best_params['learning_rate']:.6f}")
    print(f"  Optimal Batch Size:   {study.best_params['batch_size']}")