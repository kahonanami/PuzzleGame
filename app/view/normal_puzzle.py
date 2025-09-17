from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class NormalPuzzleInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("NormalPuzzle")
        layout = QVBoxLayout()
        label = QLabel("普通拼图模式")
        layout.addWidget(label)
        self.setLayout(layout)

    def display(self):
        print("Displaying Normal Puzzle Interface")