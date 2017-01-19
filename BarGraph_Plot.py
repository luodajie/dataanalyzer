from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
import matplotlib.pyplot as plt
from matplotlib import style
from PyQt4 import QtGui


style.use('ggplot')


class MatplotBarWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MatplotBarWidget, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setGeometry(180, 90, 1000, 620)
        self.canvas = FigureCanvas(plt.figure())
        self.canvas.setWindowOpacity(1)
        self.canvas.setObjectName("bar-canvas")
        self.canvas.resize(800, 620)
        plt.xlabel("Result")
        plt.ylabel("Count")
        plt.grid(True)
        plt.title("Categorical bar Graph \n Result v/s Count")
        self.canvas.draw()
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setObjectName("bar-toolbar")
        self.setStyleSheet("""
                #bar-toolbar{
                    background-color: #cccccc;
                }
                """)
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)
        self.layoutVertical.addWidget(self.toolbar)

    def print_g2(self, f_alph=None):
        plt.rcParams.update({'figure.max_open_warning': 0})
        z = []
        for i in range(len(f_alph)):
            z.append(i)
        plt.bar(z, f_alph.Count, color='#ff6666', align='center')
        plt.xticks(z, f_alph.result, rotation='vertical')

        plt.xlabel("Result")
        plt.ylabel("Count")

        plt.title("Categorical bar Graph \n Result v/s Count")
        plt.grid(linestyle='-', linewidth='0.5', color='#333333')
        plt.margins(0.01)
        self.canvas.draw()
