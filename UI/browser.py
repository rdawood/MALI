import sys
from PyQt4 import QtCore, QtGui, QtWebKit

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class vizBrowser(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(1250, 920)
        self.centralwidget = QtGui.QWidget(self)
        self.setWindowTitle("MALI Visual Output")

        self.mainLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(1)

        self.frame = QtGui.QFrame(self.centralwidget)

        self.gridLayout = QtGui.QVBoxLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)

        self.horizontalLayout = QtGui.QHBoxLayout()

        self.gridLayout.addLayout(self.horizontalLayout)

        self.html = QtWebKit.QWebView()
        self.gridLayout.addWidget(self.html)
        self.mainLayout.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)
    
    def renderVisualization(self, url):
        self.html.setUrl(QtCore.QUrl(_fromUtf8(url)))
        self.html.load(QtCore.QUrl(url))
        self.html.show()
