from qfluentwidgets import CardWidget, AvatarWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel

class AboutMeInterface(CardWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("AboutMe")
        layout = QVBoxLayout(self)
        label = QLabel("关于我")
        layout.addWidget(label)
        pass