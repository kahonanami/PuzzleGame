from qfluentwidgets import MSFluentWindow, NavigationItemPosition, Theme, setTheme
from qfluentwidgets import FluentIcon as FIF
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import json
from app.view.setting import SettingInterface
from .easy_puzzle import EasyPuzzleInterface
from .normal_puzzle import NormalPuzzleInterface
from .hard_puzzle import HardPuzzleInterface
from app.components.music_manager import MusicManager

class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        
        # 加载游戏设置文件
        # self.game_config = load_game_config()
        
        self.setWindowTitle("拼图游戏")
        
        self.setWindowIcon(QIcon("app/resource/images/logo.png"))
        
        self.resize(800, 600)
        
        # 初始化音乐管理器
        self.music_manager = MusicManager(self)
        
        self.easy_puzzle = EasyPuzzleInterface()
        self.normal_puzzle = NormalPuzzleInterface()
        self.hard_puzzle = HardPuzzleInterface()    
        self.setting = SettingInterface()
        self.addSubInterface(self.easy_puzzle, FIF.GAME, "简单模式")
        self.addSubInterface(self.normal_puzzle, FIF.PLAY, "普通模式")
        self.addSubInterface(self.hard_puzzle, FIF.FLAG, "困难模式")
        self.addSubInterface(self.setting, FIF.SETTING, "设置", position = NavigationItemPosition.BOTTOM)
        
        # 连接设置页面的音乐信号到音乐管理器
        self.setting.settings_card.musicToggled.connect(self.music_manager.toggle_music)
        self.setting.settings_card.volumeChanged.connect(self.music_manager.set_volume)

        self.load_settings()
    
    
    def resizeEvent(self, event):
        """窗口大小改变时重新定位音乐卡片"""
        super().resizeEvent(event)
        self.music_manager.reposition_music_card()

    def load_settings(self):
        """加载设置"""
        json_file = "AppData/config.json"
        if os.path.exists(json_file):
            with open(json_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                # 获取配置
                settings = config.get("setting", {})
                sound = settings.get("sound", True)
                timer = settings.get("timer", True)
                theme = settings.get("theme", 0)
                
                # 更新设置界面UI（不触发信号，防止更新界面时出现bug）
                self.setting.settings_card.update_ui_from_config(sound, timer, theme)

                # 应用音乐设置
                if sound:
                    self.music_manager.toggle_music(True)
                
                # 应用计时器设置
                if timer:
                    # TODO: 写个计时器
                    pass
                
                # 应用主题设置
                themes = {0: Theme.LIGHT, 1: Theme.DARK, 2: Theme.AUTO}
                setTheme(themes.get(theme, Theme.AUTO))
        else:
            # 这里走默认设置
            self.setting.settings_card.update_ui_from_config(True, True, 0)
            self.music_manager.toggle_music(True)
            setTheme(Theme.LIGHT)