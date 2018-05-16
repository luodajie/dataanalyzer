from PyQt4 import QtCore, QtGui
from StyleSet import form
import datameer_requests
import OracleDb
from Welcome_Gui import Ui_MainWindow
import ConfigParser


class User_Widget(QtGui.QMainWindow):
	def __init__(self, argv=None, parent=None):
		super(User_Widget, self).__init__(parent)
		app_icon = QtGui.QIcon()
		app_icon.addFile('resources/analytic-icon.png', QtCore.QSize(16,16))
		app_icon.addFile('resources/analytic-icon.png', QtCore.QSize(24,24))
		app_icon.addFile('resources/analytic-icon.png', QtCore.QSize(32,32))
		app_icon.addFile('resources/analytic-icon.png', QtCore.QSize(48,48))
		app_icon.addFile('resources/analytic-icon.png', QtCore.QSize(256,256))
		app.setWindowIcon(app_icon)

		self.setFixedSize(250, 300)
		self.setWindowTitle("User Login")

		self.setWindowOpacity(0.9)

		form_widget = QtGui.QWidget()
		form_widget.setObjectName("Form")
		form(Form=form_widget)

		title = QtGui.QLabel()
		title.setText("Datameer Login !")
		title.setAlignment(QtCore.Qt.AlignCenter)
		title.setGeometry(10, 20, 20,10)

		title1 = QtGui.QLabel()
		title1.setText("Oracle Login !")
		title1.setAlignment(QtCore.Qt.AlignCenter)
		title1.setGeometry(10, 20, 20,10)

		pic = QtGui.QLabel(self)
		pic.setGeometry(20, 10, 400, 100)
		pic.setAlignment(QtCore.Qt.AlignCenter)
		pic.setPixmap(QtGui.QPixmap("resources/login.png"))


		self.font = QtGui.QFont()
		palette = QtGui.QPalette()
		# palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.white)
		title.setPalette(palette)
		title1.setPalette(palette)
		self.font.setPointSize(12)
		self.font.setBold(True)
		self.font.setWeight(10)
		title.setFont(self.font)
		title1.setFont(self.font)

		user = QtGui.QLabel()
		user.setText("UserId : ")
		passwrd = QtGui.QLabel()
		passwrd.setText("Password: ")

		orcl_user = QtGui.QLabel()
		orcl_user.setText("UserId : ")
		orcl_passwrd = QtGui.QLabel()
		orcl_passwrd.setText("Password: ")

		self.UserLine = QtGui.QLineEdit()
		self.UserLine.setMaxLength(20)
		self.PassLine = QtGui.QLineEdit()
		self.PassLine.setEchoMode(QtGui.QLineEdit.Password)
		self.PassLine.setMaxLength(20)

		self.Orcl_UserLine = QtGui.QLineEdit()
		self.Orcl_UserLine.setMaxLength(20)
		self.Orcl_PassLine = QtGui.QLineEdit()
		self.Orcl_PassLine.setEchoMode(QtGui.QLineEdit.Password)
		self.Orcl_PassLine.setMaxLength(20)
		
		if len(argv) == 4:
			self.UserLine.setText(str(argv[1]))
			self.PassLine.setText(str(argv[2]))
			self.Orcl_PassLine.setText(str(argv[3]))

		self.Button = QtGui.QPushButton("Sign In")
		self.Button.setFixedWidth(60)
		self.Button.setFocus()
		self.Button.setDefault(True)
		self.Button.clicked.connect(self.authenticate_user)


		self.errorLabel = QtGui.QLabel()
		self.errorLabel.setAlignment(QtCore.Qt.AlignCenter)
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
		self.errorLabel.setPalette(palette)

		vlayout = QtGui.QVBoxLayout()
		# vlayout.addWidget(self.errorLabel)
		vlayout.addWidget(pic)
		vlayout.addWidget(title)

		vlayout1 = QtGui.QVBoxLayout()
		vlayout1.addWidget(title1)

		Glayout = QtGui.QGridLayout()
		Glayout.addWidget(user, 1,1)
		Glayout.addWidget(self.UserLine, 1, 2)
		Glayout.addWidget(passwrd, 2, 1)
		Glayout.addWidget(self.PassLine, 2, 2)

		Glayout1 = QtGui.QGridLayout()
		# Glayout1.addWidget(orcl_user, 1,1)
		# Glayout1.addWidget(self.Orcl_UserLine, 1, 2)
		Glayout1.addWidget(orcl_passwrd, 2, 1)
		Glayout1.addWidget(self.Orcl_PassLine, 2, 2)
		Glayout1.addWidget(self.Button, 3,2)

		v2layout = QtGui.QVBoxLayout()
		v2layout.addLayout(vlayout)
		v2layout.addLayout(Glayout)
		v2layout.addLayout(vlayout1)
		v2layout.addLayout(Glayout1)

		self.setCentralWidget(form_widget)
		form_widget.setLayout(v2layout)

		self.center()
		self.show()

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
		self.Button.keyPressEvent(e)

	def keyReleaseEvent(self, e):
		if e.key() == QtCore.Qt.Key_Return:
			e = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease,
								QtCore.Qt.Key_Space,
								e.modifiers(),
								e.text(),
								e.isAutoRepeat(),
								e.count())

		self.Button.keyReleaseEvent(e)

	def authenticate_user(self):
		try:
			datameer_requests.get_user_info(str(self.UserLine.text()), str(self.PassLine.text()))
			OracleDb.check_dbCredentials(str(self.UserLine.text()), str(self.Orcl_PassLine.text()))
			self.close()

			self.wind = Ui_MainWindow(user= str(self.UserLine.text()), passwrd = str(self.PassLine.text()),
									  oracle_pass= str(self.Orcl_PassLine.text()))
			self.wind.show()

		except IOError:
			if self.UserLine.text()== "":
				QtGui.QMessageBox.warning(
					  self, 'Error', 'UserID field is Empty')

			elif self.PassLine.text()== "":
				QtGui.QMessageBox.warning(
					  self, 'Error', 'Password field is Empty')

			elif self.Orcl_PassLine.text()== "":
				QtGui.QMessageBox.warning(
					  self, 'Error', 'Oracle Password field is Empty')


			else:
				QtGui.QMessageBox.warning(
					  self, 'Error', 'Incorrect UserName or Password')

		except ConfigParser.Error as e:
			QtGui.QMessageBox.critical(
				self, 'config file error','Check default_config.cfg file:\n {0}'.format(e))


	def center(self):
			qr = self.frameGeometry()
			cp = QtGui.QDesktopWidget().availableGeometry().center()
			qr.moveCenter(cp)
			self.move(qr.topLeft())

if __name__ == "__main__":
	import sys

	app = QtGui.QApplication(sys.argv)
	gui = User_Widget(argv = sys.argv)
	sys.exit(app.exec_())
