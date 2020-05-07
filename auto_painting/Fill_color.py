# -*- cording : utf-8 -*-
# 색을 단색이 아니도록 추가해야함

import cv2
import numpy as np

class Fill_color(object):
    def __init__(self, filename):
        self.file = ''
        self.start(filename)

    def start(self, filename):
        # while True:
            # file = input('$ File Name: ')
            # file = './multi_img_data/imgs_others_test_sketch/' + filename
            origin = cv2.imread(filename,0)
            origin_color = cv2.imread(filename)

            if origin is None or origin_color is None:
                print('Not found '+filename)
            else:
                bin_img = self.binarize(origin, 220)
                open_img = self.image_open(bin_img)
                reverse_img = self.reverse(open_img)
                dilate_img = self.image_dilate(reverse_img, 1, 1)
                white_img, transform = self.fill_white(reverse_img, dilate_img)
                color_img = self.fill_color(origin_color,transform,[0,0,255])
                # cv2.imshow('Result',color_img)
                cv2.imwrite('./multi_img_data/result/result.png', color_img)
                self.file = './multi_img_data/result/result.png'
                # cv2.waitKey(0)

    def binarize(self, img, threshold):
        # 이진화
        ret, bin_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
        return bin_img

    def image_open(self, img, kernel_size=5):
        # 열기
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        result = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        return result

    def reverse(self, img):
        # 밝기 반전
        for i in range(len(img)):
            for j in range(len(img[0])):
                if img[i][j] == 0:
                    img[i][j] = 255
                else:
                    img[i][j] = 0
        return img

    def image_dilate(self, img, kernel_size, n):
        #팽창
        for i in range(n):
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            img = cv2.dilate(img, kernel, iterations=1)
        return img

    def fill_white(self, img1, img2):
        x, y = int(len(img1) / 2), int(len(img1[0]) / 2)
        color = img2[:]
        q = [[x, y]]
        offset = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        transform = []
        while q:
            cur = q.pop(0)
            x, y = cur[0], cur[1]
            if x < 0 or y < 0:
                pass
            elif x > len(color)-1 or y > len(color[0])-1:
                pass
            elif color[x][y] == 255:
                pass
            else:
                color[x][y] = 255
                transform.append([x, y])
                for i in range(4):
                    q.append([x + offset[i][0], y + offset[i][1]])
        return [color, transform]

    # 픽셀값 변경하면서 해보는중
    def fill_color(self, img, transform, color):
        for t in transform:
            img[t[0]][t[1]] = np.array(color)
        return img

    # def fill_color(self, img, transform, color):
    #     count = 0
    #     temp_color = copy.deepcopy(color)
    #
    #     for t in transform:
    #         img[t[0]][t[1]] = np.array(temp_color)
    #
    #         if count >= 100:
    #             temp_color = copy.deepcopy(color)
    #             count = count % 100
    #         else:
    #             temp_color[0] += 3
    #             temp_color[1] += 3
    #             count += 3
    #     dst = cv2.GaussianBlur(img, (5, 5), 0)
    #     return dst

#     def fill_color(self, img, transform, color):
#         r, g ,b = color[2], color[1], color[0]

#         for t in transform:
#             temp_color = [b + random.randrange(10,100),g + random.randrange(10,100), r]
#             img[t[0]][t[1]] = np.array(temp_color)

#         dst = cv2.GaussianBlur(img, (5, 5), 0)
#         return dst
#
# main = Fill_color()
# main.start()
