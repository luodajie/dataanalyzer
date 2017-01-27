from PyQt4 import QtCore, QtGui
import sys
from StyleSet import stylish
from WorkBook_Selector import WorkBookMain

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

def close_application():
	sys.exit()



class Ui_MainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None, user = None, passwrd = None, oracle_pass=None):
		super(Ui_MainWindow, self).__init__(parent)
		self.user = user
		self.passwrd = passwrd
		self.oracle_pass = oracle_pass

		self.resize(818, 620)
		self.setWindowOpacity(0.95)
		self.centralwidget = QtGui.QWidget()
		stylish(self.centralwidget)
		self.label = QtGui.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(330, 60, 161, 31))
		font = QtGui.QFont()
		font.setPointSize(22)
		self.label.setFont(font)
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(260, 180, 281, 21))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_2.setFont(font)
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.pushButton = QtGui.QPushButton(self.centralwidget)
		self.pushButton.setGeometry(QtCore.QRect(230, 330, 111, 31))
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		# self.pushButton.clicked.connect(self.OracleOpen)

		self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_2.setGeometry(QtCore.QRect(430, 330, 140, 31))
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.pushButton_2.clicked.connect(self.workBookOpen)

		self.label_3 = QtGui.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(380, 340, 21, 16))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menu_File = QtGui.QMenu(self.menubar)
		self.menu_File.setObjectName(_fromUtf8("menu_File"))
		self.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(self)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		self.setStatusBar(self.statusbar)
		self.toolBar = QtGui.QToolBar(self)
		self.toolBar.setObjectName(_fromUtf8("toolBar"))
		self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
		self.action_DataBase = QtGui.QAction(QtGui.QIcon('resources/database.png'), "Database", self)
		self.action_DataBase.setObjectName(_fromUtf8("action_DataBase"))
		self.action_DataBase.setShortcut("Ctrl+D")
		# self.action_DataBase.triggered.connect(self.OracleOpen)

		self.action_Graphs = QtGui.QAction(QtGui.QIcon('resources/graph.ico'), "Graph", self)
		self.action_Graphs.setObjectName(_fromUtf8("action_Graphs"))
		self.action_Graphs.setShortcut("Ctrl+G")
		self.action_Graphs.triggered.connect(self.workBookOpen)

		self.actionQuit = QtGui.QAction(QtGui.QIcon('resources/exit24.png'), "Exit", self)
		self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
		self.actionQuit.setShortcut("Ctrl+Q")
		self.actionQuit.triggered.connect(close_application)
		self.menu_File.addAction(self.action_DataBase)
		self.menu_File.addAction(self.action_Graphs)
		self.menu_File.addAction(self.actionQuit)
		self.menubar.addAction(self.menu_File.menuAction())
		self.toolBar.addAction(self.action_DataBase)
		self.toolBar.addAction(self.action_Graphs)
		self.toolBar.addAction(self.actionQuit)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)
		self.setTabOrder(self.pushButton, self.pushButton_2)
		self.show()

	def retranslateUi(self):
		self.setWindowTitle(_translate("MainWindow", "Welcome", None))
		self.setWindowIcon(QtGui.QIcon("resources/analytic-icon.png"))
		self.label.setText(_translate("MainWindow", "Welcome ", None))
		self.label_2.setText(_translate("MainWindow", "Which task would you like to perform ?", None))
		self.pushButton.setText(_translate("MainWindow", "Positng in Oracle", None))
		self.pushButton_2.setText(_translate("MainWindow", "WorkBook and Graphs", None))
		self.label_3.setText(_translate("MainWindow", "OR", None))
		self.menu_File.setTitle(_translate("MainWindow", "&File", None))
		self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
		self.action_DataBase.setText(_translate("MainWindow", "&DataBase", None))
		self.action_Graphs.setText(_translate("MainWindow", "&Graphs", None))
		self.actionQuit.setText(_translate("MainWindow", "&Quit", None))

	def workBookOpen(self, user=None, passwrd = None):
		user = self.user
		passwrd = self.passwrd
		self.close()

		self.wind = WorkBookMain(user= user, passwrd = passwrd)
		self.wind.show()

	# def OracleOpen(self, user = None, oracle_pass = None):
	# 	user = self.user
	# 	oracle_pass = self.oracle_pass
	# 	self.close()
	#
	# 	self.sec = SqlServer_to_Oracle(user=user, oracle_pass=oracle_pass)


if __name__ == "__main__":

	app = QtGui.QApplication(sys.argv)
	ui = Ui_MainWindow()
	sys.exit(app.exec_())

