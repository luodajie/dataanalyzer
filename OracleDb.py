import cx_Oracle
import pandas as pd

user = None
passwrd = None
# lst_describe = []
def testName_fetcher(test_number= None, orcllw=None):
    # 'DWoct25$'
    con = cx_Oracle.connect(user=user, password= passwrd, dsn='rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com')
    cur = con.cursor()
    lst = []

    for i in test_number:

        cur.execute("select test_name from proddb2.trllr38_tst_master where test_number = '{0}' ".format(i))
        for result in cur:
#       # removing () and , from the data
            result = ' '.join(result)
            lst.append(result)


    df = pd.DataFrame({'test_name':lst})

    orcllw.clear()
    for index, row in df.iterrows():
            orcllw.addItem(str(row['test_name']))
           
        
    cur.close()
    con.close()

def description_fetcher(plot_bar_val):

    con = cx_Oracle.connect(user=user, password= passwrd, dsn='rtxa1-scan.labcorp.com:1521/lcadwp1.labcorp.com')
    cur = con.cursor()
    lst = []

    for val in plot_bar_val:
        cur.execute("select expanded_text from luod.abbrv where abbrv = '{0}' ".format(val))
        data_tuple = cur.fetchone() #fetching single data from cursor
        lst.append(data_tuple) if data_tuple else lst.append(" None ") # Single line ternary expression for if-else.

    return lst

        
    cur.close()
    con.close()
