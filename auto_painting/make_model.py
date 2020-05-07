from PIL import Image
import os, glob, numpy as np
from sklearn.model_selection import train_test_split

class make_model:
    def __init__(self):
        self.make_npy_file()
        self.make_model()

    def make_npy_file(self):
        caltech_dir = "./multi_img_data/imgs_others/train"

        categories = ["apple", "cherry", "tomato", "flower", "avocado", "leaf", "carrot", "shellfish"]
        nb_classes = len(categories)
        print(nb_classes)

        image_w = 64
        image_h = 64

        pixels = image_h * image_w * 3

        X = []
        y = []

        for idx, cat in enumerate(categories):
            # one-hot 돌리기.
            label = [0 for i in range(nb_classes)]
            label[idx] = 1

            image_dir = caltech_dir + "/" + cat
            files = glob.glob(image_dir + "/*.png")
            print(cat, " 파일 길이 : ", len(files))
            for i, f in enumerate(files):
                img = Image.open(f)
                img = img.convert("RGB")
                img = img.resize((image_w, image_h))
                data = np.asarray(img)

                X.append(data)
                y.append(label)

                if i % 700 == 0:
                    print(cat, " : ", f)

        X = np.array(X)
        y = np.array(y)
        # 1 0 0 0 이면 airplanes
        # 0 1 0 0 이면 buddha 이런식

        X_train, X_test, y_train, y_test = train_test_split(X, y)
        xy = (X_train, X_test, y_train, y_test)
        np.save("./numpy_data/multi_image_data.npy", xy)

        print("ok", len(y))

    def make_model(self):
        from keras.models import Sequential
        from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
        from keras.callbacks import EarlyStopping, ModelCheckpoint
        import matplotlib.pyplot as plt
        import keras.backend.tensorflow_backend as K
        import tensorflow as tf

        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        session = tf.compat.v1.Session(config=config)

        X_train, X_test, y_train, y_test = np.load("./numpy_data/multi_image_data.npy")
        print(X_train.shape)
        print(X_train.shape[0])


        categories = ["apple", "cherry", "tomato", "flower", "avocado", "leaf", "carrot", "shellfish"]
        nb_classes = len(categories)

        X_train = X_train.astype(float) / 255
        X_test = X_test.astype(float) / 255

        with K.tf_ops.device('/device:CPU:0'):
            model = Sequential()
            model.add(Conv2D(32, (3, 3), padding="same", input_shape=X_train.shape[1:],
                             activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.25))

            model.add(Conv2D(64, (3, 3), padding="same", activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Dropout(0.25))

            model.add(Flatten())
            model.add(Dense(256, activation='relu'))
            model.add(Dropout(0.5))
            model.add(Dense(nb_classes, activation='softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            model_dir = './model'

            if not os.path.exists(model_dir):
                os.mkdir(model_dir)

            model_path = model_dir + '/multi_img_classification.model'
            checkpoint = ModelCheckpoint(filepath=model_path, monitor='val_loss',
                                         verbose=1, save_best_only=True)
            early_stopping = EarlyStopping(monitor='val_loss', patience=6)

        model.summary()

        history = model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_test, y_test), callbacks=[checkpoint, early_stopping])

        print("정확도 : %.4f" % (model.evaluate(X_test, y_test)[1]))


        y_vloss = history.history['val_loss']
        y_loss = history.history['loss']

        x_len = np.arange(len(y_loss))

        plt.plot(x_len, y_vloss, marker='.', c='red', label='val_set_loss')
        plt.plot(x_len, y_loss, marker='.', c='blue', label='train_set_loss')
        plt.legend()
        plt.xlabel('epochs')
        plt.ylabel('loss')
        plt.grid()
        plt.show()