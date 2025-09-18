from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QSizePolicy, QFileDialog)
from PyQt5.QtCore import Qt, QSize, QUrl, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath, QColor, QFont
from qfluentwidgets import (PushButton, ComboBox, FluentIcon as FIF,
                            PrimaryPushButton, setFont, FluentIcon,
                            MessageBox, MessageBoxBase, SubtitleLabel)
from qfluentwidgets import StrongBodyLabel, TitleLabel, CardWidget
import random
import os

"""
拼图基类，子类通过继承基类并设置 grid_size 来控制拼图难度
"""

# 控制计时器是否启用
timerEnabled = True

def setTimerEnabled(enabled):
    """设置全局计时器启用状态"""
    global timerEnabled
    timerEnabled = enabled

def getTimerEnabled():
    """获取全局计时器启用状态"""
    return timerEnabled

class ClickableLabel(QLabel):
    """可点击的标签，用于拼图块构造"""
    clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.index = -1
        self.empty = False
        self.setStyleSheet("""
            ClickableLabel {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            ClickableLabel:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)

    def mousePressEvent(self, event):
        if not self.empty:
            self.clicked.emit(self.index)


class PuzzleGridWidget(QWidget):
    """拼图网格容器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)


class ImagePreviewBox(MessageBoxBase):
    """原图预览对话框"""
    def __init__(self, image: QPixmap, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('原图预览')

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        scaled_image = image.scaled(
            400, 400,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.imageLabel.setPixmap(scaled_image)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.imageLabel)

        self.cancelButton.hide()
        self.yesButton.setText("关闭")

        self.widget.setMinimumWidth(450)
        self.widget.setMinimumHeight(500)


class BasePuzzleInterface(QWidget):
    """
    拼图游戏基类，支持不同难度级别
    通过设置 grid_size 来控制拼图难度
    """
    
    def __init__(self, grid_size=4, object_name="puzzle-interface", parent=None):
        super().__init__(parent=parent)
        self.grid_size = grid_size
        self.total_pieces = grid_size * grid_size
        self.empty_piece_index = self.total_pieces - 1  # 最后一块为空白块
        self.object_name = object_name  # 存储对象名称，子类如果不覆盖可能会导致 PyQt5 管理对象时出现问题
        
        self.labels = []
        self.current_image = None
        self.piece_pixmaps = []
        self.current_positions = list(range(self.total_pieces))
        self.moving = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.elapsed_time = 0
        self.timer_running = False
        
        # 拼图区域的基础大小设置
        self.puzzle_area_width = 600
        self.puzzle_area_height = 600
        
        self.initUI()

    def initUI(self):
        mainLayout = QHBoxLayout(self)

        puzzleLayout = QVBoxLayout()
        puzzleLayout.setAlignment(Qt.AlignTop)

        self.puzzleGridWidget = PuzzleGridWidget(self)
        self.gridLayout = self.puzzleGridWidget.layout

        # 根据网格大小计算每个拼图块的大小
        self.piece_size = min(self.puzzle_area_width, self.puzzle_area_height) // self.grid_size
        
        # 创建拼图标签
        for i in range(self.total_pieces):
            label = ClickableLabel(self.puzzleGridWidget)
            label.setFixedSize(self.piece_size, self.piece_size)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.index = i
            label.clicked.connect(self.labelClicked)
            self.labels.append(label)
            self.gridLayout.addWidget(label, i // self.grid_size, i % self.grid_size)

        # 设置拼图网格大小
        self.puzzleGridWidget.setFixedSize(
            self.piece_size * self.grid_size + 2 * (self.grid_size - 1),
            self.piece_size * self.grid_size + 2 * (self.grid_size - 1)
        )

        puzzleLayout.addWidget(self.puzzleGridWidget)

        # 控制面板
        controlLayout = QVBoxLayout()
        controlLayout.setAlignment(Qt.AlignTop)
        controlLayout.setSpacing(20)

        # 难度标签
        # self.difficulty_card = CardWidget()
        # difficulty_card_layout = QVBoxLayout(self.difficulty_card)
        difficulty_names = {3: "简单", 4: "普通", 5: "困难"}
        difficulty_name = difficulty_names.get(self.grid_size, f"{self.grid_size}x{self.grid_size}")
        self.difficultyLabel = StrongBodyLabel(f"🎮 难度：{difficulty_name} ({self.grid_size}x{self.grid_size})", self)
        self.difficultyLabel.setFont(QFont("Microsoft YaHei", 14))
        self.difficultyLabel.setAlignment(Qt.AlignCenter)
        # setFont(self.difficultyLabel, 16)
        # self.difficultyLabel.setTextColor(QColor(0, 255, 0), QColor(255, 0, 0))
        # difficulty_card_layout.addWidget(self.difficultyLabel)
        # difficulty_card_layout.setAlignment(Qt.AlignHCenter) # 居中对齐
        controlLayout.addWidget(self.difficultyLabel)

        self.levelComboBox = ComboBox(self)
        self.levelComboBox.setPlaceholderText("选择关卡")
        self.levelComboBox.addItems(["点击选择图片", "椎名真白", "Cecilia", "喜多郁代", "雷姆", "自定义"])
        self.levelComboBox.currentIndexChanged.connect(self.onLevelChanged)
        controlLayout.addWidget(self.levelComboBox)

        self.fileButton = PushButton(FIF.FOLDER, "选择图片", self)
        self.fileButton.clicked.connect(self.selectImage)
        self.fileButton.hide()
        controlLayout.addWidget(self.fileButton)

        self.shuffleButton = PrimaryPushButton(FIF.SYNC, "打乱", self)
        self.shuffleButton.clicked.connect(self.shufflePuzzle)
        controlLayout.addWidget(self.shuffleButton)

        self.solveButton = PrimaryPushButton(FIF.COMPLETED, "一键通关", self)
        self.solveButton.clicked.connect(self.solvePuzzle)
        controlLayout.addWidget(self.solveButton)

        self.showImageButton = PushButton(FluentIcon.PHOTO, "查看原图", self)
        self.showImageButton.clicked.connect(self.showOriginalImage)
        controlLayout.addWidget(self.showImageButton)

        # 添加空白间距
        spacer = QWidget()
        spacer.setFixedHeight(30)
        controlLayout.addWidget(spacer)

        # 添加计时器显示（根据全局设置）
        # timerCard = CardWidget()
        # timerCardLayout = QVBoxLayout(timerCard)
        self.timerLabel = StrongBodyLabel("⏱️ 用时：00:00", self)
        self.timerLabel.setAlignment(Qt.AlignCenter)
        self.timerLabel.setTextColor(QColor(0, 0, 0), QColor(255, 255, 255))
        self.timerLabel.setFont(QFont("Microsoft YaHei", 14))
        # setFont(self.timerLabel, 14)
        # timerCardLayout.addWidget(self.timerLabel)
        
        # 根据全局设置决定是否显示计时器
        if not getTimerEnabled():
            self.timerLabel.hide()
        
        controlLayout.addWidget(self.timerLabel)

        mainLayout.addLayout(puzzleLayout, 4)
        mainLayout.addLayout(controlLayout, 1)

        self.setObjectName(self.object_name)
        self.setMicaStyle()

    def updateTimer(self):
        """更新计时器显示"""
        if getTimerEnabled():
            self.elapsed_time += 1
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timerLabel.setText(f"⏱️ 用时：{minutes:02d}:{seconds:02d}")

    def updateTimerVisibility(self):
        """更新计时器显示状态，根据全局设置"""
        if getTimerEnabled():
            self.timerLabel.show()
        else:
            self.timerLabel.hide()
            # 如果计时器被禁用，停止计时
            if self.timer_running:
                self.timer.stop()
                self.timer_running = False

    def resetTimer(self):
        """重置计时器"""
        self.timer.stop()
        self.timer_running = False
        self.elapsed_time = 0
        self.timerLabel.setText("⏱️ 用时：00:00")

    def setMicaStyle(self):
        """设置窗口样式"""
        self.resize(800, 600)
        self.setStyleSheet("QWidget{background:transparent}")

    def onLevelChanged(self, index):
        """关卡选择改变事件"""
        if index == self.levelComboBox.count() - 1:  # 自定义图片
            self.fileButton.show()
        else:
            self.fileButton.hide()
            # 使用绝对路径确保图片能正确加载
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            default_images = [
                "", 
                # os.path.join(base_path, "app", "resource", "images", "roxy.jpg"),
                os.path.join(base_path, "app", "resource", "images", "mahiro.jpg"), 
                os.path.join(base_path, "app", "resource", "images", "cecilia.jpg"), 
                os.path.join(base_path, "app", "resource", "images", "ikuyo.jpg"),
                os.path.join(base_path, "app", "resource", "images", "rem.jpg")
            ]
            if index < len(default_images) and default_images[index]:
                self.loadImage(default_images[index])

    def selectImage(self):
        """选择自定义图片"""
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "图片文件 (*.png *.jpg *.bmp)"
        )
        if fileName:
            self.loadImage(fileName)

    def loadImage(self, image_path):
        """加载图片并分割成拼图块"""
        try:
            self.current_image = QPixmap(image_path)
            # 将图片裁剪成正方形
            size = min(self.current_image.width(), self.current_image.height())
            self.current_image = self.current_image.copy(
                (self.current_image.width() - size) // 2,
                (self.current_image.height() - size) // 2,
                size, size
            )
            self.splitImage()
            self.current_positions = list(range(self.total_pieces))
            self.updateDisplay()
            
            # 更新关卡显示
            file_name = image_path.split('/')[-1]
            if len(file_name) > 4:
                file_name = file_name[:4] + '...' if any(
                    '\u4e00' <= char <= '\u9fff' for char in file_name) else file_name[:6] + '...'
            # self.levelLabel.setText(f"关卡：{file_name}")
        except Exception as e:
            MessageBox(
                "错误",
                f"加载图片时出错: {str(e)}",
                self
            ).exec()

    def splitImage(self):
        """将图片分割成拼图块"""
        if not self.current_image:
            return

        self.piece_pixmaps = []
        piece_image_size = self.current_image.width() // self.grid_size
        
        for i in range(self.total_pieces):
            row = i // self.grid_size
            col = i % self.grid_size
            piece = self.current_image.copy(
                col * piece_image_size,
                row * piece_image_size,
                piece_image_size,
                piece_image_size
            )
            # 缩放到标签大小
            piece = piece.scaled(self.piece_size, self.piece_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.piece_pixmaps.append(piece)

    def updateDisplay(self):
        """更新拼图显示"""
        if not self.piece_pixmaps:
            return

        for i, label in enumerate(self.labels):
            current_piece = self.current_positions[i]
            if current_piece == self.empty_piece_index:
                label.clear()
                label.empty = True
            else:
                label.setPixmap(self.piece_pixmaps[current_piece])
                label.empty = False

    def shufflePuzzle(self):
        """打乱拼图"""
        if not self.piece_pixmaps or self.moving:
            return

        self.resetTimer()

        empty_index = self.current_positions.index(self.empty_piece_index)
        current_empty = empty_index

        # 通过随机移动来打乱拼图
        for _ in range(1000):  # 增加打乱次数确保充分混乱
            possible_moves = []
            row = current_empty // self.grid_size
            col = current_empty % self.grid_size

            # 找到可以移动的位置
            if row > 0: possible_moves.append(current_empty - self.grid_size)
            if row < self.grid_size - 1: possible_moves.append(current_empty + self.grid_size)
            if col > 0: possible_moves.append(current_empty - 1)
            if col < self.grid_size - 1: possible_moves.append(current_empty + 1)

            next_empty = random.choice(possible_moves)
            self.current_positions[current_empty], self.current_positions[next_empty] = \
                self.current_positions[next_empty], self.current_positions[current_empty]
            current_empty = next_empty

        self.updateDisplay()

    def labelClicked(self, clicked_index):
        """处理拼图块点击事件"""
        if not self.piece_pixmaps or self.moving:
            return

        # 开始计时（仅在启用时）
        if getTimerEnabled() and not self.timer_running and (self.elapsed_time == 0 or not self.timer.isActive()):
            self.timer.start(1000)
            self.timer_running = True

        self.moving = True
        try:
            empty_index = self.current_positions.index(self.empty_piece_index)
            row1, col1 = clicked_index // self.grid_size, clicked_index % self.grid_size
            row2, col2 = empty_index // self.grid_size, empty_index % self.grid_size

            # 检查是否相邻
            if abs(row1 - row2) + abs(col1 - col2) == 1:
                self.current_positions[clicked_index], self.current_positions[empty_index] = \
                    self.current_positions[empty_index], self.current_positions[clicked_index]
                self.updateDisplay()
                self.checkCompletion()
        finally:
            self.moving = False

    def checkCompletion(self):
        """检查是否完成拼图"""
        if self.current_positions == list(range(self.total_pieces)):
            # 显示最后一块拼图
            self.labels[self.empty_piece_index].setPixmap(self.piece_pixmaps[self.empty_piece_index])
            self.labels[self.empty_piece_index].empty = False
            self.timer.stop()
            self.timer_running = False
            MessageBox(
                "恭喜",
                f"恭喜你完成拼图！\n用时：{self.elapsed_time//60:02d}:{self.elapsed_time%60:02d}",
                self
            ).exec()

    def solvePuzzle(self):
        """一键通关"""
        if not self.piece_pixmaps or self.moving:
            return

        self.timer.stop()
        self.timer_running = False

        self.current_positions = list(range(self.total_pieces))
        self.updateDisplay()
        self.labels[self.empty_piece_index].setPixmap(self.piece_pixmaps[self.empty_piece_index])
        self.labels[self.empty_piece_index].empty = False

        MessageBox(
            "恭喜",
            f"恭喜你完成拼图！\n用时：{self.elapsed_time // 60:02d}:{self.elapsed_time % 60:02d}\n*此成绩经由作弊功能获得",
            self
        ).exec()

    def showOriginalImage(self):
        """显示原图预览"""
        if not self.current_image:
            return

        preview_dialog = ImagePreviewBox(self.current_image, self)
        preview_dialog.exec()
