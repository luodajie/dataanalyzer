from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
import matplotlib.pyplot as plt
from matplotlib import style
from PyQt4 import QtGui

style.use('ggplot')


class MatplotScatWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MatplotScatWidget, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setGeometry(180, 90, 1000, 620)
        self.canvas = FigureCanvas(plt.figure())
        self.canvas.setWindowOpacity(1)
        self.canvas.setObjectName("canvas")
        self.canvas.resize(800, 620)
        plt.xlabel("Result")
        plt.ylabel("Count")
        plt.grid(True)
        plt.title("Numerical Scatter Graph \n Result v/s Count")
        self.canvas.draw()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setObjectName("toolbar")
        self.setStyleSheet("""
                QWidget{
                    background-color: rgb(230, 230, 230);
                    color: rgb(89, 89, 89);
                }
                """)
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)
        self.layoutVertical.addWidget(self.toolbar)

    def print_g1(self, fnum=None):
        plt.rcParams.update({'figure.max_open_warning': 0})
        plt.clf()
        plt.scatter(fnum.result, fnum.Count,
                    color='#ff944d', s=30)

        plt.xlabel("Result")
        plt.ylabel("Count")

        plt.title("Numerical Scatter Graph \n Result v/s Count")
        plt.grid(linestyle='-', linewidth='0.5', color='#333333')
        self.canvas.draw()
