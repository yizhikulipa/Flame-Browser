import sys
import requests
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class UpdateChecker(QThread):
    """版本检查线程"""
    
    # 定义信号
    update_available = pyqtSignal(dict)  # 有新版本可用
    no_update = pyqtSignal()             # 已是最新版本
    check_failed = pyqtSignal(str)       # 检查失败
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timeout = 10  # 10秒超时
    
    def run(self):
        """执行版本检查"""
        try:
            # 模拟版本检查（实际使用时需要配置真实的URL）
            # 这里使用模拟数据来演示功能
            self.msleep(2000)  # 模拟网络延迟
            
            # 模拟版本信息（50%概率显示有更新）
            import random
            if random.random() > 0.5:
                # 模拟有新版本
                version_info = {
                    "latest_version": "2.2.0",
                    "release_date": "2024-12-15",
                    "download_url": "https://github.com/your-username/pyro-browser/releases/latest",
                    "changelog": "https://github.com/your-username/pyro-browser/blob/main/CHANGELOG.md",
                    "update_priority": "normal",
                    "changes": [
                        "新增：自动更新检查功能",
                        "优化：关于对话框滚动体验",
                        "修复：已知的性能问题",
                        "改进：标签页管理逻辑",
                        "增强：浏览器稳定性"
                    ]
                }
                self.update_available.emit(version_info)
            else:
                # 模拟已是最新版本
                self.no_update.emit()
                
        except Exception as e:
            self.check_failed.emit(f"检查更新时发生错误: {str(e)}")

class AuthorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        self.setWindowTitle("关于开发者")
        self.setFixedSize(500, 450)
        
        self.setStyleSheet("""
            QDialog {
                background: #202020;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            }
            QLabel {
                color: #ffffff;
                background: transparent;
                font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            }
            QPushButton {
                background: #0078d4;
                border: 1px solid #0078d4;
                border-radius: 6px;
                color: white;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: bold;
                margin: 6px;
                font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
                min-height: 18px;
            }
            QPushButton:hover {
                background: #106ebe;
                border-color: #106ebe;
            }
            QPushButton:pressed {
                background: #005a9e;
                border-color: #005a9e;
            }
            QPushButton.link-button {
                background: transparent;
                border: 1px solid #0078d4;
                color: #0078d4;
                padding: 8px 12px;
            }
            QPushButton.link-button:hover {
                background: rgba(0, 120, 212, 0.1);
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 25)
        layout.setSpacing(20)
        
        # 标题
        title_label = QLabel("👨‍💻 开发者信息")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 开发者头像和基本信息
        developer_info_layout = QHBoxLayout()
        
        # 头像区域
        avatar_label = QLabel("💻")
        avatar_label.setStyleSheet("font-size: 64px; margin-right: 20px;")
        avatar_label.setAlignment(Qt.AlignCenter)
        developer_info_layout.addWidget(avatar_label)
        
        # 基本信息
        info_layout = QVBoxLayout()
        name_label = QLabel("一只苦力怕")
        name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff; margin-bottom: 5px;")
        
        role_label = QLabel("全栈开发者 & 开源爱好者")
        role_label.setStyleSheet("font-size: 14px; color: #cccccc; margin-bottom: 10px;")
        
        desc_label = QLabel("专注于 Python 桌面应用开发，热爱开源技术，致力于创造优秀的用户体验。")
        desc_label.setStyleSheet("font-size: 13px; color: #aaaaaa; line-height: 1.5;")
        desc_label.setWordWrap(True)
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(role_label)
        info_layout.addWidget(desc_label)
        info_layout.addStretch()
        
        developer_info_layout.addLayout(info_layout)
        layout.addLayout(developer_info_layout)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background: #3c3c3c; margin: 15px 0;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        # 技术栈
        tech_label = QLabel("🛠️ 技术栈")
        tech_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; margin-bottom: 8px;")
        layout.addWidget(tech_label)
        
        tech_skills = QLabel(
            "Python • PyQt5 • QtWebEngine • JavaScript • HTML/CSS • \n"
            "Git • 开源项目维护 • 跨平台开发"
        )
        tech_skills.setStyleSheet("font-size: 13px; color: #cccccc; background: #2d2d2d; padding: 12px; border-radius: 6px; line-height: 1.6;")
        tech_skills.setWordWrap(True)
        layout.addWidget(tech_skills)
        
        # 联系按钮区域
        contact_layout = QHBoxLayout()
        
        bilibili_btn = QPushButton("📺 B站主页")
        bilibili_btn.setCursor(Qt.PointingHandCursor)
        bilibili_btn.clicked.connect(self.open_bilibili)
        bilibili_btn.setStyleSheet("QPushButton { background: #fb7299; border-color: #fb7299; } QPushButton:hover { background: #ff8ab0; }")
        
        github_btn = QPushButton("🐙 GitHub")
        github_btn.setCursor(Qt.PointingHandCursor)
        github_btn.clicked.connect(self.open_github)
        github_btn.setStyleSheet("QPushButton { background: #333; border-color: #333; } QPushButton:hover { background: #555; }")
        
        qq_btn = QPushButton("💬 技术交流")
        qq_btn.setCursor(Qt.PointingHandCursor)
        qq_btn.clicked.connect(self.join_qq)
        
        contact_layout.addWidget(bilibili_btn)
        contact_layout.addWidget(github_btn)
        contact_layout.addWidget(qq_btn)
        layout.addLayout(contact_layout)
        
        layout.addStretch()
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setFixedHeight(35)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def open_bilibili(self):
        """打开B站主页"""
        if self.parent_browser:
            self.parent_browser.add_new_tab("https://space.bilibili.com/3546690835449884", "B站主页")
        self.close()
    
    def open_github(self):
        """打开GitHub"""
        if self.parent_browser:
            self.parent_browser.add_new_tab("https://github.com", "GitHub")
        self.close()
    
    def join_qq(self):
        """打开QQ群"""
        if self.parent_browser:
            self.parent_browser.add_new_tab("https://qm.qq.com/q/fCm6i05bFK", "技术交流群")
        self.close()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_browser = parent
        self.setWindowTitle("关于烈焰浏览器")
        self.setFixedSize(700, 600)
        
        # 版本检查器
        self.update_checker = None
        
        self.setStyleSheet("""
            QDialog {
                background: #202020;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            }
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 14px;
                margin: 0px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #5e5e5e;
                border-radius: 7px;
                min-height: 30px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #707070;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QLabel {
                color: #ffffff;
                background: transparent;
                font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            }
            QPushButton {
                background: #0078d4;
                border: 1px solid #0078d4;
                border-radius: 4px;
                color: white;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: bold;
                font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
                min-height: 18px;
            }
            QPushButton:hover {
                background: #106ebe;
                border-color: #106ebe;
            }
            QPushButton:pressed {
                background: #005a9e;
                border-color: #005a9e;
            }
            QPushButton:disabled {
                background: #5e5e5e;
                border-color: #5e5e5e;
                color: #aaaaaa;
            }
            QPushButton.update-available {
                background: #107c10;
                border-color: #107c10;
            }
            QPushButton.update-available:hover {
                background: #0d6b0d;
                border-color: #0d6b0d;
            }
            QProgressBar {
                border: none;
                background: #2d2d2d;
                border-radius: 4px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d4, stop:1 #00bcf2);
                border-radius: 4px;
            }
            QFrame.section {
                background: #2d2d2d;
                border-radius: 8px;
                border: 1px solid #3c3c3c;
            }
            QFrame.feature-card {
                background: #2d2d2d;
                border-radius: 8px;
                border: 1px solid #3c3c3c;
                padding: 0px;
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏（仿Edge）
        title_bar = QWidget()
        title_bar.setFixedHeight(45)
        title_bar.setStyleSheet("background: #2d2d2d; border-top-left-radius: 8px; border-top-right-radius: 8px;")
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 20, 0)
        
        title_label = QLabel("关于烈焰浏览器")
        title_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # 关闭按钮
        close_btn = QPushButton("×")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
                color: #cccccc;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #e81123;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
        
        main_layout.addWidget(title_bar)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 创建滚动内容部件
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: #202020;")
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(30, 25, 30, 25)
        content_layout.setSpacing(20)
        
        # === 浏览器头部信息 ===
        header_layout = QHBoxLayout()
        
        # 浏览器图标
        icon_frame = QFrame()
        icon_frame.setFixedSize(80, 80)
        icon_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff6b35, stop:1 #ff8e53); 
            border-radius: 12px;
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_label = QLabel("🌋")
        icon_label.setStyleSheet("font-size: 40px;")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        header_layout.addWidget(icon_frame)
        header_layout.addSpacing(20)
        
        # 名称和版本信息
        name_layout = QVBoxLayout()
        name_label = QLabel("烈焰浏览器")
        name_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff; margin-bottom: 5px;")
        
        version_label = QLabel("版本 2.1.0")
        version_label.setStyleSheet("font-size: 16px; color: #cccccc; margin-bottom: 8px;")
        
        # 版本特性标签
        version_badge = QLabel("🚀 最新稳定版")
        version_badge.setStyleSheet("""
            background: #0078d4;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        """)
        version_badge.setAlignment(Qt.AlignCenter)
        version_badge.setFixedWidth(120)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(version_label)
        name_layout.addWidget(version_badge)
        name_layout.addStretch()
        
        header_layout.addLayout(name_layout)
        header_layout.addStretch()
        
        content_layout.addLayout(header_layout)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background: #3c3c3c; margin: 10px 0;")
        separator.setFixedHeight(1)
        content_layout.addWidget(separator)
        
        # === 浏览器简介 ===
        intro_frame = QFrame()
        intro_frame.setProperty("class", "section")
        intro_frame.setStyleSheet("QFrame.section { padding: 20px; }")
        intro_layout = QVBoxLayout(intro_frame)
        
        intro_label = QLabel("📖 浏览器简介")
        intro_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin-bottom: 12px;")
        intro_layout.addWidget(intro_label)
        
        intro_text = QLabel(
            "烈焰浏览器是一款基于 PyQt5 和 QtWebEngine 构建的现代化网络浏览器。"
            "它融合了先进的 Web 技术和优雅的用户界面设计，为用户提供快速、安全、"
            "流畅的网页浏览体验。\n\n"
            "浏览器采用深色主题设计，支持多标签页管理、智能地址栏、丰富的快捷键"
            "等特性，是日常上网和开发的理想选择。"
        )
        intro_text.setStyleSheet("font-size: 14px; color: #cccccc; line-height: 1.6;")
        intro_text.setWordWrap(True)
        intro_layout.addWidget(intro_text)
        
        content_layout.addWidget(intro_frame)
        
        # === 主要特性 ===
        features_label = QLabel("✨ 主要特性")
        features_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin: 10px 0 15px 0;")
        content_layout.addWidget(features_label)
        
        # 创建特性网格布局
        features_grid = QGridLayout()
        features_grid.setSpacing(15)
        features_grid.setHorizontalSpacing(15)
        
        features = [
            ("🚀", "极速浏览", "基于 Chromium 内核，网页加载快速流畅，性能优异"),
            ("🎨", "现代化界面", "深色主题设计，护眼舒适，支持自定义主题"),
            ("📑", "多标签页", "支持无限标签页，拖拽排序，智能标签管理"),
            ("⌨️", "智能地址栏", "支持搜索建议、网址自动补全和历史记录"),
            ("⚡", "流畅动画", "标签页切换和页面加载都有平滑过渡动画"),
            ("🔒", "隐私保护", "内置隐私保护功能，清除浏览数据，安全浏览"),
            ("🌐", "跨平台支持", "支持 Windows、macOS、Linux 等多个平台"),
            ("🎯", "高效快捷键", "完整的键盘快捷键支持，提高操作效率"),
            ("🔄", "实时刷新", "支持页面刷新、强制刷新和停止加载"),
            ("📱", "响应式设计", "完美适配各种网页和屏幕尺寸"),
            ("🎵", "媒体支持", "完整支持音视频播放，高清流畅"),
            ("🔧", "开发者工具", "内置开发者工具，便于网页调试和开发")
        ]
        
        for i, (icon, title, desc) in enumerate(features):
            feature_frame = QFrame()
            feature_frame.setProperty("class", "feature-card")
            feature_frame.setStyleSheet("QFrame.feature-card { background: #2d2d2d; border-radius: 8px; border: 1px solid #3c3c3c; }")
            feature_layout = QVBoxLayout(feature_frame)
            feature_layout.setContentsMargins(15, 15, 15, 15)
            feature_layout.setSpacing(8)
            
            # 图标和标题
            title_layout = QHBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 18px; margin-right: 8px;")
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
            
            title_layout.addWidget(icon_label)
            title_layout.addWidget(title_label)
            title_layout.addStretch()
            
            # 描述
            desc_label = QLabel(desc)
            desc_label.setStyleSheet("font-size: 12px; color: #aaaaaa; line-height: 1.4;")
            desc_label.setWordWrap(True)
            desc_label.setMinimumHeight(35)
            
            feature_layout.addLayout(title_layout)
            feature_layout.addWidget(desc_label)
            
            row, col = i // 3, i % 3
            features_grid.addWidget(feature_frame, row, col)
        
        content_layout.addLayout(features_grid)
        
        # === 系统信息 ===
        sysinfo_frame = QFrame()
        sysinfo_frame.setProperty("class", "section")
        sysinfo_frame.setStyleSheet("QFrame.section { padding: 20px; }")
        sysinfo_layout = QVBoxLayout(sysinfo_frame)
        
        sysinfo_label = QLabel("💻 系统信息")
        sysinfo_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin-bottom: 15px;")
        sysinfo_layout.addWidget(sysinfo_label)
        
        # 系统信息网格
        sysinfo_grid = QGridLayout()
        sysinfo_grid.setHorizontalSpacing(25)
        sysinfo_grid.setVerticalSpacing(10)
        
        sys_info = [
            ("Python 版本:", f"{sys.version.split()[0]}"),
            ("Qt 版本:", f"{QT_VERSION_STR}"),
            ("PyQt 版本:", f"{PYQT_VERSION_STR}"),
            ("Chromium 版本:", "基于 QtWebEngine (Chromium 87+)"),
            ("构建时间:", "2024年12月"),
            ("运行平台:", f"{sys.platform.title()}"),
            ("架构:", "64位" if sys.maxsize > 2**32 else "32位")
        ]
        
        for i, (key, value) in enumerate(sys_info):
            key_label = QLabel(key)
            key_label.setStyleSheet("font-size: 13px; color: #cccccc; font-weight: bold; min-width: 120px;")
            value_label = QLabel(value)
            value_label.setStyleSheet("font-size: 13px; color: #ffffff;")
            
            sysinfo_grid.addWidget(key_label, i, 0)
            sysinfo_grid.addWidget(value_label, i, 1)
        
        sysinfo_layout.addLayout(sysinfo_grid)
        content_layout.addWidget(sysinfo_frame)
        
        # === 版本信息区域 ===
        version_frame = QFrame()
        version_frame.setProperty("class", "section")
        version_frame.setStyleSheet("QFrame.section { padding: 20px; }")
        version_layout = QVBoxLayout(version_frame)
        
        version_label = QLabel("🔄 版本信息")
        version_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; margin-bottom: 15px;")
        version_layout.addWidget(version_label)
        
        # 版本信息网格
        version_grid = QGridLayout()
        version_grid.setHorizontalSpacing(25)
        version_grid.setVerticalSpacing(10)
        
        version_info = [
            ("当前版本:", "2.1.0"),
            ("发布日期:", "2025-11-22"),
            ("检查状态:", "点击检查更新按钮查看")
        ]
        
        for i, (key, value) in enumerate(version_info):
            key_label = QLabel(key)
            key_label.setStyleSheet("font-size: 13px; color: #cccccc; font-weight: bold; min-width: 120px;")
            value_label = QLabel(value)
            value_label.setStyleSheet("font-size: 13px; color: #ffffff;")
            
            version_grid.addWidget(key_label, i, 0)
            version_grid.addWidget(value_label, i, 1)
        
        version_layout.addLayout(version_grid)
        
        # 更新检查进度条
        self.update_progress = QProgressBar()
        self.update_progress.setVisible(False)
        self.update_progress.setRange(0, 0)  # 无限进度条
        self.update_progress.setFixedHeight(6)
        version_layout.addWidget(self.update_progress)
        
        content_layout.addWidget(version_frame)
        
        # === 底部按钮区域 ===
        button_layout = QHBoxLayout()
        
        # 开发者信息按钮
        author_btn = QPushButton("👨‍💻 开发者信息")
        author_btn.setCursor(Qt.PointingHandCursor)
        author_btn.clicked.connect(self.show_author_info)
        author_btn.setFixedHeight(35)
        
        # 检查更新按钮
        self.update_btn = QPushButton("🔄 检查更新")
        self.update_btn.setCursor(Qt.PointingHandCursor)
        self.update_btn.clicked.connect(self.check_updates)
        self.update_btn.setFixedHeight(35)
        
        button_layout.addWidget(author_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.update_btn)
        
        content_layout.addLayout(button_layout)
        
        # === 版权信息 ===
        copyright_label = QLabel("© 2025 烈焰浏览器")
        copyright_label.setStyleSheet("font-size: 12px; color: #666666; margin-top: 20px;")
        copyright_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(copyright_label)
        
        # 添加弹性空间确保内容可以滚动
        content_layout.addStretch()
        
        # 设置滚动区域的内容
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def check_updates(self):
        """检查更新"""
        self.update_btn.setEnabled(False)
        self.update_btn.setText("检查中...")
        self.update_progress.setVisible(True)
        
        # 创建并启动更新检查线程
        self.update_checker = UpdateChecker(self)
        self.update_checker.update_available.connect(self.on_update_available)
        self.update_checker.no_update.connect(self.on_no_update)
        self.update_checker.check_failed.connect(self.on_check_failed)
        self.update_checker.start()
    
    def on_update_available(self, version_info):
        """有新版本可用"""
        self.update_progress.setVisible(False)
        self.update_btn.setEnabled(True)
        self.update_btn.setText("🎉 下载更新")
        self.update_btn.setProperty("class", "update-available")
        self.update_btn.setStyleSheet("QPushButton { background: #107c10; border-color: #107c10; } QPushButton:hover { background: #0d6b0d; }")
        self.update_btn.clicked.disconnect()
        self.update_btn.clicked.connect(lambda: self.download_update(version_info))
        
        # 显示更新信息对话框
        self.show_update_info(version_info)
    
    def on_no_update(self):
        """已是最新版本"""
        self.update_progress.setVisible(False)
        self.update_btn.setEnabled(True)
        self.update_btn.setText("✅ 已是最新版本")
        self.update_btn.setStyleSheet("")
        
        QMessageBox.information(self, "检查更新", 
            f"✅ 您的浏览器已是最新版本！\n\n"
            f"当前版本: 2.1.0\n"
            f"发布日期: 2024-12-01"
        )
    
    def on_check_failed(self, error_message):
        """检查更新失败"""
        self.update_progress.setVisible(False)
        self.update_btn.setEnabled(True)
        self.update_btn.setText("🔄 检查更新")
        self.update_btn.setStyleSheet("")
        
        QMessageBox.warning(self, "检查更新", 
            f"❌ 检查更新失败\n\n"
            f"错误信息: {error_message}\n\n"
            f"请检查网络连接或稍后重试。"
        )
    
    def show_update_info(self, version_info):
        """显示更新信息"""
        latest_version = version_info.get('latest_version', '未知')
        release_date = version_info.get('release_date', '未知')
        download_url = version_info.get('download_url', '#')
        changes = version_info.get('changes', [])
        
        # 创建更新信息对话框
        update_dialog = QDialog(self)
        update_dialog.setWindowTitle("发现新版本")
        update_dialog.setFixedSize(500, 400)
        update_dialog.setStyleSheet("""
            QDialog {
                background: #202020;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
                font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            }
            QLabel {
                color: #ffffff;
                background: transparent;
            }
            QPushButton {
                background: #0078d4;
                border: 1px solid #0078d4;
                border-radius: 4px;
                color: white;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #106ebe;
            }
            QPushButton.download-btn {
                background: #107c10;
                border-color: #107c10;
            }
            QPushButton.download-btn:hover {
                background: #0d6b0d;
            }
        """)
        
        layout = QVBoxLayout(update_dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("🎉 发现新版本！")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 版本信息
        version_layout = QHBoxLayout()
        current_version_label = QLabel(f"当前版本: 2.1.0")
        current_version_label.setStyleSheet("font-size: 14px; color: #cccccc;")
        
        arrow_label = QLabel("→")
        arrow_label.setStyleSheet("font-size: 16px; color: #0078d4; font-weight: bold; margin: 0 10px;")
        
        new_version_label = QLabel(f"最新版本: {latest_version}")
        new_version_label.setStyleSheet("font-size: 14px; color: #4caf50; font-weight: bold;")
        
        version_layout.addWidget(current_version_label)
        version_layout.addWidget(arrow_label)
        version_layout.addWidget(new_version_label)
        version_layout.addStretch()
        layout.addLayout(version_layout)
        
        # 更新内容
        changes_label = QLabel("📝 更新内容:")
        changes_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff; margin-top: 10px;")
        layout.addWidget(changes_label)
        
        changes_text = QTextEdit()
        changes_text.setReadOnly(True)
        changes_text.setStyleSheet("""
            QTextEdit {
                background: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 6px;
                padding: 10px;
                color: #cccccc;
                font-size: 13px;
            }
        """)
        
        changes_html = "<ul style='margin: 0; padding-left: 20px;'>"
        for change in changes:
            changes_html += f"<li style='margin-bottom: 5px;'>{change}</li>"
        changes_html += "</ul>"
        
        changes_text.setHtml(changes_html)
        changes_text.setFixedHeight(150)
        layout.addWidget(changes_text)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        later_btn = QPushButton("稍后提醒")
        later_btn.clicked.connect(update_dialog.close)
        
        download_btn = QPushButton("立即下载")
        download_btn.setProperty("class", "download-btn")
        download_btn.setStyleSheet("QPushButton { background: #107c10; border-color: #107c10; } QPushButton:hover { background: #0d6b0d; }")
        download_btn.clicked.connect(lambda: self.download_update(version_info))
        
        button_layout.addWidget(later_btn)
        button_layout.addStretch()
        button_layout.addWidget(download_btn)
        
        layout.addLayout(button_layout)
        
        update_dialog.exec_()
    
    def download_update(self, version_info):
        """下载更新"""
        download_url = version_info.get('download_url', '#')
        
        # 在浏览器中打开下载页面
        if self.parent_browser and download_url != '#':
            self.parent_browser.add_new_tab(download_url, "下载更新")
        
        QMessageBox.information(self, "下载更新", 
            "已在浏览器中打开下载页面。\n"
            "请下载最新版本并安装。"
        )
        
        # 重置更新按钮状态
        self.update_btn.setText("🔄 检查更新")
        self.update_btn.setStyleSheet("")
        self.update_btn.clicked.disconnect()
        self.update_btn.clicked.connect(self.check_updates)
    
    def show_author_info(self):
        """显示作者信息对话框"""
        author_dialog = AuthorDialog(self.parent_browser)
        author_dialog.exec_()
