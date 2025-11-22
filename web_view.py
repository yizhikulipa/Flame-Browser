from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QPainter

class FadeWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 1.0
        self.fade_animation = QPropertyAnimation(self, b"opacity")
        self.fade_animation.setDuration(400)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
    def setUrlWithAnimation(self, url):
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.3)
        self.fade_animation.finished.connect(lambda: self.load_url_and_fade_in(url))
        self.fade_animation.start()
        
    def load_url_and_fade_in(self, url):
        self.setUrl(QUrl(url))
        self.loadFinished.connect(self.on_load_finished)
        
    def on_load_finished(self):
        self.loadFinished.disconnect(self.on_load_finished)
        self.fade_animation.setStartValue(0.3)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()
        
    def get_opacity(self):
        return self._opacity
        
    def set_opacity(self, value):
        self._opacity = value
        self.update()
        
    opacity = pyqtProperty(float, get_opacity, set_opacity)
        
    def paintEvent(self, event):
        if self._opacity < 1.0:
            painter = QPainter(self)
            painter.setOpacity(self._opacity)
            super().paintEvent(event)
        else:
            super().paintEvent(event)
            