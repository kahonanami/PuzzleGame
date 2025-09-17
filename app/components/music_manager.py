"""
音乐管理器
"""
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from qfluentwidgets.multimedia import SimpleMediaPlayBar
from qfluentwidgets import InfoBar, InfoBarPosition, TransparentToolButton, BodyLabel
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import QUrl
from pathlib import Path
import io
from mutagen import File
from mutagen.id3 import ID3NoHeaderError

# TODO: music manager模块目前比较混乱，后续有时间可以重构一下

class MusicCard(SimpleMediaPlayBar):
    """音乐播放卡片"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MusicCard")
        
        # 音乐文件路径
        # TODO: 1. 可以考虑把音乐文件路径改为配置项，方便替换音乐
        #       2. 可以考虑支持文件夹路径，循环播放文件夹内的音乐
        # 考虑到本项目只是一个简单的拼图游戏，音乐不属于主要内容，暂时不做复杂处理
        # 之后如果有时间，可以考虑添加更多功能，作为MusicCard的扩展
        self.music_path = Path("app/resource/music.mp3")
        url = QUrl.fromLocalFile(str(self.music_path.absolute()))
        self.player.setSource(url)
        
        # 读取音乐元数据，用于显示
        self.music_metadata = self.load_music_metadata()
        
        # 添加音乐信息显示
        self.setup_music_info()
        
        # 隐藏按钮
        self.hide_button = TransparentToolButton(FIF.PAGE_RIGHT, self)
        self.hide_button.setToolTip("收起音乐栏")
        self.hide_button.clicked.connect(self.hide_card)
        self.layout().addWidget(self.hide_button)

        # 显示按钮
        self.show_button = TransparentToolButton(FIF.PAGE_LEFT, self)
        self.show_button.setToolTip("展开音乐栏")
        self.show_button.clicked.connect(self.show_card)
        self.show_button.hide()
        self.layout().addWidget(self.show_button)
        
        # 记录原始大小
        self.original_size = (400, 60)
        self.collapsed_size = (40, 40)
    
    def load_music_metadata(self):
        """加载音乐文件的元数据"""
        metadata = {
            'title': 'Music',
            'artist': 'Unknown Artist',
            'album': 'Game Music',
            'cover_data': None
        }
        
        try:
            if self.music_path.exists():
                audio_file = File(str(self.music_path))
                if audio_file is not None:
                    # 获取标题
                    if 'TIT2' in audio_file:
                        metadata['title'] = str(audio_file['TIT2'])
                    elif 'TITLE' in audio_file:
                        metadata['title'] = str(audio_file['TITLE'][0])
                    
                    # 获取ARTIST
                    if 'TPE1' in audio_file:
                        metadata['artist'] = str(audio_file['TPE1'])
                    elif 'ARTIST' in audio_file:
                        metadata['artist'] = str(audio_file['ARTIST'][0])
                    
                    # 获取专辑
                    if 'TALB' in audio_file:
                        metadata['album'] = str(audio_file['TALB'])
                    elif 'ALBUM' in audio_file:
                        metadata['album'] = str(audio_file['ALBUM'][0])
                    
                    # 获取专辑封面
                    cover_data = None
                    if 'APIC:Cover' in audio_file:
                        cover_data = audio_file['APIC:Cover'].data
                    elif 'APIC:' in audio_file:
                        cover_data = audio_file['APIC:'].data
                    elif hasattr(audio_file, 'pictures') and audio_file.pictures:
                        cover_data = audio_file.pictures[0].data
                    
                    metadata['cover_data'] = cover_data
                        
                    # print(f"成功读取音乐元数据: {metadata['title']} - {metadata['artist']}")
                    
        except Exception as e:
            # print(f"读取音乐元数据失败: {e}")
            pass
        
        return metadata
    
    def setup_music_info(self):
        """设置音乐信息显示"""
        # 创建音乐信息容器
        self.music_info_widget = QWidget()
        self.music_info_layout = QHBoxLayout(self.music_info_widget)
        self.music_info_layout.setContentsMargins(5, 5, 5, 5)
        
        # 音乐封面图片
        self.album_cover = QLabel()
        self.album_cover.setFixedSize(40, 40)
        self.album_cover.setScaledContents(True)
        self.album_cover.setStyleSheet("""
            QLabel {
                border-radius: 5px;
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
            }
        """)
        
        # 设置专辑封面
        self.set_album_cover()
        
        # 音乐名称
        self.music_title = BodyLabel(self.music_metadata['title'])
        self.music_title.setStyleSheet("color: #333; font-weight: bold;")
        
        # Artist
        self.artist_name = BodyLabel(self.music_metadata['artist'])
        self.artist_name.setStyleSheet("color: #666; font-size: 11px;")
        
        # 文本信息布局
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        text_layout.addWidget(self.music_title)
        text_layout.addWidget(self.artist_name)
        
        text_widget = QWidget()
        text_widget.setLayout(text_layout)
        
        # 添加到音乐信息布局
        self.music_info_layout.addWidget(self.album_cover)
        self.music_info_layout.addWidget(text_widget)
        self.music_info_layout.addStretch()
        
        # 将音乐信息插入到最前面
        self.layout().insertWidget(0, self.music_info_widget)
    
    def set_album_cover(self):
        """设置专辑封面"""
        # 首先尝试使用MP3文件中的封面
        if self.music_metadata['cover_data']:
            try:
                pixmap = QPixmap()
                pixmap.loadFromData(self.music_metadata['cover_data'])
                if not pixmap.isNull():
                    self.album_cover.setPixmap(pixmap)
                    # print("使用MP3文件中的专辑封面")
                    return
            except Exception as e:
                # print(f"加载MP3封面失败: {e}")
                pass
        
        # 如果MP3中没有封面，使用头像图片
        cover_path = Path("app/resource/images/avatar.jpg")
        if cover_path.exists():
            pixmap = QPixmap(str(cover_path))
            self.album_cover.setPixmap(pixmap)
            # print("使用默认头像作为封面")
        else:
            # 使用默认图标
            self.album_cover.setText("♪")
            self.album_cover.setAlignment(Qt.AlignCenter)
            self.album_cover.setStyleSheet("""
                QLabel {
                    border-radius: 5px;
                    background-color: #e3f2fd;
                    border: 1px solid #bbdefb;
                    color: #1976d2;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            # print("使用默认音乐图标")

    def set_volume(self, volume):
        """设置音量"""
        self.player.setVolume(int(volume))  # 确保传入整数，不然会报错
        # print(f"音乐音量已设置为: {volume}%")

    def show_card(self):
        """展开音乐栏"""
        # 显示所有控件，除了展开按钮
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget and widget != self.show_button:
                widget.show()
        
        # 隐藏展开按钮
        self.show_button.hide()
        
        # 恢复原始大小
        self.setFixedSize(*self.original_size)
        
        # 计算并移动卡片到右下角
        window_width = self.parent().width()
        window_height = self.parent().height()
        card_width = self.width()
        card_height = self.height()
        
        x = window_width - card_width - 10
        y = window_height - card_height - 10
        self.move(x, y)

    def hide_card(self):
        """收起音乐栏"""
        # 隐藏所有控件，除了展开按钮
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget and widget != self.show_button:
                widget.hide()
        
        # 显示展开按钮
        self.show_button.show()

        # 调整为收起大小
        self.setFixedSize(*self.collapsed_size)

        # 计算并移动卡片到右下角
        window_width = self.parent().width()
        window_height = self.parent().height()
        card_width = self.width()
        card_height = self.height()

        x = window_width - card_width - 20
        y = window_height - card_height - 20
        self.move(x, y)
    
    def update_music_info(self, title="背景音乐", artist="拼图游戏"):
        """更新音乐信息"""
        self.music_title.setText(title)
        self.artist_name.setText(artist)

        # self._reposition()
    
    # def _reposition(self):
    #     """重新定位卡片"""
    #     self.parent().music_manager.reposition_music_card()

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
    
    # 项目中没有用到这个函数，因为SimpleMediaPlayBar自带音量调节，这里留作对外接口备用
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
                # 使用音乐卡片自己定义的原始大小
                self.music_card_widget.setFixedSize(*self.music_card_widget.original_size)
                
                # 设置音量
                self.music_card_widget.set_volume(self.current_volume)
                
                # 先隐藏卡片
                self.music_card_widget.hide()
                
                # 立即定位到正确位置
                self.position_music_card()
                
                # 然后显示卡片
                self.music_card_widget.show()
                
                # print("全局音乐播放器已启动")
                
            except Exception as e:
                # print(f"启动音乐播放器失败: {e}")
                pass
                pass
    
    def hide_music_card(self):
        """隐藏音乐卡片"""
        if self.music_card_widget:
            self.music_card_widget.hide()
            self.music_card_widget.deleteLater()
            self.music_card_widget = None
            # print("音乐播放器已关闭")
    
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
    
    # 后续函数留作对外接口备用
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