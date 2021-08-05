import csv
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget

class MainWindow(QtWidgets.QWidget):
    def __init__(self, csvData, parent=None):
        super(MainWindow, self).__init__(parent)

        self.csvData = csvData
        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        # Graph button
        self.functionsButton = QtWidgets.QPushButton(self)
        self.functionsButton.setText("Visualisation and Search Tools")
        self.functionsButton.clicked.connect(self.loadGraphPage_pressed)

        self.loadDataButton = QtWidgets.QPushButton(self)
        self.loadDataButton.setText("Load Crash Data")
        self.loadDataButton.clicked.connect(self.loadDataButton_pressed)


        # Set up the layout
        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.loadDataButton)
        self.layoutVertical.addWidget(self.functionsButton)

    def loadGraphPage(self, csvData):
        fatalities = 0
        # TODO: Move this to another file with all functions? 
        # TODO: Rename functions to something better
        # TODO: Make this work lol
        months = ["Feb", "Mar", "Apr", "May", 
                  "Jun", "Jul", "Aug", "Sep", 
                  "Oct", "Nov", "Dec"
                ]
        with open(csvData, "r") as graphData:
            for row in csv.reader(graphData):
                if type(row[4]) == str:
                    continue
                if row[45] == "Yes":
                    print("Alcohol found")
        print(fatalities)
        # plt.plot(months, fatalities, label="test")
        # plt.xlabel('test')
        # plt.ylabel('test')
        # plt.show()

        # #What to plot
        # plt.plot(fatalaties, months, label="Test")
        # #Labels of what youre plotting
        # plt.xlabel('Fatalaties')
        # plt.ylabel('Months')
        # #Title of the graph
        # plt.title("Testing!!")
        # plt.legend()
        # #showing the graph
        # plt.show()

    def loadCrashData(self, csvData):
        with open(csvData, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)

    @QtCore.pyqtSlot()
    def loadDataButton_pressed(self):
        self.loadCrashData(self.csvData)

    @QtCore.pyqtSlot()
    def loadGraphPage_pressed(self):
        self.loadGraphPage(self.csvData)

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Victoria Accidents Viewer")

    main = MainWindow("data/Crash Statistics Victoria.csv")
    main.resize(1200, 800)
    main.move(30, 30)
    main.show()

    sys.exit(app.exec_())