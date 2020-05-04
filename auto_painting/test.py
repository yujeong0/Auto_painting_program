import cv2

class Cut_blank(object):
    def main(self):
        while True:
            command = input('$ file_name')
            if command == 'exit':
                return
            self.cut_blank(command)

    def cut_blank(self, file_name):
        origin = cv2.imread(file_name, 0)
        if origin is None:
            print('Not found '+file_name)
            return

        height, width = origin.shape

        print(height, width)

        img = origin[1:476, 1:663]
        cv2.imshow('after', img)
        cv2.imwrite('./multi_img_data/result/result.png', img)
        cv2.waitKey(0)


if __name__== '__main__':
    c = Cut_blank()
    c.main()