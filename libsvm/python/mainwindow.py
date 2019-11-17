from pathlib import Path

#from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtGui import QPixmap
#from PyQt5.QtWidgets import (
#    QApplication,
#    QFileDialog,
#    QLabel,
#    QMainWindow,
#    QPushButton,
#    QStackedWidget,
#    QVBoxLayout,
#    QWidget,
#)

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import brisquequality
#in this folder

import qtmodern.styles
import qtmodern.windows

#pip3 install qtmodern

class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        self.tools_btn = QPushButton("Back to menu", self)
        self.label = QLabel(self)
        self.text_edit = QLineEdit(self)
#        self.progress = QtGui.QProgressBar(self)

        self.text_edit.setReadOnly(True)
        self.text_edit.resize(10,40)
        self.text_edit.setSizePolicy(QSizePolicy.Minimum,
                         QSizePolicy.Minimum)
        
        def lightTheme(self):
            qtmodern.styles.light(QApplication.instance())

        def darkTheme(self):
            qtmodern.styles.dark(QApplication.instance())
            
        font = QFont()
        font.setFamily("./consola.ttf")
        font.setPixelSize(10)
        
        self.tools_btn.setFont(font)
            
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.text_edit)
        vbox.addWidget(self.label)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.tools_btn)
        vbox.addStretch(0)
        

    def set_photo(self, photo, score):
        pixmap = QPixmap(photo)
        pixmap2 = pixmap.scaled(640, 480, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap2)
        self.text_edit.setText(photo + " with score " + str(score))
        
class UIToolTab(QWidget):
    def __init__(self, parent=None):
        super(UIToolTab, self).__init__(parent)

        self.cps_btn = QPushButton("Choose", self)
        self.label = QLabel(self)
        
        font = QFont()
        font.setFamily("./consola.ttf")
        font.setPixelSize(25)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1)
        
        self.label.setFont(font)
        self.label.setText("Photo Picking")
        self.label.setStyleSheet('color: #2196f3')
        
        font.setPixelSize(10)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0)
        
        self.cps_btn.setFont(font)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.label)
        vbox.setSpacing(10)
        vbox.addWidget(self.cps_btn)
        vbox.setAlignment(Qt.AlignCenter)



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.setGeometry(0, 0, 720, 480)
        self.setFixedSize(720, 400)
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.ui_tool = UIToolTab()
        self.ui_window = UIWindow()

        self.stacked_widget.addWidget(self.ui_tool)
        self.stacked_widget.addWidget(self.ui_window)

        self.ui_tool.cps_btn.clicked.connect(self.on_choose_clicked)
        self.ui_window.tools_btn.clicked.connect(self.open_tools_window)

    @pyqtSlot()
    def on_choose_clicked(self):
        dirname = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirname:
            path = Path(dirname)
            glob_path = path.glob("*")
            path_to_photo = brisquequality.answer(glob_path)
            self.ui_window.set_photo(path_to_photo, brisquequality.best_score_get())
            self.stacked_widget.setCurrentIndex(1)

    @pyqtSlot()
    def open_tools_window(self):
        self.stacked_widget.setCurrentIndex(0)


if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(MainWindow())
    mw.show()    
    sys.exit(app.exec_())