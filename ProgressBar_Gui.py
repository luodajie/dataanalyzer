from PyQt4 import QtGui, QtCore
import sys
import time


class Window(QtGui.QProgressDialog):
    def __init__(self, parent = None, data=None ):
        super(Window, self).__init__(parent)

        self.data = data
        print self.data

        self.pro = QtGui.QProgressDialog("Migrating Data...", "Cancel", 0, self.data)
        self.pro.setCancelButton(None)
        self.pro.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |QtCore.Qt.FramelessWindowHint)

        self.show_progress()

        self.message = message_display(parent)
        # self.message.show()

    def show_progress(self):
        # num = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

        for i in range(self.data):
            time.sleep(1)
            self.pro.setValue(i)

            if self.pro.value() == (self.pro.maximum()/2):
                self.pro.setLabelText("Inserting...")


        self.pro.setValue(self.data)






class message_display(QtGui.QMessageBox):
    def __init__(self, parent):
        super(message_display, self).__init__(parent)

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setStandardButtons(QtGui.QMessageBox.Ok)

        self.information(self, "Done!", "Done Migrating data !")






def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    gui.show()
    gui.close()
    sys.exit(app.exec_())




if __name__ == '__main__':
    main()