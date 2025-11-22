from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class AnimatedTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = QPropertyAnimation(self, b"currentIndex")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def setCurrentIndexWithAnimation(self, index):
        self.animation.setStartValue(self.currentIndex())
        self.animation.setEndValue(index)
        self.animation.start()
        