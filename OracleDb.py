import cx_Oracle
import pandas as pd

user = None
passwrd = None

def testName_fetcher(test_number=None):
	
	con = cx_Oracle.connect(user=user, password= passwrd, dsn='rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com')
	cur = con.cursor()
	lst = []

	for i in test_number:
		cur.execute("select test_name from proddb2.trllr38_tst_master where test_number = '{0}' ".format(i))
		result = cur.fetchone()
		if result is not None:
			# removing () and , from the data
			lst.append(''.join(result))
		else:
			lst.append("None")

	cur.close()
	con.close()
	
	return lst

def description_fetcher(abbrv_list):

	con = cx_Oracle.connect(user=user, password= passwrd, dsn='rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com')
	cur = con.cursor()
	lst = []

	for val in abbrv_list:
		cur.execute("select expanded_text from luod.abbrv where abbrv = '{0}' ".format(val))
		data_tuple = cur.fetchone() #fetching single data from cursor
		if data_tuple is not None and len(data_tuple) > 0:
			lst.append(str(data_tuple[0]))
		else: 
			lst.append("None") 

	cur.close()
	con.close()
	
	return lst

def check_dbCredentials(userid, password):
	try:
		con = cx_Oracle.connect(userid, password, dsn='rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com')
		global user
		global passwrd
		user = userid
		passwrd = password
	except cx_Oracle.DatabaseError as e:
		error, = e.args
		if error.code == 1017:
			msgBox = QtGui.QMessageBox()
			msgBox.setText("Please Enter Correct Oracle Password")
			msgBox.show()
		else:
			print('Database connection error: {0}'.format(e))
			raise 
	except:
		raise