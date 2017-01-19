from PyQt4 import QtCore, QtGui
from StyleSet import stylish
import datameer_requests
from Analysis_Gui import Window

class WorkBookMain(QtGui.QMainWindow):
    def __init__(self, parent=None, user = None, passwrd = None):
        super(WorkBookMain, self).__init__(parent)
        self.user = user
        self.passwrd = passwrd
        self.setGeometry(70,70,841,591)
        stylish(self)
        title = QtGui.QLabel()
        title.setText("\t\tWelcome\n Please Enter WorkBook Id and select files ")
        title.setAlignment(QtCore.Qt.AlignCenter)
        self.setWindowTitle("Workbook")

        font = QtGui.QFont()
        palette = QtGui.QPalette()
        # palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.white)
        title.setPalette(palette)
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        title.setFont(font)


        self.widget = QtGui.QWidget()

        graphicsView = QtGui.QGraphicsView()
        graphicsView.setGeometry(QtCore.QRect(70, 70, 841, 591))

        label1 = QtGui.QLabel()
        label1.setText("WorkBook ID :")

        self.lineEdit = QtGui.QLineEdit()
        self.lineEdit.setGeometry(QtCore.QRect(260, 120, 491, 21))
        self.lineEdit.setPlaceholderText("Enter WorkBook Id here and then press Enter")
        self.lineEdit.editingFinished.connect(self.editing_finished)
        self.lineEdit.textEdited.connect(self.text_edited)

        self.label2 = QtGui.QLabel()
        self.label2.setText("WorkBook Name: ")

        self.label3= QtGui.QLabel()

        label4 = QtGui.QLabel()
        label4.setText("Choose File : ")

        self.listWidget = QtGui.QListWidget()
        self.listWidget.setGeometry(QtCore.QRect(70, 70, 841, 391))


        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.file_transfer)
        self.buttonBox.rejected.connect(self.reset)

        self.button_group = QtGui.QButtonGroup()

        glayout = QtGui.QGridLayout()
        glayout.addWidget( self.label2, 0,1)
        glayout.addWidget( self.label3, 0,2)

        self.vlayout = QtGui.QVBoxLayout()
        self.vlayout.addWidget(title)
        self.vlayout.addWidget(label1)
        self.vlayout.addWidget(self.lineEdit)
        self.vlayout.addLayout(glayout)
        self.vlayout.addWidget(label4)
        self.vlayout.addWidget(self.listWidget)
        self.vlayout.addWidget(self.buttonBox)

        graphicsView.setLayout(self.vlayout)
        self.widget.setLayout(self.vlayout)
        self.setCentralWidget(self.widget)

        self.center()
        self.show()

    def editing_finished(self):
        # print("Editing finished!")
        # This signal is emitted when the Return or Enter key is pressed or the line edit loses focus.
        id = self.lineEdit.text()
        lst_rd=[]
        try:
            (path, names) = datameer_requests.get_sheets(int(id))  # 259
            self.label3.setText(path)
            self.listWidget.clear()



            for name in names:
                if name not in lst_rd:
                    lst_rd.append(name)
            # ------------------------START---------------------------------------
                    listItem = QtGui.QListWidgetItem(name, self.listWidget)
                    self.radio_btn = QtGui.QRadioButton("{0}".format(name))
                    self.vlayout.addWidget(self.radio_btn)
                    self.button_group.addButton(self.radio_btn)
                    self.listWidget.addItem(listItem)
                    self.listWidget.setItemWidget(listItem, self.radio_btn)
            self.listWidget.setFocus()
                # self.connect(self.button_group.checkedButton().text(), QtCore.SIGNAL("clicked()"), self.file_transfer)
            #--------------------------------END------------------------------------



        except ValueError:
            if self.lineEdit.text() == "":
                pass
            else:
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Critical)
                msg.setWindowTitle('Error')
                msg.setText("ID must be an integer!")
                msg.exec_()

                self.label3.setText('')
                self.listWidget.clear()

        except IOError as e:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Critical)
            msg.setWindowTitle('Error')
            msg.setText(str(e))
            msg.exec_()

            self.label3.setText('')
            self.listWidget.clear()

    def text_edited(self):
        # print("Text edited...")
        # This signal is emitted whenever the text is edited.
        self.label3.setText('')
        self.listWidget.clear()

#

    def file_transfer(self):


        # for i in range(self.listWidget.count()):
        #     listItem = self.listWidget.item(i)
        #     if listItem.checkState() == QtCore.Qt.Checked:
        name = self.button_group.checkedButton().text()
        id = self.lineEdit.text()
        wind = Window(self,id= int(id), sheet= name, user = self.user, coder = self.passwrd)
        wind.show()

            # if self.button_name.isChecked():
            #     name = self.button_name.text()
            #     id = self.lineEdit.text()
            #     wind = Window(self,id= int(id), sheet= name, user = self.user, coder = self.passwrd)
            #     wind.show()

    def reset(self):
        self.lineEdit.clear()
        self.label3.setText('')
        self.listWidget.clear()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    gui = WorkBookMain()
    sys.exit(app.exec_())

