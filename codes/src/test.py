import sys
import os
import os.path
import platform
from PyQt5 import QtWidgets, QtGui
from PyQt5 import Qsci
from PyQt5 import QtCore
from format_call import *
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR


app = QtWidgets.QApplication(sys.argv)
main_window = Qsci.QsciScintilla()
main_window.setWhitespaceVisibility(Qsci.QsciScintilla.WsInvisible)
main_window.setWhitespaceSize(2)
main_window.setStyleSheet(
"""
QsciScintilla{
	background-color: black;
}
"""
    )

main_window.show()
sys.exit(app.exec_())
