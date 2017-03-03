import json
import copy
from PyQt4 import QtGui, QtCore
import datameer_requests
from StyleSet import stylish



class Column_Window(QtGui.QWidget):
	def __init__(self, id = None, sheet= None,  user=None, coder = None):
		QtGui.QWidget.__init__(self)
		
		stylish(self)
		self.id = id #workbook id
		self.sheet = sheet
		self.user = user
		self.passwrd = coder

		self.get_column(self.id, self.sheet, self.user, self.passwrd)
		
		mygroupbox = QtGui.QGroupBox()
		myform = QtGui.QFormLayout()
		
		self.font = QtGui.QFont()
		palette = QtGui.QPalette()
		self.font.setPointSize(12)
		self.font.setBold(True)
		self.font.setWeight(50)


		if len(self.column_json)==0:
			self.msgbox = QtGui.QMessageBox()
			self.msgbox.setWindowTitle("Error")
			self.msgbox.setText("Cannot Edit Columns for this sheet because Columns have dependencies")
			self.msgbox.exec_()

		else:
			# Labels are getting generated dynamically
			self.setWindowTitle('Rename Column')
			for key, vals in self.column_json.items():
				exec('label'+str(key)+'=QtGui.QLabel("'+str(vals)+'")')
				exec('label'+str(key)+'.setFixedWidth(350)' )
				exec('label'+str(key)+'.setPalette(palette)')
				exec('label'+str(key)+'.setFont(self.font)')
				exec('label'+str(key)+'.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)')

			# TextField are generated dynamically
				exec('self.myLineEdit'+str(key)+'=QtGui.QLineEdit()' )
				exec('self.myLineEdit'+str(key)+'.setPalette(palette)')
				exec('self.myLineEdit'+str(key)+'.setFont(self.font)')
				if '.' in str(vals):
					exec('self.myLineEdit'+str(key)+'.setText("'+ str(vals).split('.')[-1] +'")' )
				else:
					exec('self.myLineEdit'+str(key)+'.setText("'+ str(vals) +'")' )

				exec( 'myform.addRow(label'+str(key)+',self.myLineEdit'+str(key)+')' )


			mygroupbox.setLayout(myform)

			ButtonBox = QtGui.QGroupBox()
			ButtonsLayout = QtGui.QHBoxLayout()

			Button_01 = QtGui.QPushButton("Post")
			Button_01.clicked.connect(self.post_json)

			Button_02 = QtGui.QPushButton("Recover")
			Button_02.clicked.connect(self.recover_data)

			ButtonsLayout.addWidget(Button_01)
			ButtonsLayout.addWidget(Button_02)

			ButtonBox.setLayout(ButtonsLayout)

			scroll = QtGui.QScrollArea()
			scroll.setWidget(mygroupbox)
			scroll.setWidgetResizable(True)
			scroll.setFixedHeight(800)
			layout = QtGui.QVBoxLayout(self)
			layout.addWidget(scroll)
			layout.addWidget(ButtonBox)
			self.setGeometry(500, 100, 800, 400)
			self.show()

			
	def get_column(self, id, sheet, user, passwrd):	
		self.collect_json = datameer_requests.get_workbook_json(id)
		self.backup_json = copy.deepcopy(self.collect_json)
		self.column_json = {}

		for index, data in enumerate(self.collect_json['sheets']):
			# data is dict for a sheet
			if data['name'] == sheet:
				# check if 'formulas' is in the keys of data
				if 'formulas' in data:
					if any('(' in data['formulas'][i]['formulaString'] for i, v in enumerate(data['formulas'])):
						return False
					if any(')' in data['formulas'][i]['formulaString'] for i, v in enumerate(data['formulas'])):
						return False
					else:
						for i in data['formulas']:
							self.column_json[i['columnId']]=i['columnName']

	def post_json(self):
		lst = {}
		for key, vals in self.column_json.items():
			lst[key] = (str(eval( 'self.myLineEdit'+str(key)+'.text()' )))
		self.replace(lst)

	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def recover_data(self):
		try:
			datameer_requests.post_workbook_json(self.id, self.backup_json)
		
			msgbox = QtGui.QMessageBox()
			msgbox.setWindowTitle("Successful Recovery")
			msgbox.setText("Recovered Successfully")
			msgbox.exec_()

		except IOError as e:
			msgbox = QtGui.QMessageBox()
			msgbox.setWindowTitle("Error")
			msgbox.setText(str(e))
			msgbox.exec_()

	def replace(self, replace_word):

		try:
			if len(replace_word.values()) != len(set(replace_word.values())):
				raise IOError('Duplicated Column Name Found!')
		
			for index, data in enumerate(self.collect_json['sheets']):
				if data['name'] == self.sheet:
					if 'formulas' in data:
						for i, v in enumerate(data['columnStyles']):
							for key, vals in replace_word.items():
								if data['columnStyles'][i]['columnId'] == key:
									data['columnStyles'][i]['name'] = replace_word[key]

		
			datameer_requests.post_workbook_json(self.id, self.collect_json)

			msgbox = QtGui.QMessageBox()
			msgbox.setWindowTitle("Success")
			msgbox.setText("JSON posted Successfully")
			msgbox.exec_()

		except IOError as e:
			msgbox = QtGui.QMessageBox()
			msgbox.setWindowTitle("Error")
			msgbox.setText(str(e))
			msgbox.exec_()


if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	window = Column_Window()
	sys.exit(app.exec_())

