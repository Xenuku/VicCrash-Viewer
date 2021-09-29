import sqlite3
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap
from functions.user_period import find_data
import time

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Sleep for 2 seconds to allow the splash screen to be shown THEN load the data
        self.data = sqlite3.connect('./data/crash.db')
        
        #window settings
        self.setWindowTitle("VicCrash Viewer")
        self.width = 1500
        self.height = 1000
        self.resize(self.width, self.height)
        self.move(50, 10)


        # Define navigation buttons as per system design

        # Logo (needs replacing with better quality)
        self.logo_label = QLabel(self)
        self.logo = QtGui.QPixmap('./data/logo.png').scaled(320, 230)
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
        #### Search/date boxes/inputs
        # "Label"
        self.keyword_search_box = QGroupBox("Search Term")
        # The input box, will grab value for search
        self.keyword_search_input = QLineEdit(self)
        self.keyword_search_input.setPlaceholderText("Enter Keyword")
       
        # Creating a nice 'label' similar to the design documents
        # Adding the input to the 'label' box
        self.keyword_search_layout = QVBoxLayout(self.keyword_search_box)
        self.keyword_search_layout.addStretch(2)
        self.keyword_search_box.setLayout(self.keyword_search_layout)
        self.keyword_search_layout.addWidget(self.keyword_search_input)
        self.keyword_search_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)

        # The start date label and input, need to set a 'min' date from the data
        self.start_date_input_box = QGroupBox("Start Date")
        # Calendar input, will get date for search
        self.start_date_input = QDateEdit(calendarPopup=True)
        self.start_date_input.setDateTime(QtCore.QDateTime.currentDateTime())
        # "Label"
        self.start_date_layout = QVBoxLayout(self.start_date_input_box)
        self.start_date_layout.addStretch(2)
        self.start_date_input_box.setLayout(self.start_date_layout)
        self.start_date_layout.addWidget(self.start_date_input)
        self.start_date_input_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)

        # The end date label and input, need to set a 'max' date from the data
        self.end_date_input_box = QGroupBox("End Date")
        self.end_date_input = QDateEdit(calendarPopup=True)
        self.end_date_input.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_date_layout = QVBoxLayout(self.end_date_input_box)
        self.end_date_layout.addStretch(2)
        self.end_date_input_box.setLayout(self.end_date_layout)
        self.end_date_layout.addWidget(self.end_date_input)
        self.end_date_input_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)
        # Search button label and button linked to homePagePerformSearch function, that passes data to user_period.py
        self.search_box = QGroupBox("Search")
        self.search_button = QPushButton('Go', self)
        self.search_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.search_button.clicked.connect(self.homePagePerformSearch)
        self.search_layout = QVBoxLayout(self.search_box)
        self.search_layout.addStretch(2)
        self.search_box.setLayout(self.search_layout)
        self.search_layout.addWidget(self.search_button)
        self.search_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)

        # All all the above 'labels' and inputs into a layout ref: labelsandinputs
        self.search_input_holder = QGroupBox()
        self.input_button_holders = QGridLayout(self)
        self.input_button_holders.addWidget(self.keyword_search_box, 0, 0, 1, 2)
        self.input_button_holders.addWidget(self.start_date_input_box, 0, 2, 1, 1)
        self.input_button_holders.addWidget(self.end_date_input_box, 0, 3, 1, 1)
        self.input_button_holders.addWidget(self.search_box, 0, 4, 1, 1)
        self.search_input_holder.setLayout(self.input_button_holders)

        # Data view 
        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setMinimumHeight(900)
        self.tableView.setModel(self.model)
        cursor = self.data.cursor()
        alldata = cursor.execute("SELECT * FROM crashdata")
        # Set the headers - we could manually name them to look nicer, but atm they're just
        # Grabbing column names from DB
        self.model.setHorizontalHeaderLabels(description[0].replace("ACCIDENT_", "") for description in cursor.description)
        for row in alldata.fetchall():
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
        tab_layout.addWidget(self.search_input_holder) # This is labelsandinputs being added to the main tab
        tab_layout.addWidget(self.tableView) # The data view, will need to update this when the search has returned data
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

    #############
    # Functions #
    #############
    def homePagePerformSearch(self):
        find_data(self.start_date_input.date(), self.end_date_input.date(), self.keyword_search_input.text(), self.data)


###########################
# Running the application #
###########################
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pixmap = QPixmap('data/logo.png').scaled(400, 400)
    splash = QSplashScreen(pixmap)
    splash.show()

    mainApp = Window()
    splash.finish(mainApp)
    
    mainApp.setStyleSheet("""
        QMainWindow {
            background-color: rgb(45, 57, 69);
        }
    """)
    mainApp.show()

    sys.exit(app.exec_())