import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
from classification import classification
from Fill_color import Fill_color
import cv2

class drawing_board(QWidget):
    def __init__(self):
        super().__init__()
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # 화면크기스케일링
        self.file = ''

        # 전체 폼 박스
        formbox = QHBoxLayout()
        self.setLayout(formbox)

        # 좌, 우 레이아웃박스
        left = QVBoxLayout()
        right = QVBoxLayout()
        self.right2 = QVBoxLayout()

        # 그룹박스1 생성 및 좌 레이아웃 배치
        gb = QGroupBox('그리기 종류')
        left.addWidget(gb)

        # 그룹박스1 에서 사용할 레이아웃
        box = QVBoxLayout()
        gb.setLayout(box)

        # 그룹박스 1 의 라디오 버튼 배치
        text = ['line', 'Curve', 'Rectange', 'Ellipse']
        self.radiobtns = []

        for i in range(len(text)):
            self.radiobtns.append(QRadioButton(text[i], self))
            self.radiobtns[i].clicked.connect(self.radioClicked)
            box.addWidget(self.radiobtns[i])

        self.radiobtns[1].setChecked(True)
        self.drawType = 1

        # 그룹박스2
        gb = QGroupBox('펜 설정')
        left.addWidget(gb)

        grid = QGridLayout()
        gb.setLayout(grid)

        label = QLabel('선굵기')
        grid.addWidget(label, 0, 0)

        self.combo = QComboBox()
        grid.addWidget(self.combo, 0, 1)

        for i in range(4, 21):
            self.combo.addItem(str(i))

        label = QLabel('선색상')
        grid.addWidget(label, 1, 0)

        self.pencolor = QColor(0, 0, 0)
        self.penbtn = QPushButton()
        self.penbtn.setStyleSheet('background-color: rgb(0,0,0)')
        self.penbtn.clicked.connect(self.showColorDlg)
        grid.addWidget(self.penbtn, 1, 1)

        # 그룹박스3
        gb = QGroupBox('붓 설정')
        left.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        label = QLabel('붓색상')
        hbox.addWidget(label)

        self.brushcolor = QColor(255, 255, 255)
        self.brushbtn = QPushButton()
        self.brushbtn.setStyleSheet('background-color: rgb(255,255,255)')
        self.brushbtn.clicked.connect(self.showColorDlg)
        hbox.addWidget(self.brushbtn)

        # 그룹박스4
        gb = QGroupBox('지우개')
        left.addWidget(gb)

        hbox = QHBoxLayout()
        gb.setLayout(hbox)

        self.checkbox = QCheckBox('지우개 동작')
        self.checkbox.stateChanged.connect(self.checkClicked)
        hbox.addWidget(self.checkbox)

        # 전체 지우기
        removebutton = QPushButton('전체 지우기', self)
        left.addWidget(removebutton)
        removebutton.clicked.connect(self.remove_all)

        # 사진저장 버튼
        # savebutton = QPushButton('그림 저장', self)
        # left.addWidget(savebutton)
        # savebutton.clicked.connect(self.save_image)

        # painting 버튼
        paintingbutton = QPushButton('자동 채색', self)
        left.addWidget(paintingbutton)
        paintingbutton.clicked.connect(self.load_image)

        left.addStretch(1)  # 그냥 레이아웃 여백 추가

        # 우 레이아웃 박스에 그래픽 뷰 추가
        self.view = CView(self)
        self.view.setFixedWidth(300)
        self.view.setFixedHeight(300)
        right.addWidget(self.view)

        # 제일 오른쪽 레이아웃에 빈 흰색 배경
        pixmap = QPixmap('whiteimage.png')
        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(pixmap)
        self.right2.addWidget(self.lbl_img)

        # 전체 폼박스에 레이아웃 박스 배치
        formbox.addLayout(left)
        formbox.addLayout(right)
        formbox.addLayout(self.right2)

        formbox.setStretchFactor(left, 0)
        formbox.setStretchFactor(right, 1)

        self.setGeometry(100, 100, 700, 400)

    def radioClicked(self):
        for i in range(len(self.radiobtns)):
            if self.radiobtns[i].isChecked():
                self.drawType = i
                break

    def checkClicked(self):
        pass

    def showColorDlg(self):

        # 색상 대화상자 생성
        color = QColorDialog.getColor()

        sender = self.sender()

        # 색상이 유효한 값이면 참, QFrame에 색 적용
        if sender == self.penbtn and color.isValid():
            self.pencolor = color
            self.penbtn.setStyleSheet('background-color: {}'.format(color.name()))
        else:
            self.brushcolor = color
            self.brushbtn.setStyleSheet('background-color: {}'.format(color.name()))

    def save_image(self):
        date = datetime.now()
        filename = 'Screenshot ' + date.strftime('%Y-%m-%d_%H-%M-%S.png')
        img = QPixmap(self.view.grab(self.view.sceneRect().toRect()))
        self.file = "./multi_img_data/imgs_others_test_sketch/" + filename
        img.save(self.file, 'png')
        img = cv2.imread(self.file, 0)
        img = img[1:476, 1:663]
        cv2.imwrite(self.file, img)

    def remove_all(self):
        for i in self.view.scene.items():
            self.view.scene.removeItem(i)

    def load_image(self):
        self.save_image()
        self.lbl_img.hide()     # 전 이미지 숨김

        label = classification().label  # 이미지 분류
        # print(label)

        fill = Fill_color(self.file, label)    #이미지 색칠
        self.file = fill.file
        print(self.file)

        pixmap = QPixmap(self.file)  # jpg 는 안되는데 왜 안되는 지 아직 모르겠다..

        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(pixmap)
        self.right2.addWidget(self.lbl_img)


# QGraphicsView display QGraphicsScene
class CView(QGraphicsView):

    def __init__(self, parent):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.items = []

        self.start = QPointF()
        self.end = QPointF()

        self.setRenderHint(QPainter.HighQualityAntialiasing)

    def moveEvent(self, e):
        rect = QRectF(self.rect())
        rect.adjust(0, 0, -2, -2)

        self.scene.setSceneRect(rect)

    def mousePressEvent(self, e):

        if e.button() == Qt.LeftButton:
            # 시작점 저장
            self.start = e.pos()
            self.end = e.pos()

    def mouseMoveEvent(self, e):
        # e.buttons()는 정수형 값을 리턴, e.button()은 move시 Qt.Nobutton 리턴
        if e.buttons() & Qt.LeftButton:

            self.end = e.pos()

            if self.parent().checkbox.isChecked():
                pen = QPen(QColor(255, 255, 255), 10)
                path = QPainterPath()
                path.moveTo(self.start)
                path.lineTo(self.end)
                self.scene.addPath(path, pen)
                self.start = e.pos()
                return None

            pen = QPen(self.parent().pencolor, self.parent().combo.currentIndex()+3)

            # 직선 그리기
            if self.parent().drawType == 0:

                # 장면에 그려진 이전 선을 제거
                if len(self.items) > 0:
                    self.scene.removeItem(self.items[-1])
                    del (self.items[-1])

                    # 현재 선 추가
                line = QLineF(self.start.x(), self.start.y(), self.end.x(), self.end.y())
                self.items.append(self.scene.addLine(line, pen))

            # 곡선 그리기
            if self.parent().drawType == 1:
                # Path 이용
                path = QPainterPath()
                path.moveTo(self.start)
                path.lineTo(self.end)
                self.scene.addPath(path, pen)

                # Line 이용
                # line = QLineF(self.start.x(), self.start.y(), self.end.x(), self.end.y())
                # self.scene.addLine(line, pen)

                # 시작점을 다시 기존 끝점으로
                self.start = e.pos()

            # 사각형 그리기
            if self.parent().drawType == 2:
                brush = QBrush(self.parent().brushcolor)

                if len(self.items) > 0:
                    self.scene.removeItem(self.items[-1])
                    del (self.items[-1])

                rect = QRectF(self.start, self.end)
                self.items.append(self.scene.addRect(rect, pen, brush))

            # 원 그리기
            if self.parent().drawType == 3:
                brush = QBrush(self.parent().brushcolor)

                if len(self.items) > 0:
                    self.scene.removeItem(self.items[-1])
                    del (self.items[-1])

                rect = QRectF(self.start, self.end)
                self.items.append(self.scene.addEllipse(rect, pen, brush))

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:

            if self.parent().checkbox.isChecked():
                return None

            pen = QPen(self.parent().pencolor, self.parent().combo.currentIndex())

            if self.parent().drawType == 0:
                self.items.clear()
                line = QLineF(self.start.x(), self.start.y(), self.end.x(), self.end.y())

                self.scene.addLine(line, pen)

            if self.parent().drawType == 2:
                brush = QBrush(self.parent().brushcolor)

                self.items.clear()
                rect = QRectF(self.start, self.end)
                self.scene.addRect(rect, pen, brush)

            if self.parent().drawType == 3:
                brush = QBrush(self.parent().brushcolor)

                self.items.clear()
                rect = QRectF(self.start, self.end)
                self.scene.addEllipse(rect, pen, brush)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = drawing_board()
#     w.show()
#     sys.exit(app.exec_())
