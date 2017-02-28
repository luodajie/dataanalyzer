import re
from PyQt4 import QtCore, QtGui
from StyleSet import stylish
import datameer_requests
from Analysis_Gui import Window
from Rename_Column import Column_Window
import Welcome_Gui

class WorkBookMain(QtGui.QMainWindow):
	def __init__(self, parent=None, user = None, passwrd = None, oracle_pass=None):
		super(WorkBookMain, self).__init__(parent)

		self.user = user
		self.passwrd = passwrd
		self.oracle_pass = oracle_pass

		self.setGeometry(70,70,841,591)
		stylish(self)

		title = QtGui.QLabel()
		title.setText("\t\tWelcome\n Please Enter WorkBook Id and select sheet")
		title.setAlignment(QtCore.Qt.AlignCenter)
		self.setWindowTitle("Workbook")

		self.font = QtGui.QFont()
		palette = QtGui.QPalette()
		title.setPalette(palette)
		self.font.setPointSize(14)
		self.font.setBold(True)
		self.font.setWeight(75)
		title.setFont(self.font)

		self.widget = QtGui.QWidget()

		graphicsView = QtGui.QGraphicsView()
		graphicsView.setGeometry(QtCore.QRect(70, 70, 841, 591))

		label1 = QtGui.QLabel()
		label1.setText("WorkBook ID :")

		self.label2 = QtGui.QLabel()
		self.label2.setText("WorkBook Path: ")

		self.font_path = QtGui.QFont()
		palette_path = QtGui.QPalette()
		self.font_path.setFamily("Helvetica")
		# palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.white)

		self.font_path.setPointSize(11)
		self.font_path.setWeight(40)

		self.label3= QtGui.QLabel()
		self.label3.setPalette(palette_path)
		self.label3.setFont(self.font_path)

		self.label3.setStyleSheet( '''
		QLabel	{
			color: #ffcc66
			}
			'''
		)

		label4 = QtGui.QLabel()
		label4.setText("Choose sheet: ")

		self.label5 = QtGui.QLabel()
		self.label5.setText("WorkBook Name: ")
		self.label6 = QtGui.QLabel()
		self.label6.setFont(self.font_path)


		self.label6.setStyleSheet( '''
		QLabel	{
			color: #ffcc66
			}
			'''
		)

		self.lineEdit = QtGui.QLineEdit()
		self.lineEdit.setGeometry(QtCore.QRect(260, 120, 491, 21))
		self.lineEdit.setPlaceholderText("Enter WorkBook Id here and then press Enter")
		# self.lineEdit.clearFocus()
		self.lineEdit.editingFinished.connect(self.editing_finished)
		self.lineEdit.textEdited.connect(self.text_edited)

		self.listWidget = QtGui.QListWidget()
		self.listWidget.setGeometry(QtCore.QRect(70, 70, 841, 391))

		self.buttonBox = QtGui.QDialogButtonBox(self)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Close)
		self.buttonBox.accepted.connect(self.go_analysis)
		self.buttonBox.rejected.connect(self.reset)

		self.buttonBox.button(QtGui.QDialogButtonBox.Close).setText("Back")
		self.buttonBox.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.back_to_welcome)

		self.button_group = QtGui.QButtonGroup()


		glayout = QtGui.QGridLayout()
		glayout.addWidget( self.label5, 0,0)
		glayout.addWidget( self.label6, 1,0)
		glayout.addWidget( self.label2, 2,0)
		glayout.addWidget( self.label3, 3,0)

		self.hlayout = QtGui.QHBoxLayout()
		self.hlayout.addLayout(glayout)

		self.vlayout = QtGui.QVBoxLayout()
		self.vlayout.addWidget(title)
		self.vlayout.addWidget(label1)
		self.vlayout.addWidget(self.lineEdit)
		self.vlayout.addLayout(self.hlayout)
		self.vlayout.addWidget(label4)
		self.vlayout.addWidget(self.listWidget)
		self.vlayout.addWidget(self.buttonBox)

		graphicsView.setLayout(self.vlayout)
		self.widget.setLayout(self.vlayout)
		self.setCentralWidget(self.widget)

		self.center()
		self.show()

	def editing_finished(self):
		# This signal is emitted when the Return or Enter key is pressed or the line edit loses focus.
		id = self.lineEdit.text()
		self.font_radio = QtGui.QFont()
		palette = QtGui.QPalette()
		self.font_radio.setFamily("Helvetica")
		self.font_radio.setPointSize(11)
		self.font_radio.setWeight(40)


		try:
			(path, names) = self.get_datameer_sheets(int(id))
			self.label3.setText(path)

			get_file_name = re.search('^(.*/)([^/]*)$', path)

			if get_file_name:
				found_file_name = get_file_name.group(2)
				self.label6.setText(found_file_name)
			self.listWidget.clear()

			for name in names:
				listItem = QtGui.QListWidgetItem(name, self.listWidget)
				self.radio_btn = QtGui.QRadioButton("{0}".format(name))
				self.radio_btn.setPalette(palette)
				self.radio_btn.setFont(self.font_radio)
				# self.radio_btn.setChecked(True)
				self.vlayout.addWidget(self.radio_btn)
				self.button_group.addButton(self.radio_btn)
				self.listWidget.addItem(listItem)
				self.listWidget.setItemWidget(listItem, self.radio_btn)
			self.listWidget.setFocus()


		except ValueError:
			if self.lineEdit.text() == "":
				pass
			else:
				msg = QtGui.QMessageBox()
				msg.setIcon(QtGui.QMessageBox.Critical)
				msg.setWindowTitle('Error')
				msg.setText("ID must be an integer!")
				msg.exec_()

				self.label3.setText('')
				self.label6.setText('')
				self.listWidget.clear()

		except IOError as e :
			self.label3.setText('')
			self.label6.setText('')
			self.lineEdit.clear()
			self.listWidget.clear()
			msg = QtGui.QMessageBox()
			msg.setIcon(QtGui.QMessageBox.Critical)
			msg.setWindowTitle('Error')
			msg.setText(str(e))
			msg.exec_()

	def get_datameer_sheets(self, id):
		return datameer_requests.get_sheets(id)

	def text_edited(self):

		# This signal is emitted whenever the text is edited.
		self.label3.setText('')
		self.label6.setText('')
		self.listWidget.clear()

#

	def go_analysis(self):

		try:
			if self.button_group.checkedButton() == None:
				raise IOError('Please select a sheet!')

			name = self.button_group.checkedButton().text()
			id = self.lineEdit.text()

			self.go_analysis_window(id=int(id), sheet=name, user = self.user, coder = self.passwrd)

		except IOError as e:
			msg = QtGui.QMessageBox()
			msg.setIcon(QtGui.QMessageBox.Critical)
			msg.setWindowTitle('Error')
			msg.setText(str(e))
			msg.exec_()

	def go_analysis_window(self, id, sheet, user, coder):
		wind = Window(parent=self, id= id, sheet= sheet, user = user, coder = coder)
		wind.show()


	def reset(self):
		self.lineEdit.clear()
		self.label3.setText('')
		self.label6.setText('')
		self.listWidget.clear()

	def back_to_welcome(self):
		self.close()
		self.win = Welcome_Gui.Ui_MainWindow(user=self.user, passwrd=self.passwrd, oracle_pass=self.oracle_pass)
		self.win.show()


	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())



class rename_column(WorkBookMain):
	def __init__(self, parent = None, user= None, passwrd=None):
		WorkBookMain.__init__(self, parent, user, passwrd)

	def get_datameer_sheets(self, id):
		return datameer_requests.get_column_sheets(id)

	def go_analysis_window(self, id, sheet, user, coder):
		self.wind = Column_Window(id= id, sheet= sheet, user = user, coder = coder)
		# wind.show()



if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	gui = WorkBookMain()
	sys.exit(app.exec_())

