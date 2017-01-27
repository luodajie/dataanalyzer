import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PyQt4 import QtGui
import cx_Oracle
import OracleDb


g_userid = ''
g_password = ''

def get_sheets(id, workbook_number):
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	r = requests.get('https://datameer.labcorp.com:8443/rest/data/workbook/%d' % id, auth=(g_userid,g_password), verify=False)
	if r.status_code != 200:
		raise IOError('WorkBook ID'+' '+ workbook_number + ' does not exists !!')
	js = r.json()
	path = js['path']
	names = [elem['name'] for elem in js['datas'][0]['sheets']]
	return (path, names)

def get_user_info(userid, password):
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	r = requests.get('https://datameer.labcorp.com:8443/rest/user-management/logged-in-user?pretty', auth=(userid,password), verify=False)
	if r.status_code != 200:
		raise IOError('Incorrect Datameer UserID or Password')

	#login success, keep userid and password in glabal variables
	global g_userid
	global g_password
	g_userid = userid
	g_password = password

	return str(r.text)

def check_dbCredentials(userid, password):
	try:
		con = cx_Oracle.connect(userid, password, dsn='rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com')
		OracleDb.user = userid
		OracleDb.passwrd = password


	except cx_Oracle.DatabaseError as e:
		error, = e.args
		if error.code == 1017:
			msgBox = QtGui.QMessageBox()
			msgBox.setText("Please Enter Correct Oracle Password")
			msgBox.show()
		else:
			raise IOError
			print('Database connection error: {0}'.format(e))

		raise