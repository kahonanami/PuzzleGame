from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QCheckBox, QSlider
from PyQt5.QtCore import Qt
from qfluentwidgets import GroupHeaderCardWidget, PushButton, ComboBox, SearchLineEdit, IconWidget, InfoBarIcon, BodyLabel, PrimaryPushButton, FluentIcon, SwitchButton, Slider, Theme, setTheme, Flyout, InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon as FIF
import json
import os
from pathlib import Path

def load_game_config():
    """加载配置文件"""
    try:
        # 获取项目根目录
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent
        config_file = project_root / "AppData" / "settings.json"
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # 应用主题设置
            theme_index = settings.get('theme', 0)
            themes = {0: Theme.LIGHT, 1: Theme.DARK, 2: Theme.AUTO}
            setTheme(themes.get(theme_index, Theme.AUTO))
            
            return settings
        else:
            # 如果配置文件不存在，应用默认主题
            setTheme(Theme.LIGHT)
            return None
            
    except Exception as e:
        print(f"加载游戏配置失败: {e}")
        setTheme(Theme.LIGHT)
        return None

class SettingsCard(GroupHeaderCardWidget):
    '''游戏设置卡片'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("游戏设置")
        self.setBorderRadius(8)

        # 定义控件
        self.soundSwitch = SwitchButton()           # 音乐控件
        self.volumeSlider = Slider(Qt.Horizontal)   # 音量大小滑块
        self.timerSwitch = SwitchButton()           # 计时器
        self.themeComboBox = ComboBox()             # 主题选择

        # 底部工具栏
        self.hintIcon = IconWidget(InfoBarIcon.SUCCESS)
        self.hintLabel = BodyLabel("设置保存后将在下次游戏中生效 🎮")
        self.resetButton = PushButton(FIF.ROTATE, "重置")
        self.saveButton = PrimaryPushButton(FIF.SAVE, "保存设置")
        self.bottomLayout = QHBoxLayout()


        self.volumeSlider.setFixedWidth(200)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(70)

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
        self.addGroup(FIF.VOLUME.icon(), "音量大小", "调节游戏音乐音量", self.volumeSlider)
        self.addGroup(FIF.STOP_WATCH.icon(), "显示计时器", "在游戏中显示计时器", self.timerSwitch)
        group = self.addGroup(FIF.BRUSH.icon(), "界面主题", "选择游戏界面主题风格", self.themeComboBox)
        group.setSeparatorVisible(True)

        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)

        # 加载配置
        self.load_settings()
        
        # 在加载配置后再连接主题切换信号，不然会弹出切换的通知
        self.themeComboBox.currentIndexChanged.connect(self.change_theme)   #主题 -> change_theme
        self.saveButton.clicked.connect(self.save_settings)                 #保存设置 -> save_settings
        self.resetButton.clicked.connect(self.reset_settings)               #重置设置 -> reset_settings
        # 音乐功能已禁用 - 保留UI组件但不连接功能
        # self.soundSwitch.checkedChanged.connect(self.music_manager.toggle_music)          #音乐开关 -> toggle_music
        # self.volumeSlider.valueChanged.connect(self.music_manager.change_volume)          #音量调节 -> change_volume
        
    def load_settings(self):
        """从配置文件加载设置"""
        try:
            # 获取路径
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent
            config_file = project_root / "AppData" / "settings.json"
            
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # 应用设置到界面
                sound_enabled = settings.get('sound', True)
                volume = settings.get('volume', 70)
                
                self.soundSwitch.setChecked(sound_enabled)
                self.volumeSlider.setValue(volume)
                self.timerSwitch.setChecked(settings.get('timer', True))
                
                # 音乐功能已禁用 - 只保留UI状态
                # self.music_manager.set_volume(volume)
                # if sound_enabled:
                #     self.music_manager.play()
                # else:
                #     self.music_manager.stop()
                
                # 应用主题设置（此时信号还未连接，不会触发通知）
                theme_index = settings.get('theme', 0)
                if 0 <= theme_index < self.themeComboBox.count():
                    self.themeComboBox.setCurrentIndex(theme_index)
                    
                    # 应用主题
                    themes = {0: Theme.LIGHT, 1: Theme.DARK, 2: Theme.AUTO}
                    setTheme(themes.get(theme_index, Theme.AUTO))
                    
        except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
            # print(f"加载配置文件失败，使用默认设置: {e}")
            InfoBar.success(
            title='',
            content=f"加载配置文件失败，使用默认设置: {e}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
            self.set_default_settings()
    
    def set_default_settings(self):
        """设置默认值"""
        self.soundSwitch.setChecked(True)
        self.volumeSlider.setValue(70)
        self.timerSwitch.setChecked(True)
        self.themeComboBox.setCurrentIndex(0)
        setTheme(Theme.LIGHT)
        
        # 音乐功能已禁用 - 只保留UI默认状态
        # self.music_manager.set_volume(70)
        # self.music_manager.play()

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
        # print("游戏设置已保存:")
        # print(f"- 音乐开启: {self.soundSwitch.isChecked()}")
        # print(f"- 音量大小: {self.volumeSlider.value()}")
        # print(f"- 显示计时器: {self.timerSwitch.isChecked()}")
        # print(f"- 界面主题: {self.themeComboBox.currentText()}")
        settings = {
            "sound": self.soundSwitch.isChecked(),
            "volume": self.volumeSlider.value(),
            "timer": self.timerSwitch.isChecked(),
            "theme": self.themeComboBox.currentIndex()
        }
        try:
            # 获取路径
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent
            
            appdata_dir = project_root / "AppData"
            appdata_dir.mkdir(exist_ok=True)  # 如果目录不存在则创建

            # 配置文件路径 -> /AppData/settings.json
            config_file = appdata_dir / "settings.json"
            
            with open(config_file, "w", encoding='utf-8') as f:
                # 写入json中
                json.dump(settings, f, indent=4, ensure_ascii=False)
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
        self.volumeSlider.setValue(70)              # 音量70%
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


class SettingInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Setting")
        self.init_layout()

    def init_layout(self):
        layout = QVBoxLayout()
        self.settings_card = SettingsCard()
        layout.addWidget(self.settings_card)

        self.setLayout(layout)