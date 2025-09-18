from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QCheckBox, QSlider
from PyQt5.QtCore import Qt, pyqtSignal
from qfluentwidgets import GroupHeaderCardWidget, PushButton, ComboBox, SearchLineEdit, IconWidget, InfoBarIcon, BodyLabel, PrimaryPushButton, FluentIcon, SwitchButton, Slider, Theme, setTheme, Flyout, InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon as FIF
import json
import os
from pathlib import Path

class SettingsCard(GroupHeaderCardWidget):
    '''游戏设置卡片'''
    
    # 定义信号
    musicToggled = pyqtSignal(bool)  # 音乐开关信号
    volumeChanged = pyqtSignal(int)  # 音量变化信号
    timerToggled = pyqtSignal(bool)  # 计时器开关信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("游戏设置")
        self.setBorderRadius(8)

        # 定义控件
        self.soundSwitch = SwitchButton()           # 音乐控件
        # self.volumeSlider = Slider(Qt.Horizontal)   # 音量大小滑块
        self.timerSwitch = SwitchButton()           # 计时器
        self.themeComboBox = ComboBox()             # 主题选择

        # 底部工具栏
        self.hintIcon = IconWidget(InfoBarIcon.SUCCESS)
        self.hintLabel = BodyLabel("设置保存后将在下次游戏中生效 🎮")
        self.resetButton = PushButton(FIF.ROTATE, "重置")
        self.saveButton = PrimaryPushButton(FIF.SAVE, "保存设置")
        self.bottomLayout = QHBoxLayout()


        # self.volumeSlider.setFixedWidth(200)
        # self.volumeSlider.setRange(0, 100)
        # self.volumeSlider.setValue(70)

        self.themeComboBox.setFixedWidth(200)
        self.themeComboBox.addItems(["浅色主题", "深色主题", "自动切换"])

        self.soundSwitch.setChecked(True)  # 默认开启音乐
        self.timerSwitch.setChecked(True)  # 默认开启计时器

        # 设置底部工具栏布局
        self.hintIcon.setFixedSize(16, 16)
        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomLayout.addWidget(self.hintIcon, 0, Qt.AlignLeft)
        self.bottomLayout.addWidget(self.hintLabel, 0, Qt.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.resetButton, 0, Qt.AlignRight)
        self.bottomLayout.addWidget(self.saveButton, 0, Qt.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignVCenter)

        # 添加游戏设置组件
        self.addGroup(FIF.RINGER.icon(), "游戏音乐", "开启或关闭游戏音乐", self.soundSwitch)
        # self.addGroup(FIF.VOLUME.icon(), "音量大小", "调节游戏音乐音量", self.volumeSlider)
        self.addGroup(FIF.STOP_WATCH.icon(), "显示计时器", "在游戏中显示计时器", self.timerSwitch)
        group = self.addGroup(FIF.BRUSH.icon(), "界面主题", "选择游戏界面主题风格", self.themeComboBox)
        group.setSeparatorVisible(True)

        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)

        # 加载配置
        # self.load_settings()
        
        # 在加载配置后再连接主题切换信号，不然会弹出切换的通知
        self.themeComboBox.currentIndexChanged.connect(self.change_theme)   #主题 -> change_theme
        self.saveButton.clicked.connect(self.save_settings)                 #保存设置 -> save_settings
        self.resetButton.clicked.connect(self.reset_settings)               #重置设置 -> reset_settings
        
        # 连接音乐信号到主窗口
        self.soundSwitch.checkedChanged.connect(self.musicToggled.emit)     # 发送音乐开关信号
        self.timerSwitch.checkedChanged.connect(self.timerToggled.emit)     # 发送计时器开关信号
        # self.volumeSlider.valueChanged.connect(self.volumeChanged.emit)     # 发送音量变化信号

    def update_ui_from_config(self, sound=True, timer=True, theme=0):
        """从配置更新UI状态，不触发信号"""
        # 临时断开信号连接
        self.themeComboBox.currentIndexChanged.disconnect(self.change_theme)
        
        # 更新UI状态
        self.soundSwitch.setChecked(sound)
        self.timerSwitch.setChecked(timer)
        self.themeComboBox.setCurrentIndex(theme)
        
        # 重新连接信号
        self.themeComboBox.currentIndexChanged.connect(self.change_theme)

    def change_theme(self, index):
        """更改主题"""
        themes = {0: Theme.LIGHT, 1: Theme.DARK, 2: Theme.AUTO}
        themes_chinese = {0: "浅色主题", 1: "深色主题", 2: "自动切换"}
        setTheme(themes.get(index, Theme.AUTO))
        # print(f"主题已更改为: {themes.get(index, '未知主题')}")
        InfoBar.success(
            title='',
            content=f"主题已更改为: {themes_chinese.get(index, '未知主题')}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def save_settings(self):
        """保存设置"""
        settings = {
            "setting": {
                "sound": self.soundSwitch.isChecked(),
                "timer": self.timerSwitch.isChecked(),
                "theme": self.themeComboBox.currentIndex()
            }
        }
        try:
            # 获取路径
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent
            
            appdata_dir = project_root / "AppData"
            appdata_dir.mkdir(exist_ok=True)  # 如果目录不存在则创建

            # 配置文件路径 -> /AppData/config.json
            config_file = appdata_dir / "config.json"
            
            # 读取现有配置
            existing_config = {}
            if config_file.exists():
                try:
                    with open(config_file, "r", encoding='utf-8') as f:
                        existing_config = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    existing_config = {}
            
            # 更新配置中的 setting 部分
            existing_config.update(settings)
            
            with open(config_file, "w", encoding='utf-8') as f:
                # 写入json中
                json.dump(existing_config, f, indent=4, ensure_ascii=False)
                InfoBar.success(
                    title='',
                    content=f"设置已保存到 {config_file}",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
        except Exception as e:
            InfoBar.error(
                title='',
                content=f"保存设置时出错: {e}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    def reset_settings(self):
        """重置为默认设置"""
        # 临时断开主题切换信号，避免触发通知
        self.themeComboBox.currentIndexChanged.disconnect(self.change_theme)
        
        self.soundSwitch.setChecked(True)           # 开启音乐
        # self.volumeSlider.setValue(70)              # 音量70%
        self.timerSwitch.setChecked(True)           # 开启计时器
        self.themeComboBox.setCurrentIndex(0)       # 浅色主题
        
        # 重新连接
        self.themeComboBox.currentIndexChanged.connect(self.change_theme)
        
        # 应用浅色主题
        setTheme(Theme.LIGHT)
        
        # print("设置已重置为默认值")
        InfoBar.success(
            title='',
            content=f"设置已重置为默认值",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    
    def showProjects(self):
        """显示项目信息"""
        InfoBar.success(
            title="我的项目",
            content="拼图游戏 - 基于PyQt5和QFluentWidgets的拼图游戏，注重UI风格和用户体验",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=4000,
            parent=self
        )

class SettingInterface(QWidget):
    """设置接口"""
    def __init__(self):
        super().__init__()
        self.setObjectName("Setting")
        self.init_layout()

    def init_layout(self):
        layout = QVBoxLayout()
        self.settings_card = SettingsCard()
        layout.addWidget(self.settings_card)

        self.setLayout(layout)