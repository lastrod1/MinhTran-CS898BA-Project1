from tensorflow.keras import layers, models
 
 
def build_model(input_shape=(28, 28, 1), num_classes=10):

    channels = [32, 48, 64, 80, 96, 112, 128, 114, 160, 176]
    idx = {2, 5, 8}
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    for i, ch in enumerate(channels):
        model.add(layers.Conv2D(ch, (3, 3), padding="same"))
        model.add(layers.BatchNormalization())
        model.add(layers.Activation("relu"))

        if i in idx:
            model.add(layers.MaxPool2D(2,2))

 
    model.add(layers.GlobalAveragePooling2D())
    model.add(layers.Dense(num_classes))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation("softmax"))
 
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model