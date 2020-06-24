import numpy as np
import os, glob, numpy as np
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

caltech_dir = "./multi_img_data/imgs_others/train"

categories = ["apple", "cherry", "carrot", "flower", "leaf", "tomato", "shellfish"]
nb_classes = len(categories)
print(nb_classes)

np.random.seed(5)

data_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=90,
                                   shear_range=5.5,
                                   # width_shift_range=0.1,
                                   # height_shift_range=0.1,
                                   zoom_range=0,
                                   horizontal_flip=True,
                                   vertical_flip=True,
                                   fill_mode='nearest')

for idx, cat in enumerate(categories):
    # one-hot 돌리기.
    label = [0 for i in range(nb_classes)]
    label[idx] = 1

    image_dir = caltech_dir + "/" + cat
    files = glob.glob(image_dir + "/*.png")
    # print(files)
    # print("\n")
    file_number = 1
    for i, f in enumerate(files):

        file_name = cat + ' (' + str(file_number) + ')'
        print(file_name)

        img = load_img(image_dir + '/' + file_name + '.png')
        x = img_to_array(img)
        x = x.reshape((1,) + x.shape)

        i = 0
        file_name_freq = 1
        for batch in data_datagen.flow(x, batch_size=1,
                                       save_to_dir=image_dir,
                                       save_prefix=file_name + '_plus_'+str(file_name_freq),
                                       save_format='png'):
            i += 1
            file_name_freq += 1

            if i > 5:
                break

        file_number += 1
