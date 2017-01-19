import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import cx_Oracle
import OracleDb

g_userid = ''
g_password = ''

def get_sheets(id):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.get('https://datameer.labcorp.com:8443/rest/data/workbook/%d' % id, auth=(g_userid,g_password), verify=False)
    if r.status_code != 200:
        raise IOError('Request failed')
    js = r.json()
    path = js['path']
    names = [elem['name'] for elem in js['datas'][0]['sheets']]
#     print names
    return (path, names)

def get_user_info(userid, password):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.get('https://datameer.labcorp.com:8443/rest/user-management/logged-in-user?pretty', auth=(userid,password), verify=False)
    if r.status_code != 200:
        raise IOError('Request failed')
    
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
            raise IOError('Login Failed')
        else:
            raise IOError('Database connection error: {0}'.format(e))