import sys
import os
import os.path
import platform
import FileTreeViewer
from PyQt5 import QtWidgets, QtGui
from PyQt5 import Qsci
from PyQt5 import QtCore
from format_call import *
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR



class TextEditorTab(QtWidgets.QTabWidget):
	def __init__(self):
		super(TextEditorTab, self).__init__()
		self.setTabsClosable(True)
		self.setMovable(True)
		self.setUsesScrollButtons(True)
		self.tabCloseRequested.connect(self.closeTab)
		# self.tabBarDoubleClicked.connect(self.closeTab)


	def closeTab(self, index):
		self.removeTab(index)


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, foldername):
		super(MainWindow, self).__init__()
		self.foldername = foldername
		# self.theme_list = \
		# [ './codes/src/theme/theme.css',
		# './codes/src/theme/dracula.css',
		# './codes/src/theme/wombat.css'
		# ]
		self.theme_list = \
		[ 'theme.css',
		'dracula.css',
		'wombat.css'
		]
		self.theme_count = 0;
		self.init_GUI()
		self.filename = None



	def init_GUI(self):
		self.setWindowIcon(QtGui.QIcon('bitbug_favicon_glass.png'))
		# set stylesheet--------------------------------------------------------

		self.setStyleSheet(open(self.theme_list[self.theme_count]).read())
		# ----------------------------------------------------------------------
		self.resize(700, 500)
		self.setWindowTitle('Editor')
		text = Qsci.QsciScintilla()
		# text = QtWidgets.QTextEdit()

		self.text_setting(text)

		self.filename = None

		#initiate the tab widget
		self.tab_widget = TextEditorTab()
		self.tab_widget.tabBarDoubleClicked.connect(self.new_or_close_tab)
		# at start, one default tab
		self.tab_widget.addTab(text,'new')
		self.text = text
		# self.setCentralWidget(self.tab_widget)

		self.statusBar()

		# add splitter----------------------------------------------------------
		self.splitter = QtWidgets.QSplitter(self)
		self.splitter.setOrientation(QtCore.Qt.Horizontal)
		# add file tree viewer--------------------------------------------------
		# 'D:\\code\\python\\qt_test\\codes_v7'
		self.listview = FileTreeViewer.FileTreeViewer(self.foldername)
		self.listview.itemClicked.connect(self.open_file_in_tree_view)
		# 'D:\\code\\python\\qt_test\\codes_v7\\a.exe'
		self.splitter.addWidget(self.listview)
		self.splitter.addWidget(self.tab_widget)
		self.splitter.setSizes([150,1000])

		self.setCentralWidget(self.splitter)
		# self.layout = QtWidgets.QVBoxLayout()
		# self.layout.setContentsMargins(1,1,1,1)
		# self.layout.setSpacing(0)
		# self.layout.addWidget(listview)
		# self.layout.addWidget(self.tab_widget)
		# self.setLayout(self.layout)


		# COMMON ACTIONS--------------------------------------------------------
		exit_action = self.make_action(name='Exit',
										shortCut='Ctrl+Q',
										statusTip='Exit',
										callback=QtWidgets.qApp.quit)
		run_code_action = self.make_action(name='Run',
										shortCut='Ctrl+R',
										statusTip='Run Code',
										callback=self.run_code)
		change_theme_to_wombat_action = \
							self.make_action(name='Change Theme',
												callback=self.change_theme_to_wombat)

		# ADD TOOLBAR-----------------------------------------------------------
		self.toolBar = self.addToolBar('Run')
		# self.toolBar.addAction(exit_action)
		self.toolBar.addAction(run_code_action)
		self.toolBar.addAction(change_theme_to_wombat_action)


		# create menu bar-------------------------------------------------------
		menu_bar = self.menuBar()
		# create actions under file menu----------------------------------------
		file_actions = []
		file_actions.append(self.make_action(name='New',
										shortCut='Ctrl+N',
										statusTip='New File',
										callback=self.new_file))
		file_actions.append(self.make_action(name='Open File...',
										shortCut='Ctrl+O',
										statusTip='Open File',
										callback=self.open_file))
		file_actions.append(self.make_action(name='Open Folder...',
										shortCut=None,
										statusTip='Open Folder',
										callback=self.open_folder))
		file_actions.append(self.make_action(name='Save',
										shortCut='Ctrl+S',
										statusTip='Save File',
										callback=self.save_file))
		file_actions.append(self.make_action(name='Save As...',
										shortCut='Ctrl+Alt+S',
										statusTip='Save File As...',
										callback=self.save_as_file))

		file_actions.append(exit_action)



		file_menu = menu_bar.addMenu('File')
		file_menu.addActions(file_actions)

		# create actions under format menu--------------------------------------
		format_actions = []
		format_actions.append(self.make_action(name='Format Code',
										shortCut='Ctrl+Alt+F',
										statusTip='Format Code',
										callback=self.format_code))

		format_actions.append(self.make_action(name='Simplify Code',
										shortCut='Ctrl+Shift+S',
										statusTip='Simplify Code',
										callback=self.simplify_code))

		format_menu = menu_bar.addMenu('Format')
		format_menu.addActions(format_actions)

		# create actions under style menu---------------------------------------
		style_actions = []
		style_actions.append(self.make_action(name='Change style',
										shortCut=None,
										statusTip='Change Style',
										callback=self.change_style))

		change_style_menu = menu_bar.addMenu('Style')
		change_style_menu.addActions(style_actions)

		# create actions under help menu----------------------------------------
		help_actions = []
		help_actions.append(self.make_action(name='About',
										shortCut=None,
										statusTip='About',
										callback=self.helpAbout))

		help_menu = menu_bar.addMenu('Help')
		help_menu.addActions(help_actions)

		# self.setStyleSheet(open('./codes/src/theme/dracula.css').read())


	def new_or_close_tab(self, index):
		print(index)
		if index != -1:
			self.tab_widget.removeTab(index)
		else:
			self.new_file()

	def open_file_in_tree_view(self, item, column):
		# filename
		# if item.childCount() == 0:
		# 	return
		try:
			filename = self.listview.dict[id(item)]
		except:
			return

		try:
			file = open(filename, "r")
		except:
			return
		self.new_file()
		self.filename = filename
		try:
			data = file.read()
		except:
			return
		# text = self.tab_widget.currentWidget()
		self.text.setText(data)
		self.setWindowTitle(self.filename)
		p, f = os.path.split(self.filename)
		self.tab_widget.setTabText(self.tab_widget.currentIndex(),f)


	def change_theme_to_wombat(self):
		self.theme_count += 1
		self.theme_count = self.theme_count % (len(self.theme_list))
		self.setStyleSheet(open(self.theme_list[self.theme_count]).read())


	def helpAbout(self):
		QtWidgets.QMessageBox.about(self, "About FrogPad",
						"""<b>FrogPad</b> V1.0.0
						<p>Copyright &copy; Luo Dai & Chen Zeng.
						All rights reserved.
						<p>This application can be used to edit, format and
						simplify the code.
						<p>Python %s - QT %s - PyQt %s on %s
						<p>Email: dailuo@gmail.com""" %
						(platform.python_version(),
						QT_VERSION_STR,
						PYQT_VERSION_STR,
						platform.platform()) )


	def change_style(self):
		try:
			data = self.tab_widget.currentWidget().text()
			fileWriteObj = open('tempIn.txt', 'w')
			fileWriteObj.write(data)
			fileWriteObj.close()
			style('tempIn.txt', 'tempOut.txt')

			fileReadObj = open('tempOut.txt', 'r')
			data = fileReadObj.read()
			fileReadObj.close()

			os.remove('tempIn.txt')
			os.remove('tempOut.txt')
			self.tab_widget.currentWidget().setText(data)
		except:
			pass


	def simplify_code(self):
		try:
			data = self.tab_widget.currentWidget().text()
			fileWriteObj = open('tempIn.txt', 'w')
			fileWriteObj.write(data)
			fileWriteObj.close()

			simplify('tempIn.txt', 'tempOut.txt')

			fileReadObj = open('tempOut.txt', 'r')
			data = fileReadObj.read()
			fileReadObj.close()

			os.remove('tempIn.txt')
			os.remove('tempOut.txt')
			self.tab_widget.currentWidget().setText(data)
		except:
			pass


	def format_code(self):
		try:
			data = self.tab_widget.currentWidget().text()
			fileWriteObj = open('tempIn.txt', 'w')
			fileWriteObj.write(data)
			fileWriteObj.close()

			format_called('tempIn.txt', 'tempOut.txt')

			fileReadObj = open('tempOut.txt', 'r')
			data = fileReadObj.read()
			fileReadObj.close()

			os.remove('tempIn.txt')
			os.remove('tempOut.txt')
			self.tab_widget.currentWidget().setText(data)
		except:
			pass


	def open_folder(self):
		try:
			foldername = \
				QtWidgets.QFileDialog.getExistingDirectory(self,
				'Open Folder',
				'D:\\code')
			print(foldername)
			self.newWindow = SlaveWindow(foldername)
			self.newWindow.showMaximized()
			self.newWindow.show()
		except:
			pass

	def open_file(self):
		file_name = \
			QtWidgets.QFileDialog.getOpenFileName(self,
			'Open File',
			 "D:\\code\\python\\qt_test\\codes_v2\\codes\\test_sample")

		if file_name[0] is '':
			return

		file = open(file_name[0], "r")

		self.filename = file_name[0]
		data = file.read()
		text = self.tab_widget.currentWidget()
		text.setText(data)
		self.setWindowTitle(self.filename)
		p, f = os.path.split(file_name[0])
		self.tab_widget.setTabText(self.tab_widget.currentIndex(),f)


	def new_file(self):
		text = Qsci.QsciScintilla()
		self.text_setting(text)
		self.tab_widget.addTab(text, 'new')
		self.tab_widget.setCurrentWidget(text)
		self.text = text # set the current text editor to be self.text


	def save_as_file(self):
		file_name = QtWidgets.QFileDialog.getSaveFileName(self,
													'Save as...',
													'D:\\code\\python')
		try:
			fileWriteObj = open(file_name[0], 'w')
			data = self.text.text()
			fileWriteObj.write(data)
			fileWriteObj.close()
			self.filename = file_name[0]
			self.setWindowTitle(self.filename)
		except:
			return


	def save_file(self):
		if self.filename is None:
			file_name = QtWidgets.QFileDialog.getSaveFileName(self,
														'Save File',
														'D:\\code\\python')
			try:
				fileWriteObj = open(file_name[0], 'w')
				data = self.text.text()
				fileWriteObj.write(data)
				fileWriteObj.close()
				self.filename = file_name[0]
				self.setWindowTitle(self.filename)
			except:
				return
		else:
			data = self.text.text()
			fileWriteObj = open(self.filename, 'w')
			fileWriteObj.write(data)
			fileWriteObj.close()


	def text_setting(self, text):
		# set font
		font = QtGui.QFont()
		font.setFamily ('Consolas')
		font.setBold(True)
		font.setFixedPitch(True)
		font.setPointSize(12)

		# set lex
		lex = Qsci.QsciLexerCPP()

		lex.setFont(font)
		lex.setColor(QtGui.QColor('#ffffff'))
		lex.setColor(QtGui.QColor('#ff0b66'), Qsci.QsciLexerCPP.Keyword)
		lex.setColor(QtGui.QColor("#00FF40"), Qsci.QsciLexerCPP.Comment)
		lex.setColor(QtGui.QColor("#BD4FE8"), Qsci.QsciLexerCPP.Number)
		lex.setColor(QtGui.QColor("#04F452"), Qsci.QsciLexerCPP.PreProcessor)

		lex.setColor(QtGui.QColor("#F1E607"),Qsci.QsciLexerCPP.DoubleQuotedString)
		lex.setColor(QtGui.QColor("#FFFFFF"),Qsci.QsciLexerCPP.Operator)
		lex.setColor(QtGui.QColor("#FFFFFF"),Qsci.QsciLexerCPP.Identifier)

		lex.setColor(QtGui.QColor("#F1E607"),Qsci.QsciLexerCPP.UnclosedString)


		text.setLexer(lex)
		lex.setPaper(QtGui.QColor('#45494a'))
		text.setTabWidth(4)
		text.setUtf8(True)

		text.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle)

		text.setMarginWidth(2,12)

		text.setMarkerBackgroundColor(QtGui.QColor("#FFFFFF"),Qsci.QsciScintilla.SC_MARKNUM_FOLDEREND)
		text.setMarkerForegroundColor(QtGui.QColor("#45494a"),Qsci.QsciScintilla.SC_MARKNUM_FOLDEREND)
		text.setMarkerBackgroundColor(QtGui.QColor("#FFFFFF"),Qsci.QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
		text.setMarkerForegroundColor(QtGui.QColor("#45494a"),Qsci.QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
		text.setMarkerBackgroundColor(QtGui.QColor("#FFFFFF"),Qsci.QsciScintilla.SC_MARKNUM_FOLDERSUB)
		text.setMarkerForegroundColor(QtGui.QColor("#45494a"),Qsci.QsciScintilla.SC_MARKNUM_FOLDERSUB)
		text.setMarkerBackgroundColor(QtGui.QColor("#FFFFFF"),Qsci.QsciScintilla.SC_MARKNUM_FOLDER)
		text.setMarkerForegroundColor(QtGui.QColor("#45494a"),Qsci.QsciScintilla.SC_MARKNUM_FOLDER)
		text.setMarkerBackgroundColor(QtGui.QColor("#FFFFFF"),Qsci.QsciScintilla.SC_MARKNUM_FOLDEROPEN)
		text.setMarkerForegroundColor(QtGui.QColor("#45494a"),Qsci.QsciScintilla.SC_MARKNUM_FOLDEROPEN)
		text.setFoldMarginColors(QtGui.QColor("#45494a"),QtGui.QColor("#45494a"))

		text.setWhitespaceVisibility(Qsci.QsciScintilla.WsInvisible)
		text.setWhitespaceSize(2)
		text.setMarginWidth(1,0)


		# set indentation
		text.setIndentationWidth(4)
		text.setIndentationGuides(True)
		text.setAutoIndent(True)
		text.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll);
		text.setAutoCompletionThreshold(3)

		# set brace matching
		text.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)

		text.setCaretLineVisible(True)
		text.setCaretLineBackgroundColor(QtGui.QColor("#2D2D2D"))
		text.setCaretForegroundColor(QtGui.QColor("white"))
		# set Margins
		text.setMarginsFont(font)
		fontmetrics = QtGui.QFontMetrics(font)
		text.setMarginWidth(0, fontmetrics.width("0000") + 6)
		text.setMarginLineNumbers(0, True)
		text.setMarginsBackgroundColor(QtGui.QColor("#45494a"))
		text.setMarginsForegroundColor(QtGui.QColor("#ffffff"))


	def make_action(self, name='CLICK', shortCut=None, statusTip='CLICK',\
						callback=None):
		action = QtWidgets.QAction(name, self)
		if not shortCut is None:
			action.setShortcut(shortCut)

		if not statusTip is None:
			action.setStatusTip(statusTip)

		action.triggered.connect(callback)
		return action

	def run_code(self):
		if self.filename is None:
			return
		command = 'gcc ' + self.filename
		#print(self.filename)
		os.system(command)
		command = 'a'
		os.system(command)


class SlaveWindow(MainWindow):
	def __init__(self, foldername):
		MainWindow.__init__(self,foldername)

app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow('D:\\code\\python\\qt_test\\codes_v7')
main_window.showMaximized()
main_window.show()
sys.exit(app.exec_())
