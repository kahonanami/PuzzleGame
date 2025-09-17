from qfluentwidgets import MSFluentWindow, NavigationItemPosition, Theme, setTheme
from qfluentwidgets import FluentIcon as FIF
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from app.view.setting import SettingInterface, load_game_config
from .easy_puzzle import EasyPuzzleInterface
from .normal_puzzle import NormalPuzzleInterface
from .hard_puzzle import HardPuzzleInterface

class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        
        # 加载游戏设置文件
        self.game_config = load_game_config()
        
        self.setWindowTitle("拼图游戏")
        
        self.setWindowIcon(QIcon("app/resource/images/logo.png"))
        
        self.resize(800, 600)
        self.easy_puzzle = EasyPuzzleInterface()
        self.normal_puzzle = NormalPuzzleInterface()
        self.hard_puzzle = HardPuzzleInterface()    
        self.setting = SettingInterface()
        self.addSubInterface(self.easy_puzzle, FIF.GAME, "简单模式")
        self.addSubInterface(self.normal_puzzle, FIF.PLAY, "普通模式")
        self.addSubInterface(self.hard_puzzle, FIF.FLAG, "困难模式")
        self.addSubInterface(self.setting, FIF.SETTING, "设置", position = NavigationItemPosition.BOTTOM)