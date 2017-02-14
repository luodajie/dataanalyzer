import pyodbc
import re
import pandas as pd

def check_row_count():
	# Microsoft ODBC Driver 13.1
	driver = '{ODBC Driver 13 for SQL Server}'
	server = 'localhost'
	database = 'test'
	trust = 'yes'

	connection = pyodbc.connect(
		'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';Trusted_Connection=' + trust + '')
	cursor = connection.cursor()

	ord_act = raw_input('Enter ').replace(" ", "")
	ord_act1 = ord_act.split(',')
	modified = "'{0}'".format("', '".join(ord_act1))


	# print _insert
	# x =  ",".join(map(str,ord_act1))

	start = raw_input('start_date').replace('-', "")
	start_insert = re.sub(r'(\d\d\d\d)(\d\d)(\d\d)', r'\1-\2-\3', start)
	end = raw_input('end_data').replace('-', "")
	end_insert = re.sub(r'(\d\d\d\d)(\d\d)(\d\d)', r'\1-\2-\3', end)
																											   # 451852, 422160, 435480, 354280

	list3 = []

	stmt = "select r.universalserviceid order_code,  count(*) as order_count from [test].[dbo].[ACNT601] r (NOLOCK)"\
			"where r.universalserviceid in (%s)"\
			"and r.ObservationDtTm >= '%s' and r.ObservationDtTm <='%s' "\
			"group by r.universalserviceid " \
		   "union all" \
		   "select r.universalserviceid order_code,  count(*) order_count" \
		   "from [azPATH_Combined].[dbo].[OBR601] r (NOLOCK)" \
		   "where r.universalserviceid in (%s)" \
		   "and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s'" \
		   "group by r.universalserviceid;" %(modified, start_insert, end_insert,
											  modified, start_insert, end_insert)

	cursor.execute(stmt)

	data = cursor.fetchall()
	# data1 = data.split(',')

	for d in data:
		print d
		if d[1] > 10000:
			print "can't print as the data is too high in %s"%d[0]
			# pass

		else:
			# print d[0]
			list3.append(d[0])

	df = pd.DataFrame(list3, columns=['acct'])
	print df


		# list1, list2 = zip(*list)
	create_temp_table(start_insert, end_insert, list(df['acct']))
		# print list1
		# create_temp_table(user_oracle=user_oracle, passwrd=passwrd, req_num=req_num)
			#
	cursor.close()
	connection.close()


def create_temp_table(start_insert, end_insert, test_num = [] ):
	# x = ",".join(map(str, test_num))
	# y = x.split(',')
	# print tuple(y)
	# modified = "{0}".format("','".join(x))
	# for i in range(len(test_num)):
	# 	print test_num[i]
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


	stmt = "select distinct r.eid into #EIDS from [test].[dbo].[ACNT601] r (NOLOCK)" \
			"where r.universalserviceid in (%s)" \
			"and r.ObservationDtTm >= '%s' and r.ObservationDtTm <= '%s'" \
		   "union all" \
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

	fetch_data(eids_input=",".join(map(str,test_num)), cursor1=cursor1)

	cursor.close()
	connection.close()

def fetch_data(eids_input = None, cursor1= None):
	# modified = "'{0}'".format("', '".join(eids_input))


	print "Data is from ORD_ACCTS : "

	stmt1 = "select a.eid, r.universalserviceid,  upper(ltrim(rtrim(pd.LName))) + upper(ltrim(rtrim(pd.FName))) + convert(VARCHAR(10), pd.DOB,120) as pseudo_lpid," \
			"ac.AccountNumber as ORDERING_ACCT_NUM, ac.accountmailingnamefirstline as ACCOUNT_FACILITY, ac.accountmailingaddressstreet as ACCOUNT_ADDRESS," \
			"ac.AccountMailingAddressState as ACCOUNT_ST, ac.AccountMailingAddressZipCode as ACCOUNT_Zip, pd.orderingphysiciannpi as PHYS_NPI" \
			"into #ORD_ACCTS" \
			"from " \
			"#EIDS a," \
			"[azLAB_Combined].[dbo].[OBR601] r (NOLOCK)," \
			"[azADT_Combined].[dbo].[PID601] pd (NOLOCK), " \
			"[azADT_Combined].[dbo].[ACNT601] ac (NOLOCK)" \
			"where a.eid=r.eid and universalserviceid in (%s) and a.eid=pd.eid and pd.Account = ac.AccountNumber" \
			"union all" \
			"select a.eid, r.universalserviceid,  upper(ltrim(rtrim(pd.LName))) + upper(ltrim(rtrim(pd.FName))) + convert(VARCHAR(10), pd.DOB,120) as pseudo_lpid," \
			"ac.AccountNumber as ORDERING_ACCT_NUM, ac.accountmailingnamefirstline as ACCOUNT_FACILITY, ac.accountmailingaddressstreet as ACCOUNT_ADDRESS," \
			"ac.AccountMailingAddressState as ACCOUNT_ST, ac.AccountMailingAddressZipCode as ACCOUNT_Zip, pd.orderingphysiciannpi as PHYS_NPI" \
			"from " \
			"#EIDS a," \
			"[azPATH_Combined].[dbo].[OBR601] r (NOLOCK)," \
			"[azADT_Combined].[dbo].[PID601] pd (NOLOCK), " \
			"[azADT_Combined].[dbo].[ACNT601] ac (NOLOCK)" \
			"where a.eid=r.eid and universalserviceid in (%s) and a.eid=pd.eid and pd.Account = ac.AccountNumber;" % (eids_input, eids_input)


	cursor1.execute(stmt1)

	stt = "select * from #ORD_ACCTS"
	cursor1.execute(stt)
	abc1 = cursor1.fetchall()
	for d in abc1:
		print d

	print "Data is from TESTS : "

	stmt2 = "SELECT oa.phys_npi, oa.ordering_acct_num, oa.account_facility, oa.account_address, oa.account_st, oa.account_zip, " \
			"p.eid, p.observationdttm as draw_date, p.observresultstatus, p.universalserviceid as order_code, p.observationid, p.observation, " \
			"p.units_code, left(replace(replace(replace(p.observationvalue,char(13),''),char(10),''),char(9),''),600) as observationvalue " \
			"into #TESTS" \
			"FROM " \
			"#EIDS a," \
			"#ord_accts oa," \
			"[azLAB_Combined].[dbo].[OBX601] p (NOLOCK)" \
			"where a.eid=p.eid and a.eid = oa.eid and p.universalserviceid in (%s) " \
			"union all" \
			"SELECT oa.phys_npi, oa.ordering_acct_num, oa.account_facility, oa.account_address, oa.account_st, oa.account_zip, " \
			"p.eid, p.observationdttm as draw_date, p.observresultstatus, p.universalserviceid as order_code, p.observationid, p.observation, " \
			"p.units_code, left(replace(replace(replace(p.observationvalue,char(13),''),char(10),''),char(9),''),600) as observationvalue " \
			"FROM " \
			"#EIDS a," \
			"#ord_accts oa," \
			"[azPATH_Combined].[dbo].[OBX601] p (NOLOCK)" \
			"where a.eid=p.eid and a.eid = oa.eid and p.universalserviceid in (%s);" % (eids_input, eids_input)

	cursor1.execute(stmt2)
	stt_result = "select * from #TESTS"
	cursor1.execute(stt_result)
	abc_result = cursor1.fetchall()
	for d in abc_result:
		print d
	#
	data3 = len(abc1) + len(abc_result)

	print data3

	cursor1.close()




check_row_count()