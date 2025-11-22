import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QKeySequence

from tab_widget import AnimatedTabWidget
from web_view import FadeWebEngineView
from dialogs import AboutDialog, AuthorDialog
from styles import get_main_window_style, get_toolbar_button_style, get_url_bar_style

class PyroBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("烈焰浏览器")
        self.setGeometry(100, 100, 1400, 900)
        
        # 设置Edge风格的深色主题
        self.set_modern_dark_theme()
        
        # 创建动画标签页系统
        self.tab_widget = AnimatedTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # 创建第一个标签页
        self.add_new_tab("https://www.bing.com", "必应首页")
        
        # 创建现代化的地址栏
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("在必应中搜索或输入网址")
        self.url_bar.setStyleSheet(get_url_bar_style())
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        # 创建现代化的导航按钮
        后退按钮 = self.create_styled_button("←", "后退")
        后退按钮.clicked.connect(self.go_back)
        
        前进按钮 = self.create_styled_button("→", "前进")
        前进按钮.clicked.connect(self.go_forward)
        
        刷新按钮 = self.create_styled_button("↻", "刷新")
        刷新按钮.clicked.connect(self.reload_page)
        
        主页按钮 = self.create_styled_button("🏠", "主页")
        主页按钮.clicked.connect(self.navigate_home)
        
        # 创建搜索按钮
        搜索按钮 = self.create_styled_button("🔍", "搜索")
        搜索按钮.clicked.connect(self.navigate_to_url)
        
        # 创建进度条
        self.progress = QProgressBar()
        self.progress.setMaximumHeight(3)
        self.progress.setVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background: transparent;
                border-radius: 0px;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d4, stop:1 #00bcf2
                );
                border-radius: 0px;
            }
        """)
        
        # 创建新标签页按钮
        新标签按钮 = self.create_styled_button("+", "新建标签页")
        新标签按钮.clicked.connect(lambda: self.add_new_tab("https://www.bing.com", "新标签页"))
        
        # 创建网页关闭按钮
        关闭网页按钮 = self.create_styled_button("✕", "关闭当前网页")
        关闭网页按钮.clicked.connect(self.close_current_tab)
        
        # 创建关于按钮
        关于按钮 = self.create_styled_button("💬", "关于")
        关于按钮.clicked.connect(self.show_about)
        
        # 创建工具栏
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background: #2d2d2d;
                border: none;
                border-bottom: 1px solid #3c3c3c;
                padding: 6px 8px;
                spacing: 4px;
            }
        """)
        self.addToolBar(toolbar)
        
        # 添加组件到工具栏
        toolbar.addWidget(后退按钮)
        toolbar.addWidget(前进按钮)
        toolbar.addWidget(刷新按钮)
        toolbar.addWidget(主页按钮)
        toolbar.addSeparator()
        toolbar.addWidget(self.url_bar)
        toolbar.addWidget(搜索按钮)
        toolbar.addSeparator()
        toolbar.addWidget(新标签按钮)
        toolbar.addWidget(关闭网页按钮)  # 添加关闭网页按钮
        toolbar.addSeparator()
        
        # 添加弹性空间，将关于按钮推到最右边
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        toolbar.addWidget(关于按钮)
        
        # 设置布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(toolbar)
        layout.addWidget(self.progress)
        layout.addWidget(self.tab_widget)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # 连接信号
        self.tab_widget.currentChanged.connect(self.tab_changed)
        
        # 添加快捷键
        self.setup_shortcuts()
        
    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()
        
    def create_styled_button(self, text, tooltip):
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.setFixedSize(32, 32)
        btn.setStyleSheet(get_toolbar_button_style())
        return btn
    
    def create_browser_tab(self, url="https://www.bing.com"):
        browser = FadeWebEngineView()
        
        # 设置网页的字体和样式
        settings = browser.settings()
        settings.setFontFamily(QWebEngineSettings.StandardFont, "Microsoft YaHei")
        settings.setFontFamily(QWebEngineSettings.SerifFont, "Microsoft YaHei")
        settings.setFontFamily(QWebEngineSettings.SansSerifFont, "Microsoft YaHei")
        settings.setFontSize(QWebEngineSettings.DefaultFontSize, 14)
        
        browser.setUrl(QUrl(url))
        browser.urlChanged.connect(self.update_urlbar)
        browser.loadFinished.connect(self.page_loaded)
        browser.loadProgress.connect(self.update_progress)
        browser.titleChanged.connect(self.update_window_title)
        return browser
    
    def add_new_tab(self, url="https://www.bing.com", title="新标签页"):
        browser = self.create_browser_tab(url)
        index = self.tab_widget.addTab(browser, title)
        self.tab_widget.setCurrentIndexWithAnimation(index)
        return browser
    
    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
        else:
            self.close()
    
    def close_current_tab(self):
        """关闭当前标签页"""
        current_index = self.tab_widget.currentIndex()
        self.close_tab(current_index)
    
    def tab_changed(self, index):
        if index >= 0:
            browser = self.tab_widget.widget(index)
            if browser:
                self.update_urlbar(browser.url())
                title = browser.page().title()
                self.update_window_title(title)
    
    def update_window_title(self, title):
        if title:
            title = title.replace('\n', ' ').strip()
            if len(title) > 30:
                title = title[:30] + "..."
            self.setWindowTitle(f"{title} - 烈焰浏览器")
        else:
            self.setWindowTitle("烈焰浏览器")
    
    def go_back(self):
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.back()
    
    def go_forward(self):
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.forward()
    
    def reload_page(self):
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.reload()
    
    def previous_tab(self):
        current_index = self.tab_widget.currentIndex()
        new_index = (current_index - 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndexWithAnimation(new_index)
    
    def next_tab(self):
        current_index = self.tab_widget.currentIndex()
        new_index = (current_index + 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndexWithAnimation(new_index)
    
    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        
        current_url = self.get_current_url()
        if current_url and 'bilibili.com' in current_url and not url.startswith(('http://', 'https://')):
            if '.' not in url:
                search_url = f'https://search.bilibili.com/all?keyword={url.replace(" ", "+")}'
                self.load_url_in_current_tab(search_url)
                return
        
        if not url.startswith(('http://', 'https://')):
            if '.' in url:
                url = 'https://' + url
            else:
                url = f'https://www.bing.com/search?q={url.replace(" ", "+")}'
        
        self.load_url_in_current_tab(url)
    
    def get_current_url(self):
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            return current_browser.url().toString()
        return ""
    
    def load_url_in_current_tab(self, url):
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))
    
    def navigate_home(self):
        self.load_url_in_current_tab("https://www.bing.com")
    
    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)
        
        current_browser = self.tab_widget.currentWidget()
        if current_browser:
            title = current_browser.page().title()
            if title:
                显示标题 = title[:20] + "..." if len(title) > 20 else title
                current_index = self.tab_widget.currentIndex()
                self.tab_widget.setTabText(current_index, 显示标题)
    
    def page_loaded(self):
        self.progress.setVisible(False)
        self.statusBar().showMessage("页面加载完成", 2000)
    
    def update_progress(self, progress):
        self.progress.setValue(progress)
        self.progress.setVisible(progress < 100)
    
    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+R"), self).activated.connect(self.reload_page)
        QShortcut(QKeySequence("Ctrl+T"), self).activated.connect(
            lambda: self.add_new_tab("https://www.bing.com", "新标签页"))
        QShortcut(QKeySequence("Ctrl+L"), self).activated.connect(self.focus_urlbar)
        QShortcut(QKeySequence("Ctrl+W"), self).activated.connect(self.close_current_tab)
        QShortcut(QKeySequence("F5"), self).activated.connect(self.reload_page)
        QShortcut(QKeySequence("Ctrl+Tab"), self).activated.connect(self.next_tab)
        QShortcut(QKeySequence("Ctrl+Shift+Tab"), self).activated.connect(self.previous_tab)
        QShortcut(QKeySequence("F1"), self).activated.connect(self.show_about)
    
    def focus_urlbar(self):
        self.url_bar.selectAll()
        self.url_bar.setFocus()
    
    def set_modern_dark_theme(self):
        self.setStyleSheet(get_main_window_style())
        