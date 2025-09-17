from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class EasyPuzzleInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("EasyPuzzle")
        layout = QVBoxLayout()
        label = QLabel("简单拼图模式")
        layout.addWidget(label)
        self.setLayout(layout)

    def display(self):
        print("Displaying Easy Puzzle Interface")