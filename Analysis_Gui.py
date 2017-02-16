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
from functools import partial
import datameer_requests



def close_application():
	sys.exit()


class Window(QtGui.QMainWindow):
	def __init__(self, parent=None, sheet=None, id=0, user= None, coder= None):
		super(Window, self).__init__(parent)

		self.sheet = sheet
		self.id = id
		self.user = user
		self.coder = coder
		self.setWindowOpacity(0.96)
		self.mainWidget = QtGui.QWidget()
		self.mainWidget.setObjectName("MainWidget")

		self.setWindowTitle("Data-Analyzer")
		self.setWindowIcon(QtGui.QIcon("analytic-icon.png"))
		
		self.numLabel = QtGui.QLabel()
		self.nameLabel = QtGui.QLabel()
		self.tableLabel = QtGui.QLabel()
		self.list_layout = QtGui.QHBoxLayout()
		self.label_layout = QtGui.QGridLayout()
		self.table_layout = QtGui.QHBoxLayout()
		self.grid_layout = QtGui.QGridLayout()
		self.main_layout = QtGui.QVBoxLayout()
		stylish(self.mainWidget)
		self.setGeometry(50, 50, 1300, 900)
		
		self.numLabel.setText("Test Number")
		self.numLabel.setAlignment(QtCore.Qt.AlignCenter)
		
		self.nameLabel.setText("Test Name")
		self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
		
		font = QtGui.QFont()
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(100)
		font.setFamily("Helvetica")
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.white)
		self.numLabel.setPalette(palette)
		self.numLabel.setFont(font)
		self.nameLabel.setPalette(palette)
		self.nameLabel.setFont(font)
		
		self.tableLabel.setObjectName("tableLabel")
		self.tableLabel.setText("Categorical Data")
		self.tableLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.tableLabel.setFont(font)
		self.tableLabel.setPalette(palette)

		extract_action = QtGui.QAction("Quit Screen", self)
		extract_action.setShortcut("Ctrl+Q")
		extract_action.setStatusTip("Quit 'Ctrl+Q'")
		extract_action.triggered.connect(close_application)

		self.testListWidget = QtGui.QListWidget()
		self.testListWidget.setGeometry(50, 100, 50, 600)
		self.testListWidget.resize(2, 6)
		self.testListWidget.setObjectName("testNumberList")
		self.testListWidget.itemClicked.connect(self.onTestNumSelected)

		self.nameListWidget = QtGui.QListWidget()
		self.nameListWidget.resize(2, 6)
		self.nameListWidget.setObjectName("testNameList")

		self.tableWidget = QtGui.QTableView()
		self.tableWidget.setGeometry(1000, 100, 100, 600)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.tableWidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignHCenter)
		self.tableWidget.setObjectName("abbrvTable")
		self.tableWidget.setLineWidth(50)
		self.tableWidget.setShowGrid(True)

		font = QtGui.QFont()
		font.setPointSize(11)
		font.setWeight(10)
		palette = QtGui.QPalette()
		self.tableWidget.setPalette(palette)
		self.tableWidget.setFont(font)
		self.testListWidget.setFont(font)
		self.nameListWidget.setFont(font)

		font_header = QtGui.QFont()
		palette_header = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)
		self.tableWidget.setPalette(palette_header)
		font_header.setPointSize(12)
		font_header.setWeight(30)
		stylesheet = "QHeaderView::section{Background-color:rgb(128, 128, 128);\
								   border-radius:14px; color: rgb(230, 230, 230);} * { gridline-color: gray }"
		self.tableWidget.setStyleSheet(stylesheet)
		self.tableWidget.horizontalHeader().setFont(font_header)
		# self.tableWidget.setAlternatingRowColors(True)

		
		self.barPlotButton = QtGui.QPushButton()
		self.barPlotButton.setObjectName("barPlotButton")
		self.barPlotButton.setText("Get Categorical Graph")
		self.barPlotButton.setStyleSheet( '''
		QPushButton	{
			color: #ffcc66
			}
			'''
		)
		self.barPlotButton.move(50, 50)
		self.barPlotButton.setFixedSize(150, 50)
		self.barPlotButton.clicked.connect(self.onBarPlotButtonClicked)
		
		self.list_layout.addStretch()
		self.list_layout.addWidget(self.testListWidget)
		self.list_layout.addWidget(self.nameListWidget)
		self.list_layout.addStretch()

		self.label_layout.addWidget(self.numLabel, 0,1)
		self.label_layout.addWidget(self.nameLabel, 0,2)

		self.table_layout.addWidget(self.tableWidget)
		# self.table_layout.addStretch()

		self.grid_layout.addLayout(self.label_layout, 0,1)
		self.grid_layout.addWidget(self.tableLabel, 0, 4)
		self.grid_layout.addLayout(self.list_layout, 1, 1)
		self.grid_layout.addWidget(self.barPlotButton, 1, 3)
		self.grid_layout.addLayout(self.table_layout, 1, 4)

		# scatter plot
		self.plot_scat = MatplotScatWidget()
		
		self.main_layout.addLayout(self.grid_layout)
		self.main_layout.addWidget(self.plot_scat)
		self.mainWidget.setLayout(self.main_layout)
		
		# initial test codes and names
		self.loadTest()
		
		# main_menu = self.menuBar()
		# file_menu = main_menu.addMenu("&Quit")
		# file_menu.addAction(extract_action)
		
		self.statusBar()
		self.center()
		self.setCentralWidget(self.mainWidget)
		self.show()

		
	def loadTest(self):
		# load data
		txt = datameer_requests.get_data(self.id, self.sheet)
		df = pd.read_csv(StringIO(txt), header=0, dtype={'test_number':str,'result':str,'Count':np.int64})
		test_numbers = df.test_number.unique().tolist()
		
		# keep data for efficiency
		self.data = df
		
		lst = OracleDb.testName_fetcher(test_number = test_numbers)
		self.nameListWidget.clear()
		for i in lst:
			self.nameListWidget.addItem(str(i))
			
		for i in test_numbers:
			self.testListWidget.addItem(str(i))


	def onTestNumSelected(self, index):
		self.testListWidget.setEnabled(False)
		test_number = self.testListWidget.currentItem().text()
		self.main_layout.removeWidget(self.plot_scat)
		self.plot_scat = MatplotScatWidget()
		self.main_layout.addWidget(self.plot_scat)
		
		# refresh scatter plot and alpha value table
		self.generate_numeric_alpha(tx=test_number)

		
	def generate_numeric_alpha(self, tx):
	
		df = self.data
		
		# Coerce alpha result to NaN
		df1 = pd.DataFrame(pd.to_numeric(df['result'], errors='coerce'))
		
		# Get numeric list
		t = df.ix[df1.dropna().index.values]
		t['result'] = t.result.astype('float')

		# Get alpha list
		index = df1['result'].index[df1['result'].apply(np.isnan)]
		z = df.ix[index]

		# Selecting data according to test number
		q = t[t['test_number'] == tx].groupby('result')['Count'].sum()
		numeric_values = q.to_frame().reset_index()
		alpha_values = z[z['test_number'] == tx].sort_values(by=['Count'],ascending=False)

		# Draw scatter plot
		self.plot_scat.print_g1(fnum=numeric_values)

		# Fetching description of alpha values from database
		desc = OracleDb.description_fetcher(abbrv_list=alpha_values['result'])

		# Below line will remove the false positive warning
		pd.options.mode.chained_assignment = None  # default='warn'

		# Joining description
		desc_df = pd.DataFrame({'description':desc}, index = alpha_values.index)



		wow = pd.DataFrame.to_dict(desc_df)
		print wow

		print wow['description']
		join_df = alpha_values.join(desc_df)
		
		# Display table
		model = PandasModel(join_df.ix[:, 1:4])
		# self.tableWidget.reset()
		self.tableWidget.setModel(model)
		# keep alpha values for bar chart
		self.data_alpha = alpha_values
		
		QtCore.QTimer.singleShot(0.01, partial(self.mySelectListItem))

	def mySelectListItem(self):
		self.testListWidget.setEnabled(True)
		self.nameListWidget.setCurrentRow(self.testListWidget.currentRow())

		testnumber_item = self.testListWidget.currentItem()
		testname_item = self.nameListWidget.currentItem()
		self.testListWidget.scrollToItem(testnumber_item, QtGui.QAbstractItemView.PositionAtTop)
		self.nameListWidget.scrollToItem(testname_item, QtGui.QAbstractItemView.PositionAtTop)
		
	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def onBarPlotButtonClicked(self):
		bar_plot = MatplotBarWidget()
		bar_plot.setWindowTitle("Categorical Graph")
		bar_plot.setWindowIcon(QtGui.QIcon("icon.png"))
		bar_plot.print_g2(self.data_alpha[:10]) # draw top 10 bars only
		bar_plot.show()



def main():
	app = QtGui.QApplication(sys.argv)
	gui = Window()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
