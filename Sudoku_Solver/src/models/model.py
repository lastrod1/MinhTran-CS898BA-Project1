from tensorflow.keras import layers, models
 
 
def build_model(input_shape=(28, 28, 1), num_classes=10):

    channels = [48, 96, 144, 192]
 
    model = models.Sequential()
    model.add(layers.Input(shape=input_shape))
    for ch in channels:
        model.add(layers.Conv2D(ch, (7, 7), padding="valid"))
        model.add(layers.BatchNormalization())
        model.add(layers.Activation("relu"))
 
    model.add(layers.Flatten())
    model.add(layers.Dense(num_classes))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation("softmax"))
 
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model