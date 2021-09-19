import csv
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor
from functions.user_period import find_data

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = open('./data/Crash Statistics Victoria.csv', "r")
        #window settings
        self.setWindowTitle("VicCrash Viewer")
        self.width = 1500
        self.height = 1000
        self.resize(self.width, self.height)
        self.move(50, 10)


        # Define navigation buttons as per system design

        # Logo (needs replacing with better quality)
        self.logo_label = QLabel(self)
        self.logo = QtGui.QPixmap('./data/logo.jpg')
        self.logo_label.setPixmap(self.logo)
        
        # Sidebar buttons, styled in setupUI
        self.home = QPushButton('Home', self)
        self.home.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.home.clicked.connect(self.homeButton)

        self.tod = QPushButton('Time of Day', self)
        self.tod.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.tod.clicked.connect(self.todButton)
        

        self.alco = QPushButton('Alcohol', self)
        self.alco.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.alco.clicked.connect(self.alcoButton)        

        self.speed = QPushButton('Speed', self)
        self.speed.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.speed.clicked.connect(self.speedButton)
        

        self.homepage = self.homePage()
        self.speedpage = self.speedPage()
        self.todpage = self.todPage()
        self.alcoholpage = self.alcoholPage()

        self.setupUI()


    def setupUI(self):
        sidebar = QVBoxLayout()
        sidebar.addWidget(self.logo_label)
        sidebar.addWidget(self.home)
        sidebar.addWidget(self.tod)
        sidebar.addWidget(self.alco)
        sidebar.addWidget(self.speed)
        sidebar.addStretch(5)
        sidebar.setSpacing(20)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setStyleSheet(""" 
            QPushButton {
                background-color: rgb(205, 221, 172);
                color: rgb(45, 57, 69);
                font-weight: bold;
                font-size: 15px;
                height: 30px;
            }
            QPushButton:hover {
                background-color: rgb(255, 255, 255);
            }
        """)

        self.main_widget = QTabWidget()
        self.main_widget.tabBar().setObjectName("mainTab")

        self.main_widget.addTab(self.homepage, 'Home')
        self.main_widget.addTab(self.todpage, 'Time of Day')
        self.main_widget.addTab(self.alcoholpage, 'Alcohol')
        self.main_widget.addTab(self.speedpage, 'Speed')
        

        self.main_widget.setCurrentIndex(0)
        #Hide the tabs at the top, we're using the sidebar nav as per design doc
        self.main_widget.setStyleSheet("""
                QTabBar::tab {
                    width: 0; 
                    height: 0; 
                    margin: 0; 
                    padding: 0; 
                    border: none;
                } QTabWidget {
                    background-color: rgb(239, 243, 244);
                } QLabel {
                    color: rgb(44, 52, 57);
                    font-weight: bold;
                    font-size: 25px;
                }
                """)

        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.main_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_layout_widget = QWidget()
        main_layout_widget.setLayout(main_layout)
        self.setCentralWidget(main_layout_widget)
    
    ###################
    # Sidebar Buttons #
    ###################

    def homeButton(self):
        self.main_widget.setCurrentIndex(0)
    
    def todButton(self):
        self.main_widget.setCurrentIndex(1)

    def alcoButton(self):
        self.main_widget.setCurrentIndex(2)
    
    def speedButton(self):
        self.main_widget.setCurrentIndex(3)


    #########
    # PAGES #
    #########

    def homePage(self):
        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setMinimumHeight(900)
        self.tableView.setModel(self.model)
        for row in csv.reader(self.data):
            items = [
                QtGui.QStandardItem(field)
                for field in row
            ]
            self.model.appendRow(items)
        self.tableView.setStyleSheet(""" 
            QTableView {
                background-color: rgb(255, 255, 255);
                color: rgb(0, 0, 0);
            }
        """)
        shadow = QGraphicsDropShadowEffect(blurRadius=15, xOffset=1, yOffset=1)
        self.tableView.setGraphicsEffect(shadow)
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel('Accident Data'))
        tab_layout.addWidget(self.tableView)
        tab_layout.addStretch(5)
        tab = QWidget()
        tab.setLayout(tab_layout)
        return tab


    def todPage(self):
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel('Time of Day'))
        tab_layout.addStretch(5)
        tab = QWidget()
        tab.setLayout(tab_layout)
        return tab

    def alcoholPage(self):
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel('Alcohol'))
        tab_layout.addStretch(5)
        tab = QWidget()
        tab.setLayout(tab_layout)
        return tab

    def speedPage(self):
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(QLabel('Speed'))
        tab_layout.addStretch(5)
        tab = QWidget()
        tab.setLayout(tab_layout)
        return tab

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainApp = Window()
    mainApp.setStyleSheet("""
        QMainWindow {
            background-color: rgb(45, 57, 69);
        }
    """)
    mainApp.show()
    find_data("20", "20", "Yolo")

    sys.exit(app.exec_())