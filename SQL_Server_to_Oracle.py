import pyodbc
import re
import cx_Oracle
import pandas as pd
from PyQt4 import QtGui
import ProgressBar_Gui

def check_row_count(user_oracle=None, passwrd=None, req_num=None, test_num=None, start_date=None, end_date=None):
	# Microsoft ODBC Driver 13.1
	driver = '{ODBC Driver 13 for SQL Server}'
	server = 'rtwamd09'
	database = 'azLAB_Combined'
	trust = 'yes'

	connection = pyodbc.connect(
		'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';Trusted_Connection=' + trust + '')
	cursor = connection.cursor()

	test_numbers = str(test_num).replace(" ", "")
	split_operation = test_numbers.split(',')
	modified = "'{0}'".format("', '".join(split_operation))

	start = str(start_date)
	end = str(end_date)
	start_insert = re.sub(r'(\d\d\d\d)(\d\d)(\d\d)', r'\1-\2-\3', start)
	end_insert = re.sub(r'(\d\d\d\d)(\d\d)(\d\d)', r'\1-\2-\3', end)

	list3 = []

	stmt =  "select r.universalserviceid order_code, count(*) as order_count "\
			"from [azLAB_Combined].[dbo].[OBR601] r (NOLOCK) "\
			"where r.universalserviceid in (%s) "\
			"and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s' "\
			"group by r.universalserviceid " \
			"union all " \
			"select r.universalserviceid order_code, count(*) order_count " \
			"from [azPATH_Combined].[dbo].[OBR601] r (NOLOCK) " \
			"where r.universalserviceid in (%s) " \
			"and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s' " \
			"group by r.universalserviceid;" % (modified, start_insert, end_insert,
											    modified, start_insert, end_insert)

	cursor.execute(stmt)

	data = cursor.fetchall()

	for d in data:
		print d
		if d[1] > 10000:
			raise IOError("can't process as the count is too high for %s" % d[0])
		else:
			list3.append(d[0])

	df = pd.DataFrame(list3, columns=['order_code'])
	print df

	cursor.close()
	connection.close()
	create_temp_table(start_insert, end_insert, list(df['order_code']), user_oracle=user_oracle, passwrd=passwrd, req_num=req_num)
	
	return ",".join(list3)
	


def create_temp_table(start_insert, end_insert, test_num = [], user_oracle= None, passwrd =None, req_num=None):
	# Microsoft ODBC Driver 13.1
	driver = '{ODBC Driver 13 for SQL Server}'
	server = 'rtwamd09'
	database = 'azLAB_Combined'
	trust = 'yes'

	connection = pyodbc.connect(
		'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';Trusted_Connection=' + trust + '')
	cursor = connection.cursor()

	list2= []

	stmt = "select distinct r.eid into #EIDS " \
			"from [azLAB_Combined].[dbo].[OBR601] r (NOLOCK) " \
			"where r.universalserviceid in ('%s') " \
			"and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s' " \
			"union all " \
			"select distinct r.eid " \
			"from [azPATH_Combined].[dbo].[OBR601] r (NOLOCK) " \
			"where r.universalserviceid in ('%s') " \
			"and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s';" % ("', '".join(test_num), start_insert, end_insert,
																			  "', '".join(test_num), start_insert, end_insert)

	cursor.execute(stmt)

	cursor.execute("SELECT * FROM #EIDS")

	data = cursor.fetchall()
	for d in data:
		list2.append(d[0])
		
	df = pd.DataFrame(list2, columns=['eid'])
	#print df

	collect_data(test_num = test_num, connection=connection, cursor=cursor, user_oracle=user_oracle, passwrd=passwrd, req_num=req_num)


def collect_data(test_num = [], connection=None, cursor= None, user_oracle= None, passwrd= None, req_num= None):
	modified = "'{0}'".format("', '".join(test_num))

	print "ORD_ACCTS:"

	stmt1 = "select a.eid, r.universalserviceid, r.universalservicename, upper(ltrim(rtrim(pd.LName))) + upper(ltrim(rtrim(pd.FName))) + convert(VARCHAR(10), pd.DOB, 120) as pseudo_lpid, " \
			"pd.DOB, pd.sex, ac.AccountNumber as ORDERING_ACCT_NUM, ac.accountmailingnamefirstline as ACCOUNT_FACILITY, ac.accountmailingaddressstreet as ACCOUNT_ADDRESS, " \
			"ac.AccountMailingAddressState as ACCOUNT_ST, ac.AccountMailingAddressZipCode as ACCOUNT_Zip, pd.orderingphysiciannpi as PHYS_NPI, a2.OIDexternal as lpid, r.FillerOrderNo, " \
			"r.observationdttm as draw_date " \
			"into #ORD_ACCTS " \
			"from " \
			"#EIDS a, " \
			"[azLAB_Combined].[dbo].[OBR601] r (NOLOCK), " \
			"[azADT_Combined].[dbo].[PID601] pd (NOLOCK), " \
			"[azADT_Combined].[dbo].[ACNT601] ac (NOLOCK), " \
			"[azAEID].[dbo].[AEID203] a1 (NOLOCK), " \
			"[azAEID].[dbo].[AEID204] a2 (NOLOCK) " \
			"where a.eid=r.eid and universalserviceid in (%s) and a.eid=pd.eid and pd.Account = ac.AccountNumber and a.eid = a1.EIDforSOID and a1.OID = a2.OID " \
			"union all " \
			"select a.eid, r.universalserviceid, r.universalservicename, upper(ltrim(rtrim(pd.LName))) + upper(ltrim(rtrim(pd.FName))) + convert(VARCHAR(10), pd.DOB,120) as pseudo_lpid, " \
			"pd.DOB, pd.sex, ac.AccountNumber as ORDERING_ACCT_NUM, ac.accountmailingnamefirstline as ACCOUNT_FACILITY, ac.accountmailingaddressstreet as ACCOUNT_ADDRESS, " \
			"ac.AccountMailingAddressState as ACCOUNT_ST, ac.AccountMailingAddressZipCode as ACCOUNT_Zip, pd.orderingphysiciannpi as PHYS_NPI, a2.OIDexternal as lpid, r.FillerOrderNo, " \
			"r.observationdttm as draw_date " \
			"from " \
			"#EIDS a, " \
			"[azPATH_Combined].[dbo].[OBR601] r (NOLOCK), " \
			"[azADT_Combined].[dbo].[PID601] pd (NOLOCK), " \
			"[azADT_Combined].[dbo].[ACNT601] ac (NOLOCK), " \
			"[azAEID].[dbo].[AEID203] a1 (NOLOCK), " \
			"[azAEID].[dbo].[AEID204] a2 (NOLOCK) " \
			"where a.eid=r.eid and universalserviceid in (%s) and a.eid=pd.eid and pd.Account = ac.AccountNumber and a.eid = a1.EIDforSOID and a1.OID = a2.OID;" % (modified, modified)

	cursor.execute(stmt1)

	stt = "select * from #ORD_ACCTS"
	cursor.execute(stt)
	ord_accts_table_data = cursor.fetchall()
	#for d in ord_accts_table_data:
	#	print d

	print "TESTS:"

	stmt2 = "SELECT oa.pseudo_lpid, oa.FillerOrderNo, oa.DOB, oa.sex, oa.lpid, oa.phys_npi, oa.ordering_acct_num, oa.account_facility, oa.account_address, oa.account_st, oa.account_zip, " \
			"p.eid, p.observationdttm as draw_date, p.observresultstatus, p.universalserviceid as order_code, oa.universalservicename as order_name, p.observationid, p.observation, " \
			"p.units_code, left(replace(replace(replace(p.observationvalue,char(13),''),char(10),''),char(9),''),600) as observationvalue " \
			"into #TESTS " \
			"FROM " \
			"#EIDS a, " \
			"#ord_accts oa, " \
			"[azLAB_Combined].[dbo].[OBX601] p (NOLOCK) " \
			"where a.eid=p.eid and a.eid = oa.eid and p.universalserviceid in (%s) " \
			"union all " \
			"SELECT oa.pseudo_lpid, oa.FillerOrderNo, oa.DOB, oa.sex, oa.lpid, oa.phys_npi, oa.ordering_acct_num, oa.account_facility, oa.account_address, oa.account_st, oa.account_zip, " \
			"p.eid, p.observationdttm as draw_date, p.observresultstatus, p.universalserviceid as order_code, oa.universalservicename as order_name, p.observationid, p.observation, " \
			"p.units_code, left(replace(replace(replace(p.observationvalue,char(13),''),char(10),''),char(9),''),600) as observationvalue " \
			"FROM " \
			"#EIDS a, " \
			"#ord_accts oa, " \
			"[azPATH_Combined].[dbo].[OBX601] p (NOLOCK) " \
			"where a.eid=p.eid and a.eid = oa.eid and p.universalserviceid in (%s);" % (modified, modified)
	
	cursor.execute(stmt2)
	
	stt2 = "select * from #TESTS"
	cursor.execute(stt2)
	tests_table_data = cursor.fetchall()
	#for d in tests_table_data:
	#	print d
		
	cursor.close()
	connection.close()
	
	row_length = len(ord_accts_table_data) + len(tests_table_data)
	check_existing_table(ord_accts_table_data, tests_table_data , user=str(user_oracle), passwrd=str(passwrd), req_num=str(req_num))


def check_existing_table(ord_accts_table_data, tests_table_data, user=None, passwrd=None, req_num=None):
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

	insert_data_trends_ords_table(ord_accts_table_data, user, passwrd, req_num)
	insert_data_trends_rslt_table(tests_table_data, user, passwrd, req_num)

	cur1.close()
	cur.close()
	con.close()


def create_trends_ords_table(trends_demo_tablename, cur, req_num):
	create_stmt = "CREATE TABLE TRENDS_DEMO_%s (EID VARCHAR2(80),ORDER_CODE VARCHAR2(60),ORDER_NAME VARCHAR2(512),PSEUDO_LPID VARCHAR2(130),DATE_OF_BIRTH DATE,PATIENT_SEX VARCHAR2(50), " \
				  "ORDERING_ACCT_NUM VARCHAR2(8),ACCOUNT_FACILITY VARCHAR2(30),ACCOUNT_ADDRESS VARCHAR2(35), " \
				  "ACCOUNT_ST VARCHAR2(2),ACCOUNT_ZIP VARCHAR2(5),NPI_NUM VARCHAR2(50),LPID VARCHAR2(256),FILLERORDERNO VARCHAR2(60),DRAW_DATE DATE)" % req_num

	drop_stmt = "DROP TABLE TRENDS_DEMO_%s" % req_num
	
	grant_stmt = "GRANT SELECT ON TRENDS_DEMO_%s TO PUBLIC" % req_num

	if trends_demo_tablename:
		print "Table Found:", trends_demo_tablename[0]
		cur.execute(drop_stmt)
		print "Table Dropped"
		
	cur.execute(create_stmt)
	cur.execute(grant_stmt)
	print "Table Created"

def create_trends_rslts_table(trends_result_tablename, cur1, req_num):
	create_stmt1 = "CREATE TABLE TRENDS_RESULTS_%s (PSEUDO_LPID VARCHAR2(130),FILLERORDERNO VARCHAR2(60),DATE_OF_BIRTH DATE,PATIENT_SEX VARCHAR2(50),LPID VARCHAR2(256),NPI_NUM VARCHAR2(50),ORDERING_ACCT_NUM VARCHAR2(8), " \
				   "ACCOUNT_FACILITY VARCHAR2(30),ACCOUNT_ADDRESS VARCHAR2(35),ACCOUNT_ST VARCHAR2(2), " \
				   "ACCOUNT_ZIP VARCHAR2(5),EID VARCHAR2(80),DRAW_DATE DATE,OBSERVRESULTSTATUS VARCHAR2(60), " \
				   "ORDER_CODE VARCHAR2(100),ORDER_NAME VARCHAR2(512),TEST_NUMBER VARCHAR2(60),TEST_NAME VARCHAR2(150), " \
				   "UNITS_CODE VARCHAR2(60),OBSERVATIONVALUE VARCHAR2(3500))" % req_num

	drop_stmt1 = "DROP TABLE TRENDS_RESULTS_%s" % req_num
	
	grant_stmt1 = "GRANT SELECT ON TRENDS_RESULTS_%s TO PUBLIC" % req_num

	if trends_result_tablename:
		print "Table Found:", trends_result_tablename[0]
		cur1.execute(drop_stmt1)
		print "Table Dropped"

	cur1.execute(create_stmt1)
	cur1.execute(grant_stmt1)
	print "Table Created"

def insert_data_trends_ords_table(ord_accts_table_data, user, passwrd, req_num):
	table = "TRENDS_DEMO_%s" % req_num
	dsn = 'rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com'

	con = cx_Oracle.connect(user=user, password=passwrd, dsn=dsn)
	cur = con.cursor()

	cur.bindarraysize = len(ord_accts_table_data)
	cur.setinputsizes(80, 60, 512, 130, 10, 50, 8, 30, 35, 2, 5, 50, 256, 60, 10)
	cur.executemany(
		"INSERT INTO "+ table +" (EID, ORDER_CODE, ORDER_NAME, PSEUDO_LPID, DATE_OF_BIRTH, PATIENT_SEX, ORDERING_ACCT_NUM, ACCOUNT_FACILITY, "
		"ACCOUNT_ADDRESS, ACCOUNT_ST, ACCOUNT_ZIP, NPI_NUM, LPID, FILLERORDERNO, DRAW_DATE) VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15 )", ord_accts_table_data)

	con.commit()
	print "Ord_accts Inserted"

	cur.close()
	con.close()


def insert_data_trends_rslt_table(tests_table_data, user, passwrd, req_num):
	table = "TRENDS_RESULTS_%s" % req_num
	dsn = 'rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com'

	con = cx_Oracle.connect(user=user, password=passwrd, dsn=dsn)
	cur = con.cursor()

	cur.bindarraysize = len(tests_table_data)
	cur.setinputsizes(130, 60, 10, 50, 256, 50, 8, 30, 35, 2, 5, 80, 10, 60, 100, 512, 60, 150, 60, 3500)
	cur.executemany(
		"INSERT INTO "+ table +" (PSEUDO_LPID, FILLERORDERNO, DATE_OF_BIRTH, PATIENT_SEX, LPID, NPI_NUM, ORDERING_ACCT_NUM, ACCOUNT_FACILITY, ACCOUNT_ADDRESS, ACCOUNT_ST, ACCOUNT_ZIP, EID, "
		"DRAW_DATE, OBSERVRESULTSTATUS, ORDER_CODE, ORDER_NAME, TEST_NUMBER, TEST_NAME, UNITS_CODE, OBSERVATIONVALUE) "
		"VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20 )", tests_table_data)

	con.commit()
	print "Tests Inserted"

	cur.close()
	con.close()


if __name__ == '__main__':
	import sys

	check_row_count()
	app = QtGui.QApplication(sys.argv)





