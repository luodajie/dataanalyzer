# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'second.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from StyleSet import stylish
from time import sleep
import Welcome_Gui
import SQL_Server_to_Oracle

import sys

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

class Second(QtGui.QMainWindow):
	def __init__(self, parent=None, user=None, passwrd=None, oracle_pass=None):
		super(Second, self).__init__(parent)

		self.user = user
		self.passwrd = passwrd
		self.oracle_pass = oracle_pass


		self.setObjectName(_fromUtf8("MainWindow"))
		self.resize(648, 508)
		self.setWindowOpacity(0.95)

		self.centralwidget = QtGui.QWidget()
		stylish(self.centralwidget)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
		self.graphicsView.setGeometry(QtCore.QRect(70, 50, 511, 351))
		self.graphicsView.setObjectName(_fromUtf8("graphicsView"))

		self.label1 = QtGui.QLabel(self.centralwidget)
		self.label1.setGeometry(QtCore.QRect(170, 20, 300, 20))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label1.setFont(font)
		self.label1.setObjectName(_fromUtf8("label1"))

		self.formLayoutWidget = QtGui.QWidget(self.centralwidget)
		self.formLayoutWidget.setGeometry(QtCore.QRect(80, 60, 491, 331))
		self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
		self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
		self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
		self.formLayout.setObjectName(_fromUtf8("formLayout"))

		self.label = QtGui.QLabel(self.formLayoutWidget)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setObjectName(_fromUtf8("label"))
		self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)

		self.lineEdit = QtGui.QLineEdit(self.formLayoutWidget)
		self.lineEdit.setFrame(True)
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit)

		self.label_2 = QtGui.QLabel(self.formLayoutWidget)
		self.label_2.setAlignment(QtCore.Qt.AlignCenter)
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)

		self.textEdit = QtGui.QTextEdit(self.formLayoutWidget)
		self.textEdit.setFrameShape(QtGui.QFrame.Panel)
		self.textEdit.setFrameShadow(QtGui.QFrame.Sunken)
		self.textEdit.setLineWidth(1)
		self.textEdit.setMidLineWidth(1)
		self.textEdit.setTabChangesFocus(True)
		self.textEdit.setObjectName(_fromUtf8("textEdit"))
		self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.textEdit)

		self.label_3 = QtGui.QLabel(self.formLayoutWidget)
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)

		self.lineEdit_2 = QtGui.QLineEdit(self.formLayoutWidget)
		self.lineEdit_2.setAutoFillBackground(False)
		self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
		self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_2)

		self.label_4 = QtGui.QLabel(self.formLayoutWidget)
		self.label_4.setAlignment(QtCore.Qt.AlignCenter)
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)

		self.lineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget)
		self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
		self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_3)

		
		self.buttonBox = QtGui.QDialogButtonBox(self.centralwidget)
		self.buttonBox.setGeometry(QtCore.QRect(230, 430, 156, 23))
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save|QtGui.QDialogButtonBox.Close)
		self.buttonBox.setCenterButtons(False)
		self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
		self.buttonBox.accepted.connect(self.validate_form)
		self.buttonBox.rejected.connect(self.reset)

		self.buttonBox.button(QtGui.QDialogButtonBox.Close).setText("Back")
		self.buttonBox.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.back_to_welcome)


		self.setCentralWidget(self.centralwidget)
		self.statusbar = QtGui.QStatusBar(self)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		self.setStatusBar(self.statusbar)
		self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

		self.retranslateUi()
		QtCore.QMetaObject.connectSlotsByName(self)
		self.show()

	def retranslateUi(self):
		self.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.setWindowIcon(QtGui.QIcon("resources/analytic-icon.png"))
		self.label1.setText(_translate("MainWindow", "Migration SQL Server ---> Oracle ", None))
		self.label.setText(_translate("MainWindow", "Request No.:", None))
		self.label_2.setText(_translate("MainWindow", "Test Number:\n \n ( Please insert\n Comma Seperated \nValues )", None))
		self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter Request Number here.....", None))
		self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "YYYYMMDD", None))
		self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "YYYYMMDD", None))
		self.label_3.setText(_translate("MainWindow", "Start Date:", None))
		self.label_4.setText(_translate("MainWindow", "End Date:", None))



	def reset(self):
		self.lineEdit.clear()
		self.lineEdit_2.clear()
		self.lineEdit_3.clear()
		self.textEdit.clear()

	def send_userInput_to_database(self):
		req_num = self.lineEdit.text()
		return SQL_Server_to_Oracle.check_row_count(user_oracle=self.user, passwrd=self.oracle_pass, req_num=req_num, test_num=self.textEdit.toPlainText(), start_date=self.lineEdit_2.text(), end_date=self.lineEdit_3.text())

		
	def back_to_welcome(self):
		self.close()
		self.win = Welcome_Gui.Ui_MainWindow(user=self.user, passwrd=self.passwrd, oracle_pass=self.oracle_pass)
		self.win.show()


	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Return:
			# If Return is pressed, replace it with Space
			e = QtGui.QKeyEvent(QtCore.QEvent.KeyPress,
								QtCore.Qt.Key_Space,
								e.modifiers(),
								e.text(),
								e.isAutoRepeat(),
								e.count())

		# Call the base class event handler
		# QtGui.QDialogButtonBox.Save.keyPressEvent(e)
		self.buttonBox.button(QtGui.QDialogButtonBox.Save).keyPressEvent(e)

	def keyReleaseEvent(self, e):
		if e.key() == QtCore.Qt.Key_Return:
			e = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease,
								QtCore.Qt.Key_Space,
								e.modifiers(),
								e.text(),
								e.isAutoRepeat(),
								e.count())

		self.buttonBox.button(QtGui.QDialogButtonBox.Save).keyReleaseEvent(e)

	def tabkeypressevent(self, event):
		if event.key() == QtCore.Qt.Key_Tab:
			self.textEdit.setTabChangesFocus(True)
			
	def show_progress(self):
		self.progress = ProgressDialog(parent=self, mainWindow=self)
		self.progress.resize(250, 50)
		self.progress.exec_()
		
	def validate_form(self):
		req_num = str(self.lineEdit.text())
		test_num = str(self.textEdit.toPlainText())
		start_date = str(self.lineEdit_2.text())
		end_date = str(self.lineEdit_3.text())
		
		if not req_num.isdigit():
			QtGui.QMessageBox.warning(self, 'Error', 'Invalid Request No.!')
		elif test_num.strip() == "":
			QtGui.QMessageBox.warning(self, 'Error', 'Empty Test Number!')
		elif not start_date.isdigit() or len(start_date) != 8:
			QtGui.QMessageBox.warning(self, 'Error', 'Invalid Start Date!')
		elif not end_date.isdigit() or len(end_date) != 8:
			QtGui.QMessageBox.warning(self, 'Error', 'Invalid End Date!')
		else:
			self.show_progress()

class ProgressDialog(QtGui.QDialog):
	def __init__(self, parent=None, mainWindow=None):
		super(ProgressDialog, self).__init__(parent)
		
		self.setWindowTitle("Please wait...")
		self._want_to_close = False
		
		layout = QtGui.QVBoxLayout(self)
		self.progressBar = QtGui.QProgressBar(self)
		self.progressBar.setRange(0,0)
		layout.addWidget(self.progressBar)
		self.setLayout(layout)

		self.myLongTask = TaskThread(mainWindow)
		self.myLongTask.start()
		self.myLongTask.taskFinishedSignal.connect(self.onFinished)
		self.myLongTask.taskErrorSignal.connect(self.onError)

	def onFinished(self, argument):
		self.progressBar.setRange(0,1)
		self.progressBar.setValue(1)
		self._want_to_close = True
		self.close()
		QtGui.QMessageBox.information(self, 'Success', 'Done! Tests inserted: ' + argument)
		
	def onError(self, argument):
		self._want_to_close = True
		self.close()
		QtGui.QMessageBox.critical(self, 'Error', argument)
		
	def closeEvent(self, evnt):
		if self._want_to_close:
			super(ProgressDialog, self).closeEvent(evnt)
		else:
			evnt.ignore()

class TaskThread(QtCore.QThread):

	taskFinishedSignal = QtCore.pyqtSignal(str)
	taskErrorSignal = QtCore.pyqtSignal(str)
	
	def __init__(self, mainWindow=None):
		super(TaskThread, self).__init__()
		self.mainWindow = mainWindow
	
	def run(self):
		try:
			msg = self.mainWindow.send_userInput_to_database()
			#for i in range(100000000):
			#	x = i * i
			self.taskFinishedSignal.emit(msg)
		except Exception as e:
			self.taskErrorSignal.emit(str(e))

if __name__ == "__main__":

	app = QtGui.QApplication(sys.argv)
	ui = Second()
	sys.exit(app.exec_())

