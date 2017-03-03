import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json


g_userid = ''
g_password = ''

def get_sheets(id):
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	r = requests.get('https://datameer.labcorp.com:8443/rest/data/workbook/%d' % id, auth=(g_userid,g_password), verify=False)
	if r.status_code != 200:
		raise IOError('WorkBook ID '+ str(id) + ' does not exist!')
	js = r.json()
	path = js['path']
	names = [elem['name'] for elem in js['datas'][0]['sheets']]
	return (path, names)

def get_column_sheets(id):
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	r = requests.get('https://datameer.labcorp.com:8443/rest/workbook/%d' % id, auth=(g_userid,g_password), verify=False)
	if r.status_code != 200:
		raise IOError('ID '+ str(id) + ' does not exist!')
	js = r.json()
	path = js['file']['path']
	names = []
	for index, data in enumerate(js['sheets']):
		names.append(data['name'])

	return (path, names)
	
def get_workbook_json(id):
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)   
	r = requests.get("https://datameer.labcorp.com:8443/rest/workbook/%d" % id,  auth=(g_userid,g_password), verify=False)
	if r.status_code != 200:
		raise IOError('Workbook ID '+ str(id) + ' Not Found!')
	return r.json()
	
def post_workbook_json(id, json_data):
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)   
	r = requests.put("https://datameer.labcorp.com:8443/rest/workbook/%d" % id,  data=json.dumps(json_data, indent=4), headers ={'Content-Type':'application/json'} , auth=(g_userid,g_password), verify=False)
	if r.status_code != 200:
		raise IOError('Cannot post JSON to Datameer.')
	return r.status_code

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
	
def get_data(id, sheetname):
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	r = requests.get('https://datameer.labcorp.com:8443/rest/data/workbook/%d/%s/download' % (id, sheetname), auth=(g_userid,g_password), verify=False)
	if r.status_code != 200:
		raise IOError('Request failed')
	return r.text

