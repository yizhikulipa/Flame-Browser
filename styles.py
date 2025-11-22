def get_main_window_style():
    return """
        QMainWindow {
            background: #202020;
            color: #ffffff;
        }
        QTabWidget::pane {
            border: none;
            background: #202020;
        }
        QTabBar::tab {
            background: #2d2d2d;
            color: #cccccc;
            padding: 8px 16px;
            margin-right: 1px;
            border: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
        }
        QTabBar::tab:selected {
            background: #202020;
            color: #ffffff;
            border-bottom: 2px solid #0078d4;
        }
        QTabBar::tab:hover {
            background: #3c3c3c;
        }
        QTabBar::tab:!selected {
            margin-top: 2px;
        }
        QTabBar::close-button {
            image: url(none);
            subcontrol-position: right;
        }
        QStatusBar {
            background: #2d2d2d;
            color: #cccccc;
            border-top: 1px solid #3c3c3c;
        }
    """

def get_toolbar_button_style():
    return """
        QPushButton {
            background: transparent;
            border: 1px solid transparent;
            border-radius: 4px;
            color: #cccccc;
            font-size: 14px;
            font-weight: normal;
        }
        QPushButton:hover {
            background: #3c3c3c;
            border-color: #5e5e5e;
        }
        QPushButton:pressed {
            background: #5e5e5e;
        }
        QPushButton:disabled {
            color: #666666;
        }
    """

def get_url_bar_style():
    return """
        QLineEdit {
            padding: 6px 12px;
            border: 1px solid #5e5e5e;
            border-radius: 20px;
            background: #2d2d2d;
            color: #ffffff;
            font-size: 14px;
            margin: 0 5px;
            font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
        }
        QLineEdit:focus {
            border-color: #0078d4;
            background: #2d2d2d;
        }
    """