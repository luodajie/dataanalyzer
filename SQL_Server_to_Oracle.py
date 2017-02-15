import pyodbc
import re
import cx_Oracle
import pandas as pd
from PyQt4 import QtGui
import ProgressBar_Gui

def check_row_count(user_oracle=None, passwrd=None, req_num=None, test_num=None, start_date=None, end_date=None):
	# Microsoft ODBC Driver 13.1
	driver = '{ODBC Driver 13 for SQL Server}'
	server = 'localhost'
	database = 'test'
	trust = 'yes'

	connection = pyodbc.connect(
		'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';Trusted_Connection=' + trust + '')
	cursor = connection.cursor()

	test_numbers = test_num.replace(" ", "")
	split_operation = test_numbers.split(',')
	modified = "'{0}'".format("', '".join(split_operation))

	start = str(start_date)
	end = str(end_date)
	start_insert = re.sub(r'(\d\d\d\d)(\d\d)(\d\d)', r'\1-\2-\3', start)
	end_insert = re.sub(r'(\d\d\d\d)(\d\d)(\d\d)', r'\1-\2-\3', end)

	list3 = []

	stmt = "select r.universalserviceid order_code,  count(*) as order_count from [azPATH_Combined].[dbo].[OBR601] r (NOLOCK) "\
			"where r.universalserviceid in (%s) "\
			"and r.ObservationDtTm >= '%s' and r.ObservationDtTm <='%s' "\
			"group by r.universalserviceid " \
		   "union all " \
		   "select r.universalserviceid order_code,  count(*) order_count " \
		   "from [azPATH_Combined].[dbo].[OBR601] r (NOLOCK)" \
		   "where r.universalserviceid in (%s) " \
		   "and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s'" \
		   "group by r.universalserviceid;" %(modified, start_insert, end_insert,
											  modified, start_insert, end_insert)

	cursor.execute(stmt)

	data = cursor.fetchall()

	for d in data:
		print d
		if d[1] > 10000:
			print "can't print as the data is too high in %s"%d[0]

		else:
			list3.append(d[0])

	df = pd.DataFrame(list3, columns=['acct'])
	print df

	create_temp_table(start_insert, end_insert, list(df['acct']), user_oracle=user_oracle, passwrd=passwrd, req_num=req_num)
	cursor.close()
	connection.close()


def create_temp_table(start_insert, end_insert, test_num = [], user_oracle= None, passwrd =None, req_num=None):
	# Microsoft ODBC Driver 13.1
	driver = '{ODBC Driver 13 for SQL Server}'
	server = 'localhost'
	database = 'test'
	trust = 'yes'

	connection = pyodbc.connect(
		'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';Trusted_Connection=' + trust + '')
	cursor = connection.cursor()
	cursor1 = connection.cursor()

	list2= []


	stmt = "select distinct r.eid into #EIDS from [azPATH_Combined].[dbo].[OBR601] r (NOLOCK) " \
			"where r.universalserviceid in (%s) " \
			"and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s' " \
		   "union all " \
		   "select distinct r.eid " \
		   "from [azPATH_Combined].[dbo].[OBR601] r (NOLOCK)" \
		   "where r.universalserviceid in (%s)" \
		   "and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s';"% (",".join(map(str,test_num)), start_insert, end_insert,
																			",".join(map(str,test_num)), start_insert, end_insert)

	cursor.execute(stmt)

	cursor.execute("SELECT * FROM #EIDS")

	data = cursor.fetchall()
	for d in data:
		list2.append(d[0])
		# fetch_data(d[0])
	# fetch_data(list)
	df = pd.DataFrame(list2, columns=['eid'])
	print df

	collect_data(eids_input=",".join(map(str,test_num)), cursor1=cursor1, user_oracle=user_oracle, passwrd=passwrd, req_num=req_num)

	cursor.close()
	connection.close()

def collect_data(eids_input = None, cursor1= None, user_oracle= None, passwrd= None, req_num= None):
	# modified = "'{0}'".format("', '".join(eids_input))


	print "Data is from ORD_ACCTS : "

	stmt1 = "select a.eid, r.universalserviceid,  upper(ltrim(rtrim(pd.LName))) + upper(ltrim(rtrim(pd.FName))) + convert(VARCHAR(10), pd.DOB,120) as pseudo_lpid, " \
			"ac.AccountNumber as ORDERING_ACCT_NUM, ac.accountmailingnamefirstline as ACCOUNT_FACILITY, ac.accountmailingaddressstreet as ACCOUNT_ADDRESS, " \
			"ac.AccountMailingAddressState as ACCOUNT_ST, ac.AccountMailingAddressZipCode as ACCOUNT_Zip, pd.orderingphysiciannpi as PHYS_NPI " \
			"into #ORD_ACCTS " \
			"from " \
			"#EIDS a, " \
			"[azLAB_Combined].[dbo].[OBR601] r (NOLOCK)," \
			"[azADT_Combined].[dbo].[PID601] pd (NOLOCK), " \
			"[azADT_Combined].[dbo].[ACNT601] ac (NOLOCK)" \
			"where a.eid=r.eid and universalserviceid in (%s) and a.eid=pd.eid and pd.Account = ac.AccountNumber " \
			"union all " \
			"select a.eid, r.universalserviceid,  upper(ltrim(rtrim(pd.LName))) + upper(ltrim(rtrim(pd.FName))) + convert(VARCHAR(10), pd.DOB,120) as pseudo_lpid, " \
			"ac.AccountNumber as ORDERING_ACCT_NUM, ac.accountmailingnamefirstline as ACCOUNT_FACILITY, ac.accountmailingaddressstreet as ACCOUNT_ADDRESS, " \
			"ac.AccountMailingAddressState as ACCOUNT_ST, ac.AccountMailingAddressZipCode as ACCOUNT_Zip, pd.orderingphysiciannpi as PHYS_NPI " \
			"from " \
			"#EIDS a, " \
			"[azPATH_Combined].[dbo].[OBR601] r (NOLOCK), " \
			"[azADT_Combined].[dbo].[PID601] pd (NOLOCK), " \
			"[azADT_Combined].[dbo].[ACNT601] ac (NOLOCK)" \
			"where a.eid=r.eid and universalserviceid in (%s) and a.eid=pd.eid and pd.Account = ac.AccountNumber;" % (eids_input, eids_input)


	cursor1.execute(stmt1)

	stt = "select * from #ORD_ACCTS"
	cursor1.execute(stt)
	ORD_ACCTS_table_data = cursor1.fetchall()
	for d in ORD_ACCTS_table_data:
		print d

	print "Data is from TESTS : "

	stmt2 = "SELECT oa.phys_npi, oa.ordering_acct_num, oa.account_facility, oa.account_address, oa.account_st, oa.account_zip, " \
			"p.eid, p.observationdttm as draw_date, p.observresultstatus, p.universalserviceid as order_code, p.observationid, p.observation, " \
			"p.units_code, left(replace(replace(replace(p.observationvalue,char(13),''),char(10),''),char(9),''),600) as observationvalue " \
			"into #TESTS " \
			"FROM " \
			"#EIDS a, " \
			"#ord_accts oa," \
			"[azLAB_Combined].[dbo].[OBX601] p (NOLOCK) " \
			"where a.eid=p.eid and a.eid = oa.eid and p.universalserviceid in (%s) " \
			"union all " \
			"SELECT oa.phys_npi, oa.ordering_acct_num, oa.account_facility, oa.account_address, oa.account_st, oa.account_zip, " \
			"p.eid, p.observationdttm as draw_date, p.observresultstatus, p.universalserviceid as order_code, p.observationid, p.observation, " \
			"p.units_code, left(replace(replace(replace(p.observationvalue,char(13),''),char(10),''),char(9),''),600) as observationvalue " \
			"FROM " \
			"#EIDS a, " \
			"#ord_accts oa," \
			"[azPATH_Combined].[dbo].[OBX601] p (NOLOCK)" \
			"where a.eid=p.eid and a.eid = oa.eid and p.universalserviceid in (%s);" % (eids_input, eids_input)

	cursor1.execute(stmt2)
	stt_result = "select * from #TESTS"
	cursor1.execute(stt_result)
	Tests_table_data = cursor1.fetchall()
	for d in Tests_table_data:
		print d
	#
	row_length = len(ORD_ACCTS_table_data) + len(Tests_table_data)

	ProgressBar_Gui.Window(data=row_length)

	check_existing_table(ORD_ACCTS_table_data, Tests_table_data , user=str(user_oracle), passwrd=str(passwrd),req_num=str(req_num))

	cursor1.close()

def check_existing_table(ORD_ACCTS_table_data, Tests_table_data, user=None, passwrd=None, req_num=None):
	dsn = 'rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com'

	con = cx_Oracle.connect(user=user, password=passwrd, dsn=dsn)
	cur = con.cursor()
	cur1 = con.cursor()

	# To check whether table exist or not:
	stmt = "SELECT tname FROM tab WHERE tname = 'TRENDS_DEMO_{}'".format(req_num)
	cur.execute(stmt)
	trends_demo_tablename = cur.fetchone()

	stmt1 = "SELECT tname FROM tab WHERE tname = 'TRENDS_RESULTS_{}'".format(req_num)
	cur1.execute(stmt1)
	trends_result_tablename = cur1.fetchone()

	create_trends_ords_table(trends_demo_tablename, cur, req_num)
	create_trends_rslts_table(trends_result_tablename, cur1, req_num)

	insert_data_trends_ords_table(ORD_ACCTS_table_data, user, passwrd,req_num)
	insert_data_trends_rslt_table(Tests_table_data, user, passwrd, req_num)

	cur1.close()
	cur.close()
	con.close()


def create_trends_ords_table(trends_demo_tablename, cur, req_num):
	create_stmt = "CREATE TABLE TRENDS_DEMO_%s (eid VARCHAR2(50),universalserviceid VARCHAR2(50),pseudo_lpid VARCHAR2(50), " \
				  "ORDERING_ACCT_NUM VARCHAR2(50),ACCOUNT_FACILITY VARCHAR2(50),ACCOUNT_ADDRESS VARCHAR2(50), " \
				  "ACCOUNT_ST VARCHAR2(50),ACCOUNT_Zip VARCHAR2(50),PHYS_NPI VARCHAR2(50))" %req_num

	drop_stmt = "DROP TABLE TRENDS_DEMO_%s" %req_num

	if trends_demo_tablename:
		print "Table FOUND:", trends_demo_tablename[0]
		cur.execute(drop_stmt)
		print "Table Dropped"
		cur.execute(create_stmt)
		print "Table created:", "AABB".upper()
	else:
		cur.execute(create_stmt)
		print "Table created from else:", "AABB".upper()


def create_trends_rslts_table(trends_result_tablename, cur1, req_num ):
	create_stmt1 = "CREATE TABLE TRENDS_RESULTS_%s (eid VARCHAR2(50),AccountNumber VARCHAR2(50), " \
				   "pseudo_lpid VARCHAR2(50),ORDERING_ACT_NUM VARCHAR2(50),ACCOUNT_FACILITY VARCHAR2(50), " \
				   "ACCOUNT_ADDRESS VARCHAR2(50),ACCOUNT_ST VARCHAR2(50),ACCOUNT_Zip VARCHAR2(50),PHYS_NPI VARCHAR2(50)," %req_num

	drop_stmt1 = "DROP TABLE TRENDS_RESULTS_%s"  %req_num

	if trends_result_tablename:
		print "Table FOUND:", trends_result_tablename[0]
		cur1.execute(drop_stmt1)
		print "Table Dropped"
		cur1.execute(create_stmt1)
		print "Table created:", "AACC".upper()
	else:
		cur1.execute(create_stmt1)
		print "Table created from else:", "AACC".upper()


#
# #
def insert_data_trends_ords_table(ORD_ACCTS_table_data, user, passwrd, req_num):
	table = "Trends_demo_%s" %req_num
	dsn = 'rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com'

	con = cx_Oracle.connect(user=user, password=passwrd, dsn=dsn)
	cur = con.cursor()

	cur.bindarraysize = len(ORD_ACCTS_table_data)
	cur.setinputsizes(50, 50, 50, 50, 50, 50, 50, 50, 50)
	cur.executemany(
		"INSERT INTO "+ table +" (eid,	universalserviceid,	pseudo_lpid, ORDERING_ACCT_NUM, ACCOUNT_FACILITY,	"
		"ACCOUNT_ADDRESS, ACCOUNT_ST, ACCOUNT_Zip, PHYS_NPI) VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9 )",ORD_ACCTS_table_data)

	con.commit()
	print "inserted in AABB"

	cur.close()
	con.close()


def insert_data_trends_rslt_table(Tests_table_data, user, passwrd, req_num):
	table = "Trends_results_%s" %req_num
	dsn = 'rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com'

	con = cx_Oracle.connect(user=user, password=passwrd, dsn=dsn)
	cur = con.cursor()

	cur.bindarraysize = len(Tests_table_data)
	cur.setinputsizes(50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50)
	cur.executemany(
		"INSERT INTO "+ table +" (phys_npi, ordering_acct_num ,account_facility ,account_address ,account_st ,account_zip ,eid ,"
		"draw_date ,observresultstatus ,order_code,observationid ,observation ,units_code ,"
		"observationvalue) VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14 )",Tests_table_data)

	con.commit()
	print "inserted in AACC"

	cur.close()
	con.close()


if __name__ == '__main__':
	import sys

	check_row_count()
	app = QtGui.QApplication(sys.argv)





