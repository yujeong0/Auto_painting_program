from PIL import Image
import os, glob, numpy as np
from keras.models import load_model
import cv2
# from Segmentation import Segmentation

class classification():
    def __init__(self):
        self.label = ''
        self.classify()

    def classify(self):
        caltech_dir = "./multi_img_data/imgs_others_test_sketch"

        image_w = 64
        image_h = 64

        pixels = image_h * image_w * 3

        X = []
        filenames = []
        files = glob.glob(caltech_dir+"/*.*")
        for i, f in enumerate(files):
            img = Image.open(f)
            img = img.convert("RGB")
            img = img.resize((image_w, image_h))
            data = np.asarray(img)
            filenames.append(f)
            X.append(data)

        X = np.array(X)
        model = load_model('./model/multi_img_classification.model')

        prediction = model.predict(X)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
        cnt = 0

        # sg = Segmentation()

        for i in prediction:
            pre_ans = i.argmax()  # 예측 레이블
            # print(i)
            # print(pre_ans)
            pre_ans_str = ''
            if pre_ans == 0: pre_ans_str = "사과"
            elif pre_ans == 1: pre_ans_str = "체리"
            elif pre_ans == 2: pre_ans_str = "토마토"
            elif pre_ans == 3: pre_ans_str = "꽃"
            elif pre_ans == 4: pre_ans_str = "아보카도"
            elif pre_ans == 5: pre_ans_str = "나뭇잎"
            elif pre_ans == 6: pre_ans_str = "당근"
            elif pre_ans == 7: pre_ans_str = "조개"

            if i[0] >= 0.8:
                print("해당 " + filenames[cnt].split("\\")[1] + "이미지는 " + pre_ans_str + "으로 추정됩니다.")
                self.label = 'apple'
            elif i[1] >= 0.8:
                print("해당 " + filenames[cnt].split("\\")[1] + "이미지는 " + pre_ans_str + "으로 추정됩니다.")
                self.label = 'cherry'
            elif i[2] >= 0.8:
                print("해당 " + filenames[cnt].split("\\")[1] + "이미지는 " + pre_ans_str + "으로 추정됩니다.")
                self.label = 'tomato'
            elif i[3] >= 0.8:
                print("해당 " + filenames[cnt].split("\\")[1] + "이미지는 " + pre_ans_str + "으로 추정됩니다.")
                self.label = 'flower'
            elif i[4] >= 0.8:
                print("해당 " + filenames[cnt].split("\\")[1] + "이미지는 " + pre_ans_str + "으로 추정됩니다.")
                self.label = 'avocado'
            elif i[5] >= 0.8:
                print("해당 " + filenames[cnt].split("\\")[1] + "이미지는 " + pre_ans_str + "으로 추정됩니다.")
                self.label = 'leaf'
            elif i[6] >= 0.8:
                print("해당 " + filenames[cnt].split("\\")[1] + "이미지는 " + pre_ans_str + "으로 추정됩니다.")
                self.label = 'carrot'
            elif i[7] >= 0.8:
                print("해당 " + filenames[cnt].split("\\")[1] + "이미지는 " + pre_ans_str + "으로 추정됩니다.")
                self.label = 'shellfish'
            else:
                print("해당 이미지는 없는 데이터입니다.")
                self.label = 'none'

            cnt += 1
