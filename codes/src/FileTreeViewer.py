from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os.path
import os


class FileTreeViewer(QTreeWidget):
	"""docstring for FileTreeViewer"""
	def __init__(self, foldername):
		super(FileTreeViewer, self).__init__()
		self.dict = {}
		self.__initui__(foldername)



	def listdir(self, level, path, father_node):
		for i in os.listdir(path):
			node = QTreeWidgetItem(father_node, QTreeWidgetItem.UserType)
			self.dict[id(node)] = path+'\\'+i
			node.setText(0, i)
			if os.path.isdir(path+'\\'+i):

				self.listdir(level+1, path+'\\'+i, node)


	def __initui__(self, foldername):
		self.setHeaderHidden(True)
		node = QTreeWidgetItem(self, QTreeWidgetItem.UserType)
		node.setText(0, os.path.split(foldername)[1])
		self.listdir(1, foldername, father_node=node)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	widget = FileTreeViewer()
	widget.show()
	sys.exit(app.exec_())
	pass
