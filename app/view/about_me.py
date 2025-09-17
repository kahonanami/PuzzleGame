from qfluentwidgets import (
    CardWidget, AvatarWidget, SubtitleLabel, BodyLabel, 
    HyperlinkButton, IconWidget, FluentIcon as FIF,
    PrimaryPushButton, InfoBar, InfoBarPosition
)
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, 
    QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QDesktopServices
import webbrowser

class AboutMeInterface(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("AboutMeInterface")
        self.initUI()
        
    def initUI(self):
        # 主布局
        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(30)
        mainLayout.setContentsMargins(40, 40, 40, 40)
        
        # 设置页面样式
        self.setStyleSheet("""
            AboutMeInterface {
                background-color: transparent;
            }
            CardWidget {
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        
        # 主卡片
        self.createProfileCard(mainLayout)
        
        # 个人信息
        self.createInfoCard(mainLayout)
        
        # 联系方式
        self.createContactCard(mainLayout)
        
        # 添加弹性空间
        mainLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
    def createProfileCard(self, mainLayout):
        """创建个人资料卡片"""
        profileCard = CardWidget()
        profileCard.setFixedHeight(200)
        profileLayout = QHBoxLayout(profileCard)
        profileLayout.setContentsMargins(30, 20, 30, 20)
        
        # 头像
        avatar = AvatarWidget("app/resource/images/avatar.jpg")
        avatar.setRadius(80)
        avatar.setFixedSize(160, 160)
        profileLayout.addWidget(avatar)
        
        # 个人信息
        infoLayout = QVBoxLayout()
        infoLayout.setSpacing(15)
        
        # 姓名
        nameLabel = SubtitleLabel("Azusaq")
        nameLabel.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        infoLayout.addWidget(nameLabel)
        
        # 角色
        roleLabel = BodyLabel("🛡️ 信息安全专业 | 网络安全爱好者")
        roleLabel.setStyleSheet("color: #606060; font-size: 14px;")
        infoLayout.addWidget(roleLabel)
        
        # 座右铭
        mottoLabel = BodyLabel("✨\"无法触及，因而耀眼\"✨")
        mottoLabel.setStyleSheet("color: #0078d4; font-style: italic; font-size: 13px;")
        infoLayout.addWidget(mottoLabel)
        
        # GitHub按钮
        githubButton = PrimaryPushButton(FIF.GITHUB, "访问我的 GitHub")
        githubButton.clicked.connect(self.openGitHub)
        githubButton.setFixedWidth(200)
        infoLayout.addWidget(githubButton)
        
        infoLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        profileLayout.addLayout(infoLayout)
        mainLayout.addWidget(profileCard)
        
    def createInfoCard(self, mainLayout):
        """创建基本信息卡片"""
        infoCard = CardWidget()
        infoLayout = QVBoxLayout(infoCard)
        infoLayout.setContentsMargins(30, 20, 30, 20)
        
        # 标题
        titleLabel = SubtitleLabel("📊 关于我")
        titleLabel.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        infoLayout.addWidget(titleLabel)
        
        # 信息项
        infoItems = [
            ("🎓 专业", "信息安全"),
            ("💻 主要语言", "C/C++, Python"),
            ("🔧 开发工具", "Ubuntu，VS Code，Git"),
            ("🔒 兴趣爱好", "网络安全，二进制安全"),
            ("📚 学习方向", "网络安全，操作系统，二进制分析")
        ]
        
        for label, value in infoItems:
            itemLayout = QHBoxLayout()
            labelWidget = BodyLabel(label)
            labelWidget.setFixedWidth(120)
            labelWidget.setStyleSheet("font-weight: bold; color: #333;")
            valueWidget = BodyLabel(value)
            valueWidget.setStyleSheet("color: #606060;")
            
            itemLayout.addWidget(labelWidget)
            itemLayout.addWidget(valueWidget)
            itemLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
            
            infoLayout.addLayout(itemLayout)
            
        mainLayout.addWidget(infoCard)
        
    def createContactCard(self, mainLayout):
        """创建联系方式卡片"""
        contactCard = CardWidget()
        contactLayout = QVBoxLayout(contactCard)
        contactLayout.setContentsMargins(30, 20, 30, 20)
        
        # 标题
        titleLabel = SubtitleLabel("📞 联系方式")
        titleLabel.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        contactLayout.addWidget(titleLabel)
        
        # 联系方式按钮
        buttonsLayout = QHBoxLayout()
        
        # GitHub按钮
        githubBtn = PrimaryPushButton(FIF.GITHUB, "GitHub")
        githubBtn.clicked.connect(self.openGitHub)
        githubBtn.setFixedSize(120, 40)
        
        # 邮箱按钮
        emailBtn = PrimaryPushButton(FIF.MAIL, "Email")
        emailBtn.clicked.connect(self.openEmail)
        emailBtn.setFixedSize(120, 40)
        
        # QQ按钮
        qqBtn = PrimaryPushButton(FIF.PEOPLE, "QQ")
        qqBtn.clicked.connect(self.showQQ)
        qqBtn.setFixedSize(120, 40)
        
        # 项目按钮
        projectBtn = PrimaryPushButton(FIF.FOLDER, "关于本项目")
        projectBtn.clicked.connect(self.showProjects)
        projectBtn.setFixedSize(120, 40)
        
        buttonsLayout.addWidget(githubBtn)
        buttonsLayout.addWidget(emailBtn)
        buttonsLayout.addWidget(qqBtn)
        buttonsLayout.addWidget(projectBtn)
        buttonsLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        contactLayout.addLayout(buttonsLayout)
        
        # 感谢信息
        # thankLabel = BodyLabel("🙏 感谢使用我的拼图游戏！")
        # thankLabel.setAlignment(Qt.AlignCenter)
        # thankLabel.setStyleSheet("color: #0078d4; font-size: 14px; margin-top: 20px;")
        # contactLayout.addWidget(thankLabel)
        
        mainLayout.addWidget(contactCard)
        
    def openGitHub(self):
        """打开GitHub页面"""
        try:
            webbrowser.open("https://github.com/kahonanami")
        except:
            InfoBar.error(
                title="错误",
                content="无法打开浏览器",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            
    def openEmail(self):
        """打开邮箱"""
        try:
            webbrowser.open("mailto:azusaq@qq.com")
        except:
            InfoBar.info(
                title="提示",
                content="请手动复制邮箱地址：azusaq@qq.com",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            
    def showQQ(self):
        """显示QQ信息"""
        InfoBar.info(
            title="QQ联系方式",
            content="QQ号：3523457454",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=4000,
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