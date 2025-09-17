from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from qfluentwidgets import InfoBar, InfoBarPosition
from PyQt5.QtCore import Qt
from pathlib import Path

class MusicManager(QObject):
    """音乐管理器类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.media_player = QMediaPlayer()
        self.setup_music()
    
    def setup_music(self):
        """设置音乐播放器"""
        try:
            # 获取音乐文件路径
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent
            music_file = project_root / "app" / "resource" / "music.mp3"
            
            if music_file.exists():
                # 设置音乐文件
                url = QUrl.fromLocalFile(str(music_file))
                content = QMediaContent(url)
                self.media_player.setMedia(content)
                
                # 设置循环播放
                self.media_player.setLoops(QMediaPlayer.Infinite)
                
                # 设置默认音量
                self.media_player.setVolume(70)
                print(f"音乐文件已加载: {music_file}")
            else:
                print(f"音乐文件不存在: {music_file}")
                
        except Exception as e:
            print(f"设置音乐播放器失败: {e}")
    
    def toggle_music(self, enabled):
        """切换音乐播放状态"""
        try:
            if enabled:
                self.media_player.play()
                print("开始播放音乐")
                if self.parent_widget:
                    InfoBar.success(
                        title='',
                        content="开始播放背景音乐",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self.parent_widget
                    )
            else:
                self.media_player.stop()
                print("停止播放音乐")
                if self.parent_widget:
                    InfoBar.success(
                        title='',
                        content="停止播放背景音乐",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self.parent_widget
                    )
        except Exception as e:
            print(f"切换音乐播放状态失败: {e}")
            if self.parent_widget:
                InfoBar.error(
                    title='',
                    content=f"音乐播放出错: {str(e)}",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self.parent_widget
                )
    
    def change_volume(self, value):
        """调整音量大小"""
        try:
            self.media_player.setVolume(value)
            print(f"音量调整为: {value}%")
        except Exception as e:
            print(f"调整音量失败: {e}")
    
    def set_volume(self, volume):
        """设置音量"""
        self.change_volume(volume)
    
    def play(self):
        """播放音乐"""
        self.toggle_music(True)
    
    def stop(self):
        """停止音乐"""
        self.toggle_music(False)
    
    def is_playing(self):
        """检查是否正在播放"""
        return self.media_player.state() == QMediaPlayer.PlayingState