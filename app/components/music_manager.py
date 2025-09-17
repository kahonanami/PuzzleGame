"""
音乐管理器 - 封装所有音乐相关功能
"""
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget
from qfluentwidgets.multimedia import SimpleMediaPlayBar
from qfluentwidgets import InfoBar, InfoBarPosition
from PyQt5.QtCore import QUrl
from pathlib import Path


class MusicCard(SimpleMediaPlayBar):
    """音乐播放卡片"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MusicCard")
        url = QUrl.fromLocalFile(str(Path("app/resource/music.mp3").absolute()))
        self.player.setSource(url)
    
    def set_volume(self, volume):
        """设置音量"""
        if hasattr(self.player, 'setVolume'):
            self.player.setVolume(int(volume))  # 确保传入整数
            print(f"音乐音量已设置为: {volume}%")
        elif hasattr(self.player, 'audioOutput'):
            # 对于新版本的QMediaPlayer
            self.player.audioOutput().setVolume(volume / 100.0)
            print(f"音乐音量已设置为: {volume}%")
        else:
            print("无法设置音量：不支持的播放器类型")


class MusicManager(QObject):
    """全局音乐管理器"""
    
    # 定义信号
    musicToggled = pyqtSignal(bool)  # 音乐开关信号
    volumeChanged = pyqtSignal(int)  # 音量变化信号
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.music_card_widget = None
        self.is_enabled = False
        self.current_volume = 70  # 默认音量
    
    def toggle_music(self, enabled):
        """切换音乐开关"""
        self.is_enabled = enabled
        if enabled:
            self.show_music_card()
        else:
            self.hide_music_card()
        self.musicToggled.emit(enabled)
    
    def set_volume(self, volume):
        """设置音量"""
        self.current_volume = volume
        if self.music_card_widget:
            self.music_card_widget.set_volume(volume)
        self.volumeChanged.emit(volume)
    
    def show_music_card(self):
        """显示全局音乐卡片"""
        if self.music_card_widget is None:
            try:
                # 创建音乐播放器
                self.music_card_widget = MusicCard(self.parent_window)
                self.music_card_widget.setFixedSize(300, 50)
                
                # 设置音量
                self.music_card_widget.set_volume(self.current_volume)
                
                # 先隐藏卡片，避免闪烁
                self.music_card_widget.hide()
                
                # 立即定位到正确位置
                self.position_music_card()
                
                # 然后显示卡片
                self.music_card_widget.show()
                
                print("全局音乐播放器已启动")
                # InfoBar.success(
                #     title='',
                #     content=f"设置已重置为默认值",
                #     orient=Qt.Horizontal,
                #     isClosable=True,
                #     position=InfoBarPosition.TOP,
                #     duration=2000,
                #     parent=MainWindow.self
                # )
                
            except Exception as e:
                print(f"启动音乐播放器失败: {e}")
    
    def hide_music_card(self):
        """隐藏音乐卡片"""
        if self.music_card_widget:
            self.music_card_widget.hide()
            self.music_card_widget.deleteLater()
            self.music_card_widget = None
            print("音乐播放器已关闭")
    
    def position_music_card(self):
        """定位音乐卡片到右下角"""
        if self.music_card_widget and self.parent_window:
            # 获取主窗口的实际大小
            window_width = self.parent_window.width()
            window_height = self.parent_window.height()
            card_width = self.music_card_widget.width()
            card_height = self.music_card_widget.height()
            
            # 计算右下角位置
            x = window_width - card_width - 10
            y = window_height - card_height - 10
            
            self.music_card_widget.move(x, y)
    
    def reposition_music_card(self):
        """重新定位音乐卡片（用于窗口大小改变时）"""
        if self.music_card_widget and self.music_card_widget.isVisible():
            self.position_music_card()
    
    def is_music_enabled(self):
        """检查音乐是否启用"""
        return self.is_enabled
    
    def get_current_volume(self):
        """获取当前音量"""
        return self.current_volume
    
    def cleanup(self):
        """清理资源"""
        if self.music_card_widget:
            self.music_card_widget.deleteLater()
            self.music_card_widget = None