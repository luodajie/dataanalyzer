import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
import pandas as pd
import numpy as np
from io import StringIO
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ScatterGraph_Plot import MatplotScatWidget
from BarGraph_Plot import MatplotBarWidget
from StyleSet import stylish
from Categorical_table_View import PandasModel
import OracleDb
from pyqtgraph.widgets.TableWidget import TableWidget
from functools import partial



def close_application():
    sys.exit()


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None, sheet=None, id=0, user= None, coder= None):
        super(Window, self).__init__(parent)

        self.sheet = sheet
        self.id = id
        self.user = user
        self.coder = coder
        self.setWindowOpacity(0.9)
        self.widget = QtGui.QWidget()
        self.widget.setObjectName("MainWidget")

        self.pushButtonPlot = QtGui.QPushButton()
        self.label = QtGui.QLabel()
        self.testLabel = QtGui.QLabel()
        self.label1 = QtGui.QLabel()
        self.list_layout = QtGui.QHBoxLayout()
        self.test_layout = QtGui.QGridLayout()
        self.table_layout = QtGui.QHBoxLayout()
        self.grid_layout = QtGui.QGridLayout()
        self.layoutVertical = QtGui.QVBoxLayout()
        stylish(self.widget)
        self.setGeometry(50, 50, 1300, 900)
        self.setWindowTitle("Data-Analyzer")
        self.setWindowIcon(QtGui.QIcon("analytic-icon.png"))

        extract_action = QtGui.QAction("Quit Screen", self)
        extract_action.setShortcut("Ctrl+Q")
        extract_action.setStatusTip("Quit 'Ctrl+Q'")
        extract_action.triggered.connect(close_application)

        self.listWidget = QtGui.QListWidget()
        self.listWidget.setGeometry(50, 100, 50, 600)
        self.listWidget.resize(2, 6)
        self.listWidget.setObjectName("mylist")

        self.oraclelistWidget = QtGui.QListWidget()
#         self.oraclelistWidget.setGeometry(50, 100, 50, 600)
        self.oraclelistWidget.resize(2, 6)
        self.oraclelistWidget.setObjectName("myOracle")

        self.tableWidget = QtGui.QTableView()
        self.tableWidget.setGeometry(1000, 100, 100, 600)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget.setObjectName("mytable")

        self.read(self.listWidget)

        self.f_alph = None

        self.statusBar()
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("&Quit")
        file_menu.addAction(extract_action)

        self.plot_scat = MatplotScatWidget()

        self.center()
        self.home()
        self.setCentralWidget(self.widget)
        self.show()

    def home(self):
        self.pushButtonPlot.setObjectName("pushButton")
        self.pushButtonPlot.setText("Get Categorical Graph")
        self.pushButtonPlot.move(50, 50)
        self.pushButtonPlot.resize(100, 200)

        self.label.setText("Test Numbers")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.testLabel.setText("Test Name")
        self.testLabel.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont()
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.white)
        self.label.setPalette(palette)
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.testLabel.setPalette(palette)
        self.testLabel.setFont(font)

        self.label1.setObjectName("label1")
        self.label1.setText("Categorical Data")
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setFont(font)
        self.label1.setPalette(palette)

        self.list_layout.addStretch()
        self.list_layout.addWidget(self.listWidget)
        self.list_layout.addWidget(self.oraclelistWidget)
        self.list_layout.addStretch()

        self.test_layout.addWidget(self.label, 0,1)
        self.test_layout.addWidget(self.testLabel, 0,2)

#         self.table_layout.addStretch()
        self.table_layout.addWidget(self.tableWidget)
#         self.table_layout.addStretch()

        self.grid_layout.addLayout(self.test_layout, 0,1)
        self.grid_layout.addWidget(self.label1, 0, 4)
        self.grid_layout.addLayout(self.list_layout, 1, 1)
        self.grid_layout.addWidget(self.pushButtonPlot, 1, 3)
        self.grid_layout.addLayout(self.table_layout, 1, 4)

        self.layoutVertical.addLayout(self.grid_layout)
        self.pushButtonPlot.clicked.connect(self.on_pushbutton_clicked)
        self.widget.setLayout(self.layoutVertical)

        self.layoutVertical.addWidget(self.plot_scat)

    @pyqtSlot("QModelIndex")
    def my_list(self, index):
        self.listWidget.setEnabled(False)
        self.layoutVertical.removeWidget(self.plot_scat)
        self.plot_scat = MatplotScatWidget()
        self.layoutVertical.addWidget(self.plot_scat)
        self.read(tx=index.text())


    def read(self, list_widget=None, tx=0):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        r = requests.get("https://datameer.labcorp.com:8443/rest/data/workbook/{0}/{1}/download".format(self.id, self.sheet), auth=(self.user, self.coder), verify=False)
        df = pd.read_csv(StringIO(r.text))
        df_str = pd.read_table(StringIO(r.text), sep=',', names=['test_number','result','Count'])
        test_val = df_str.test_number.unique().tolist()
        OracleDb.testName_fetcher(test_number = test_val, orcllw=self.oraclelistWidget)
        test_val.pop(0)
        if list_widget is not None:
            self.create_test_list(test_val, list_widget)
        else:
            self.generate_num_alph(df=df, tx=tx)
            QtCore.QTimer.singleShot(0.01, partial(self.listWidget.setEnabled, True))

    def generate_num_alph(self, df, tx):
        df1 = pd.DataFrame(df['result'])
        df2 = pd.to_numeric(df1['result'], errors='coerce')
        df1['result'] = df2
        # number list
        t = df.ix[df1.dropna().index.values]
        t['result'] = t.result.astype('float')

        # alpha list

        index = df1['result'].index[df1['result'].apply(np.isnan)]

        z = df.ix[index]

        # Selecting data according to test numbers
        q = t[t['test_number'] == float(tx)].groupby('result')['Count'].sum()
        plot_scat_val = pd.DataFrame(q, columns=['Count'])
        plot_bar_val = z[z['test_number'] == float(tx)][:20]

        self.plot_scat.print_g1(fnum=plot_scat_val)

        # Sending results in dbconnect.py and fetching description from database
        describe = OracleDb.description_fetcher(plot_bar_val=plot_bar_val['result'])

        # Below line will remove the false positive warning
        pd.options.mode.chained_assignment = None  # default='warn'

        # _____Joining two dataFrames_____
        descr= pd.DataFrame({'description':[i for i in describe]} , index = plot_bar_val.index)

        join_df = plot_bar_val.join(descr)

        model = PandasModel(join_df.ix[:, 1:4])
        # self.tableWidget.reset()
        self.draw_table(model)


        self.f_alph = plot_bar_val

    def create_test_list(self, read_test_num, list_widget):
        for i in read_test_num:
            list_widget.addItem(str(i))


        self.listWidget.itemClicked.connect(self.my_list)

    def draw_table(self, model):
        self.tableWidget.setModel(model)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_pushbutton_clicked(self):
        # scatter graph is not being updated because another instance of same class is created here as window.
        # needed to be resolved.
        plot_bar = MatplotBarWidget()
        plot_bar.setWindowTitle("Categorical Graph")
        plot_bar.setWindowIcon(QtGui.QIcon("icon.png"))
        plot_bar.print_g2(self.f_alph)
        plot_bar.show()


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
