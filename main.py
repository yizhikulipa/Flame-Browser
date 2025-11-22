import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from browser_window import PyroBrowser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 强制设置应用字体
    app.setFont(QFont("Microsoft YaHei", 9))
    
    app.setApplicationName("烈焰浏览器")
    app.setApplicationVersion("2.1.0")
    
    browser = PyroBrowser()
    browser.show()
    
    sys.exit(app.exec_())
    