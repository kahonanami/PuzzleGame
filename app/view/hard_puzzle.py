from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class HardPuzzleInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("HardPuzzle")
        layout = QVBoxLayout()
        label = QLabel("困难拼图模式")
        layout.addWidget(label)
        self.setLayout(layout)

    def display(self):
        print("Displaying Hard Puzzle Interface")