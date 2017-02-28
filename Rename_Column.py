import json
from PyQt4 import QtGui, QtCore
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from StyleSet import stylish



class Column_Window(QtGui.QWidget):
	def __init__(self, id = None, sheet= None,  user=None, coder = None):
		QtGui.QWidget.__init__(self)
		stylish(self)
		self.id = id
		self.sheet = sheet
		self.user = user
		self.passwrd = coder

		check_API(self.id, self.sheet, self.user, self.passwrd)
		self.val = jsons
		mygroupbox = QtGui.QGroupBox()
		myform = QtGui.QFormLayout()
		self.font = QtGui.QFont()
		palette = QtGui.QPalette()

		self.font.setPointSize(12)
		self.font.setBold(True)
		self.font.setWeight(50)


		if len(jsons)==0:
			self.msgbox = QtGui.QMessageBox()
			self.msgbox.setWindowTitle("Error")
			self.msgbox.setText("Cannot Edit Columns for this sheet because Columns have dependencies")
			self.msgbox.exec_()


		else:
			# Labels are getting generated dynamically
			self.setWindowTitle('Rename Column')
			for key, vals in self.val.items():
				exec('label = QtGui.QLabel("Formulas :")')
				exec( 'label'+str(key)+'=QtGui.QLabel("'+str(vals)+'")')
				exec( 'label'+str(key)+'.setFixedWidth(250)' )
				exec('label'+str(key)+'.setPalette(palette)')
				exec('label'+str(key)+'.setFont(self.font)')
				exec('label'+str(key)+'.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)')

			# TextField are generated dynamically
				exec( 'self.myLineEdit'+str(key)+'=QtGui.QLineEdit()' )
				exec('self.myLineEdit'+str(key)+'.setPalette(palette)')
				exec('self.myLineEdit'+str(key)+'.setFont(self.font)')
				if '.' in str(vals):
					exec( 'self.myLineEdit'+str(key)+'.setText("'+ str(vals).split('.')[1] +'")' )
				else:
					exec( 'self.myLineEdit'+str(key)+'.setText("'+ str(vals) +'")' )

				exec( 'myform.addRow(label'+str(key)+',self.myLineEdit'+str(key)+')' )


			mygroupbox.setLayout(myform)

			ButtonBox = QtGui.QGroupBox()
			ButtonsLayout = QtGui.QHBoxLayout()

			Button_01 = QtGui.QPushButton("Post")
			Button_01.clicked.connect(self.post_json)

			Button_02 = QtGui.QPushButton("Recover")
			Button_02.clicked.connect(self.backup_button)


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


	def post_json(self):
		lst = {}
		for key, vals in self.val.items():
			lst[key] = (str(eval( 'self.myLineEdit'+str(key)+'.text()' )))
		print lst
		replace(lst)


	def backup_button(self):
		recover_data()

	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())



def check_API(id, sheet, user, passwrd):
	global backup
	global userid
	global password
	global idd

	idd = id
	userid = user
	password = passwrd
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)   #auth=("luod", "luod1")
	data = requests.get("https://datameer.labcorp.com:8443/rest/workbook/%d" %id,  auth=(user, passwrd),
						verify=False)
	backup = data

	if data.status_code != 200:
		raise IOError("Sheet Not Found" + str(data.status_code))

	get_column_name(data=data, sheet=sheet)


def recover_data():
	backup_data = backup.json()
	r = requests.put("https://datameer.labcorp.com:8443/rest/workbook/%d" %idd,  data=json.dumps(backup_data, indent=4), headers ={'Content-Type':'application/json'} , auth=(userid, password), verify=False)
	if r.status_code==200:
		msgbox = QtGui.QMessageBox()
		msgbox.setWindowTitle("Successful Recovery ")
		msgbox.setText("JSON Recovered Successfully \n Status Code = 200 (Successful)")
		msgbox.exec_()

	else:
		msgbox = QtGui.QMessageBox()
		msgbox.setWindowTitle("Error")
		msgbox.setText("Cannot Post: Some Error Occured  \n Server Error: %s" % str(r.status_code))
		msgbox.exec_()

def get_column_name(data=None, sheet=None):
	global collect_json_data
	collect_json_data = data.json()

	search(collect_json_data=collect_json_data, sheet = sheet )



def search(collect_json_data=None, sheet = None):
	global jsons
	global sheetName
	sheetName = sheet
	jsons = {}

	for index, data in enumerate(collect_json_data['sheets']):

		if data['name'] == sheetName:
			for item in data:
				if 'formulas' in item:

					if any('(' in data['formulas'][i]['formulaString'] for i, v in enumerate(data['formulas'])):
						return False
					if any(')' in data['formulas'][i]['formulaString'] for i, v in enumerate(data['formulas'])):
						return False
					else:
						for i in data['formulas']:
							jsons[i['columnId']]=i['columnName']



def replace(replace_word):

	for index, data in enumerate(collect_json_data['sheets']):

		if data['name'] == sheetName:
			for i in data:
				if 'formulas' in i:

					for i, v in enumerate(data['columnStyles']) :
						print data['columnStyles'][i]['name']
						for key, vals in replace_word.items():
							if data['columnStyles'][i]['columnId'] == key:
								data['columnStyles'][i]['name'] = replace_word[key]

	r = requests.put("https://datameer.labcorp.com:8443/rest/workbook/%d" %idd, data=json.dumps(collect_json_data, indent=4), headers ={'Content-Type':'application/json'} , auth=(userid, password), verify=False)

	if r.status_code==200:
		msgbox = QtGui.QMessageBox()
		msgbox.setWindowTitle("Success")
		msgbox.setText("JSON posted Successfully")
		msgbox.exec_()

	else:
		msgbox = QtGui.QMessageBox()
		msgbox.setWindowTitle("Error")
		msgbox.setText("Cannot Post: Some Error Occured  \n Server Error: %s" % str(r.status_code))
		msgbox.exec_()


if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	window = Column_Window()
	sys.exit(app.exec_())

