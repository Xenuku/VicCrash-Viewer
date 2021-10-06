import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QPixmap
from functions.user_period import find_data
from functions.time_of_day import get_time_data
from functions.alcohol_incident import get_alcohol_incidents
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# Globally used across all pages for embedding charts
class PlotCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100, plotspot=111):
        fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.axes = fig.add_subplot(plotspot)
        self.axes.cla()

        FigureCanvas.__init__(self, fig)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = sqlite3.connect('./data/crash.db')
        
        # Window settings
        self.setWindowTitle("VicCrash Viewer")
        self.width = 1500
        self.height = 700
        self.resize(self.width, self.height)
        self.move(50, 10)

        self.logo_label = QLabel(self)
        self.logo = QtGui.QPixmap('./data/logo.png').scaled(250, 175)
        self.logo_label.setPixmap(self.logo)
        self.logo_label.setStyleSheet("padding-bottom: 30px;")
        
        # Sidebar buttons, styled in setupUI
        # Home Button nav button
        self.home = QPushButton('HOME', self)
        self.home.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.home.clicked.connect(self.homeButton)
        self.home.setFixedHeight(80)
        self.home.setAutoDefault(True)

        # Time of day nav button
        self.tod = QPushButton('TIME OF DAY', self)
        self.tod.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.tod.clicked.connect(self.todButton)
        self.tod.setFixedHeight(80)

        # Alcohol nav button
        self.alco = QPushButton('ALCOHOL', self)
        self.alco.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.alco.clicked.connect(self.alcoButton)
        self.alco.setFixedHeight(80) # Make it so the Home button is white on first load

        # Speed nav button
        self.speed = QPushButton('SPEED', self)
        self.speed.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.speed.clicked.connect(self.speedButton)
        self.speed.setFixedHeight(80)

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
        sidebar.setSpacing(0)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setStyleSheet(""" 
            QPushButton {
                background-color: rgb(205, 221, 172);
                color: rgb(45, 57, 69);
                font-weight: bold;
                font-size: 15px;
                height: 30px;
                border: 0.5px solid black;
                border-radius: 5px;
                margin: 0;
                width: 100%;
            }
            QPushButton:focus {
                background-color: rgb(255, 255, 255);
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
                } 
                QTabWidget {
                    background-color: rgb(239, 243, 244);
                } 
                QLabel {
                    color: rgb(44, 52, 57);
                    font-weight: bold;
                    font-size: 25px;
                }
                QTabWidget::pane {
                    border-radius: 10px;  
                    background-color: rgb(255, 255, 255);
                }
                """)

        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.main_widget)
        main_layout.setSpacing(-10)
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
        # Search/date boxes/inputs
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
        self.start_date_input.setDate(QtCore.QDate(2013, 7, 1))
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
        self.end_date_input.setDate(QtCore.QDate(2019, 3, 21))
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

         # Search button label and button linked to homePagePerformSearch function, that passes data to user_period.py
        self.reset_box = QGroupBox("Reset")
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.reset_button.clicked.connect(self.homePageResetTable)
        self.reset_layout = QVBoxLayout(self.reset_box)
        self.reset_layout.addStretch(2)
        self.reset_box.setLayout(self.reset_layout)
        self.reset_layout.addWidget(self.reset_button)
        self.reset_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)

        # All all the above 'labels' and inputs into a grid layout ref: labelsandinputs
        self.search_input_holder = QGroupBox()
        self.input_button_holders = QGridLayout(self)
        self.input_button_holders.addWidget(self.keyword_search_box, 0, 0, 1, 2)
        self.input_button_holders.addWidget(self.start_date_input_box, 0, 2, 1, 1)
        self.input_button_holders.addWidget(self.end_date_input_box, 0, 3, 1, 1)
        self.input_button_holders.addWidget(self.search_box, 0, 4, 1, 1)
        self.input_button_holders.addWidget(self.reset_box, 0, 5, 1, 1)
        self.search_input_holder.setLayout(self.input_button_holders)

        # Inserting data into the table
        self.model = QtGui.QStandardItemModel(self)
        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setMinimumHeight(700)
        self.tableView.setModel(self.model)
        cursor = self.data.cursor()
        alldata = cursor.execute("SELECT * FROM crashdata")
        # Set the headers - RAW data version as per software plan
        self.table_headers = [description[0].replace("ACCIDENT_", "") for description in cursor.description]
        self.model.setHorizontalHeaderLabels(self.table_headers)
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
        self.filter_start_date_input_box = QGroupBox("Start Date")
        self.filter_start_date_input = QDateEdit(calendarPopup=True)
        self.filter_start_date_input.setDate(QtCore.QDate(2013, 7, 1))
        self.filter_start_date_layout = QVBoxLayout(self.filter_start_date_input_box)
        self.filter_start_date_layout.addStretch(2)
        self.filter_start_date_input_box.setLayout(self.filter_start_date_layout)
        self.filter_start_date_layout.addWidget(self.filter_start_date_input)
        self.filter_start_date_input_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)

        # The end date label and input, need to set a 'max' date from the data
        self.filter_end_date_input_box = QGroupBox("End Date")
        self.filter_end_date_input = QDateEdit(calendarPopup=True)
        self.filter_end_date_input.setDate(QtCore.QDate(2019, 3, 21))
        self.filter_end_date_layout = QVBoxLayout(self.filter_end_date_input)
        self.filter_end_date_layout.addStretch(2)
        self.filter_end_date_input_box.setLayout(self.filter_end_date_layout)
        self.filter_end_date_layout.addWidget(self.filter_end_date_input)
        self.filter_end_date_input_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)

        # Search button label and button linked to todPagePerformFilterSearch function, that passes data to time_of_day.py
        self.filter_box = QGroupBox("Search")
        self.filter_button = QPushButton('Go', self)
        self.filter_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.filter_button.clicked.connect(self.todPagePerformFilterSearch)
        self.filter_layout = QVBoxLayout(self.filter_box)
        self.filter_layout.addStretch(2)
        self.filter_box.setLayout(self.filter_layout)
        self.filter_layout.addWidget(self.filter_button)
        self.filter_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)
        
        self.filter_input_holder = QGroupBox()
        self.filter_input_button_holders = QGridLayout(self)
        self.filter_input_button_holders.addWidget(self.filter_start_date_input_box, 0, 2, 1, 1)
        self.filter_input_button_holders.addWidget(self.filter_end_date_input_box, 0, 3, 1, 1)
        self.filter_input_button_holders.addWidget(self.filter_box, 0, 4, 1, 1)
        self.filter_input_holder.setLayout(self.filter_input_button_holders)

        initial_graph = get_time_data(self.filter_start_date_input.date(), self.filter_end_date_input.date(), self.data)
        rounded_time = []
        incident_count = []
        for row in enumerate(initial_graph):
            rounded_time.append(row[1][0])
            incident_count.append(row[1][1])

        self.todchart = PlotCanvas(self, width=10, height=10, dpi=100)
        self.todchart.axes.plot(rounded_time, incident_count, 'b--', label="Time of day trend")
        self.todchart.axes.set_xlabel("Time (24 hour)")
        self.todchart.axes.set_ylabel("Accidents (total)")
        self.todchart.axes.set_title('Average Accidents per hour')

       
        self.filter_tab_layout = QVBoxLayout()
        self.filter_tab_layout.addWidget(QLabel('Time of Day'))
        self.filter_tab_layout.addWidget(self.filter_input_holder)
        self.filter_tab_layout.addWidget(self.todchart) 
        self.filter_tab_layout.addStretch(5)
        tab = QWidget()
        tab.setLayout(self.filter_tab_layout)
        return tab

    def alcoholPage(self):
        self.alcohol_start_date_input_box = QGroupBox("Start Date")
        self.alcohol_start_date_input = QDateEdit(calendarPopup=True)
        self.alcohol_start_date_input.setDate(QtCore.QDate(2013, 7, 1))
        self.alcohol_start_date_layout = QVBoxLayout(self.alcohol_start_date_input_box)
        self.alcohol_start_date_layout.addStretch(2)
        self.alcohol_start_date_input_box.setLayout(self.alcohol_start_date_layout)
        self.alcohol_start_date_layout.addWidget(self.alcohol_start_date_input)
        self.alcohol_start_date_input_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)

        self.alcohol_end_date_input_box = QGroupBox("End Date")
        self.alcohol_end_date_input = QDateEdit(calendarPopup=True)
        self.alcohol_end_date_input.setDate(QtCore.QDate(2019, 3, 21))
        self.alcohol_end_date_layout = QVBoxLayout(self.alcohol_end_date_input)
        self.alcohol_end_date_layout.addStretch(2)
        self.alcohol_end_date_input_box.setLayout(self.alcohol_end_date_layout)
        self.alcohol_end_date_layout.addWidget(self.alcohol_end_date_input)
        self.alcohol_end_date_input_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)

        # Search button label and button linked to todPagePerformFilterSearch function, that passes data to time_of_day.py
        self.alcohol_box = QGroupBox("Search")
        self.alcohol_button = QPushButton('Go', self)
        self.alcohol_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.alcohol_button.clicked.connect(self.alcoholPageFilter)
        self.alcohol_layout = QVBoxLayout(self.alcohol_box)
        self.alcohol_layout.addStretch(2)
        self.alcohol_box.setLayout(self.alcohol_layout)
        self.alcohol_layout.addWidget(self.alcohol_button)
        self.alcohol_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)
        
        self.alcohol_input_holder = QGroupBox()
        self.alcohol_input_button_holders = QGridLayout(self)
        self.alcohol_input_button_holders.addWidget(self.alcohol_start_date_input_box, 0, 2, 1, 1)
        self.alcohol_input_button_holders.addWidget(self.alcohol_end_date_input_box, 0, 3, 1, 1)
        self.alcohol_input_button_holders.addWidget(self.alcohol_box, 0, 4, 1, 1)
        self.alcohol_input_holder.setLayout(self.alcohol_input_button_holders)

        initial_graph = get_alcohol_incidents(self.alcohol_start_date_input.date(), self.alcohol_end_date_input.date(), self.data)
        print('init', initial_graph)

        labels = []
        alcohol_incidents = []

        for row in enumerate(initial_graph[0]):
            labels.append(row[1][0])
            alcohol_incidents.append(row[1][1])
        x = np.arange(len(labels))
        bar_width = 0.5
        explode = [0.1, 0]
        wedges = {'linewidth':0}
        colors = ['#21E132', '#DB2DCE']

        self.alcohol_chart = PlotCanvas(self, width=5, height=5, dpi=100)
        self.alcohol_chart.axes.pie(list(initial_graph[1][0]), labels=["Alcohol Involved", "No Alcohol"], explode=explode, colors=colors, shadow=True, startangle=270, wedgeprops=wedges, autopct='%1.1f%%')
        self.alcohol_chart.axes.set_title('Alcohol vs No Alcohol related accidents')

        self.alcohol_chart_2 = PlotCanvas(self, width=8, height=6, dpi=100)
        self.alcohol_chart_2.axes.bar(x, alcohol_incidents, bar_width, label="Alcohol Involved")
        self.alcohol_chart_2.axes.set_xticks(x)
        xlabels = self.alcohol_chart_2.axes.set_xticklabels(labels)
        self.alcohol_chart_2.axes.set_ylabel("Accident amounts")
        for i, label in enumerate(xlabels):
            label.set_y(label.get_position()[1] - (i % 2) * 0.075)
        self.alcohol_chart_2.axes.set_title('Alcohol involved collisions')

        self.alcohol_tab_layout = QVBoxLayout()
        self.alcohol_tab_layout.addWidget(QLabel('Alcohol'))
        self.alcohol_tab_layout.addWidget(self.alcohol_input_holder)
        self.alcohol_tab_layout.addWidget(self.alcohol_chart)
        self.alcohol_tab_layout.addWidget(self.alcohol_chart_2)
        self.alcohol_tab_layout.addStretch(5)
        tab = QWidget()
        tab.setLayout(self.alcohol_tab_layout)
        return tab

    def speedPage(self):
        # Speed chart starting search date
        self.speed_start_date_input_box = QGroupBox("Start Date")
        self.speed_start_date_input = QDateEdit(calendarPopup=True)
        self.speed_start_date_input.setDate(QtCore.QDate(2013, 7, 1))
        self.speed_start_date_layout = QVBoxLayout(self.speed_start_date_input_box)
        self.speed_start_date_layout.addStretch(2)
        self.speed_start_date_input_box.setLayout(self.speed_start_date_layout)
        self.speed_start_date_layout.addWidget(self.speed_start_date_input)
        self.speed_start_date_input_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)
        # Speed chart end search date
        self.speed_end_date_input_box = QGroupBox("End Date")
        self.speed_end_date_input = QDateEdit(calendarPopup=True)
        self.speed_end_date_input.setDate(QtCore.QDate(2019, 3, 21))
        self.speed_end_date_layout = QVBoxLayout(self.speed_end_date_input_box)
        self.speed_end_date_layout.addStretch(2)
        self.speed_end_date_input_box.setLayout(self.speed_end_date_layout)
        self.speed_end_date_layout.addWidget(self.speed_end_date_input)
        self.speed_end_date_input_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
         """)
        
        # Speed chart filter button, connects to function speedPagePerformSearch
        self.speed_search_box = QGroupBox("Search")
        self.speed_search_button = QPushButton('Filter', self)
        self.speed_search_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.speed_search_button.clicked.connect(self.speedPagePerformSearch)
        self.speed_search_layout = QVBoxLayout(self.speed_search_box)
        self.speed_search_layout.addStretch(2)
        self.speed_search_box.setLayout(self.speed_search_layout)
        self.speed_search_layout.addWidget(self.speed_search_button)
        self.speed_search_box.setStyleSheet("""
            QGroupBox {
                color: black;
            }
        """)
        # holders for start and end speed dates
        self.speed_search_input_holder = QGroupBox()
        self.speed_input_button_holders = QGridLayout(self)
        self.speed_input_button_holders.addWidget(self.speed_start_date_input_box, 0, 2, 1, 1)
        self.speed_input_button_holders.addWidget(self.speed_end_date_input_box, 0, 3, 1, 1)
        self.speed_input_button_holders.addWidget(self.speed_search_box, 0, 4, 1, 1)
        self.speed_search_input_holder.setLayout(self.speed_input_button_holders)
        speed_start_date = self.speed_start_date_input.date().toString('yyyy-MM-dd')
        speed_end_date = self.speed_end_date_input.date().toString('yyyy-MM-dd')

        # grabbing crash data from specific speed zones
        speed_query = f"""
        SELECT  
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "40 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_start_date}') AND DATE('{speed_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "50 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_start_date}') AND DATE('{speed_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "60 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_start_date}') AND DATE('{speed_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "70 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_start_date}') AND DATE('{speed_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "80 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_start_date}') AND DATE('{speed_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "90 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_start_date}') AND DATE('{speed_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "100 km/hr" AND (DATE(accident_date)
                                BETWEEN DATE('{speed_start_date}') AND DATE('{speed_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "110 km/hr" AND (DATE(accident_date)
                                BETWEEN DATE('{speed_start_date}') AND DATE('{speed_end_date}')) );
        """
        cursor = self.data.cursor()
        speeddata = cursor.execute(speed_query)
        speed_results = speeddata.fetchall()
        speed_results = list(speed_results[0])
        
        
        self.speed_labels = [
            f'40 km/hr ({speed_results[0]})',
            f'50 km/hr ({speed_results[1]})', 
            f'60 km/hr ({speed_results[2]})', 
            f'70 km/hr ({speed_results[3]})', 
            f'80 km/hr ({speed_results[4]})', 
            f'90 km/hr ({speed_results[5]})', 
            f'100 km/hr ({speed_results[6]})',
            f'110 km/hr ({speed_results[7]})'
        ]
        explode = [0.3, 0, 0,0,0,0,0,0]
        wedges = {'linewidth':0}
        colors = ['#21E132', '#DB2DCE', '#D22424', '#2542D0', '#D9E72C', '#1BD8D3', '#D68919', '#6624E2']
        self.speed_chart = PlotCanvas(self, width=10, height=10, dpi=100)
        self.speed_chart.axes.pie(speed_results, explode=explode, labels=self.speed_labels, colors=colors, shadow=True, startangle=270, wedgeprops=wedges, autopct='%1.1f%%')
        self.speed_chart.axes.set_title('Number of Accidents per Speed Zone')

        self.speed_tab_layout = QVBoxLayout()
        self.speed_tab_layout.addWidget(QLabel('Speed'))
        self.speed_tab_layout.addWidget(self.speed_search_input_holder)
        self.speed_tab_layout.addWidget(self.speed_chart)
        self.speed_tab_layout.addStretch(5)
        tab = QWidget()
        tab.setLayout(self.speed_tab_layout)
        return tab

    #############
    # Functions #
    #############
    def homePagePerformSearch(self):
        self.search_results = find_data(self.start_date_input.date(), self.end_date_input.date(), self.keyword_search_input.text(), self.data)
        # Updating the page model to show search results
        self.search_results_model = QtGui.QStandardItemModel(self)
        # Set the headers of the filtered data
        self.search_table_headers = [
            "Accident No",
            "Status",
            "Date",
            "Time",
            "Type",
            "Day",
            "Alcohol?",
            "Hit 'n' Run?",
            "Lighting",
            "Police?",
            "Road Type",
            "Severity",
            "Speed limit",
            "Run offroad?",
            "Region",
            "Total Involved",
            "Fatality",
            "Serious Injury",
            "Injury",
            "Not Injured",
            "Males",
            "Females",
            "Old Drivers",
            "Young Drivers",
            "No license",
            "Num of Vehicles"
        ]
        self.search_results_model.setHorizontalHeaderLabels(self.search_table_headers)
        self.tableView.setModel(self.search_results_model)
        for row in self.search_results:
            items = [
                QtGui.QStandardItem(field)
                for field in row
            ]
            self.search_results_model.appendRow(items)
    
    # When the user wants to go back to the raw dataset instead of search results
    def homePageResetTable(self):
        self.tableView.setModel(self.model)
    
    def speedPagePerformSearch(self):
        # Update the chart data here
        cursor = self.data.cursor()
        speed_search_start_date = self.speed_start_date_input.date().toString('yyyy-MM-dd')
        speed_search_end_date = self.speed_end_date_input.date().toString('yyyy-MM-dd')
        speed_search_query = f"""
        SELECT  
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "40 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_search_start_date}') AND DATE('{speed_search_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "50 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_search_start_date}') AND DATE('{speed_search_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "60 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_search_start_date}') AND DATE('{speed_search_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "70 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_search_start_date}') AND DATE('{speed_search_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "80 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_search_start_date}') AND DATE('{speed_search_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "90 km/hr" AND (DATE(accident_date) 
                                BETWEEN DATE('{speed_search_start_date}') AND DATE('{speed_search_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "100 km/hr" AND (DATE(accident_date)
                                BETWEEN DATE('{speed_search_start_date}') AND DATE('{speed_search_end_date}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE speed_zone = "110 km/hr" AND (DATE(accident_date)
                                BETWEEN DATE('{speed_search_start_date}') AND DATE('{speed_search_end_date}')) );
        """
        speeddata = cursor.execute(speed_search_query)
        searched_speed_results = speeddata.fetchall()
        searched_speed_results = list(searched_speed_results[0])

        self.search_labels = [
            f'40 km/hr ({searched_speed_results[0]})',
            f'50 km/hr ({searched_speed_results[1]})', 
            f'60 km/hr ({searched_speed_results[2]})', 
            f'70 km/hr ({searched_speed_results[3]})', 
            f'80 km/hr ({searched_speed_results[4]})', 
            f'90 km/hr ({searched_speed_results[5]})', 
            f'100 km/hr ({searched_speed_results[6]})',
            f'110 km/hr ({searched_speed_results[7]})'
        ]
 
        # Remove the initial pie chart as it is no longer required.
        self.speed_tab_layout.removeWidget(self.speed_chart)
        # Delete the search results each time, update with new results
        if hasattr(self, 'searched_speed_chart'):
            self.speed_tab_layout.removeWidget(self.searched_speed_chart)
        explode = [0.3, 0, 0,0,0,0,0,0]
        wedges = {'linewidth':0}
        colors = ['#21E132', '#DB2DCE', '#D22424', '#2542D0', '#D9E72C', '#1BD8D3', '#D68919', '#6624E2']
        self.searched_speed_chart = PlotCanvas(self, width=10, height=10, dpi=100)
        self.searched_speed_chart.axes.pie(searched_speed_results, labels=self.search_labels, explode=explode, colors=colors, shadow=True, startangle=270, wedgeprops=wedges, autopct='%1.1f%%')
        self.searched_speed_chart.axes.set_title('Number of Accidents per Speed Zone')
        self.speed_tab_layout.addWidget(self.searched_speed_chart)
    
    def todPagePerformFilterSearch(self):
        filter_results = get_time_data(self.filter_start_date_input.date(), self.filter_end_date_input.date(), self.data)
        rounded_time = []
        incident_count = []
        for row in enumerate(filter_results):
            rounded_time.append(row[1][0])
            incident_count.append(row[1][1])
        if hasattr(self, 'filtered_tod_chart'):
            self.filter_tab_layout.removeWidget(self.filtered_tod_chart)
        self.filtered_tod_chart = PlotCanvas(self, width=10, height=10, dpi=100)
        self.filtered_tod_chart.axes.plot(rounded_time, incident_count, 'g--', label="Time of day trend")
        self.filtered_tod_chart.axes.set_xlabel("Time (24 hour)")
        self.filtered_tod_chart.axes.set_ylabel("Accidents (total)")
        self.filtered_tod_chart.axes.set_title('Average Accidents per hour')
        self.filter_tab_layout.removeWidget(self.todchart)
        self.filter_tab_layout.addWidget(self.filtered_tod_chart)

    def alcoholPageFilter(self):
        searched_alcohol_results = get_alcohol_incidents(self.alcohol_start_date_input.date(), self.alcohol_end_date_input.date(), self.data)

        labels = []
        alcohol_incidents = []

        for row in enumerate(searched_alcohol_results[0]):
            labels.append(row[1][0])
            alcohol_incidents.append(row[1][1])
        x = np.arange(len(labels))
        bar_width = 0.5
        explode = [0.1, 0]
        wedges = {'linewidth':0}
        colors = ['#21E132', '#DB2DCE']

        if hasattr(self, 'searched_alcohol'):
            self.alcohol_tab_layout.removeWidget(self.searched_alcohol)
        if hasattr(self, 'searched_alcohol_chart_2'):
            self.alcohol_tab_layout.removeWidget(self.searched_alcohol_chart_2)

        self.searched_alcohol = PlotCanvas(self, width=5, height=5, dpi=100)
        self.searched_alcohol.axes.pie(list(searched_alcohol_results[1][0]), labels=["Alcohol Involved", "No Alcohol"], explode=explode, colors=colors, shadow=True, startangle=270, wedgeprops=wedges, autopct='%1.1f%%')
        self.searched_alcohol.axes.set_title('Alcohol vs No Alcohol related accidents')

        self.searched_alcohol_chart_2 = PlotCanvas(self, width=8, height=6, dpi=100)
        self.searched_alcohol_chart_2.axes.bar(x, alcohol_incidents, bar_width, label="Alcohol Involved")
        self.searched_alcohol_chart_2.axes.set_xticks(x)
        xlabels = self.searched_alcohol_chart_2.axes.set_xticklabels(labels)
        self.searched_alcohol_chart_2.axes.set_ylabel("Accident amounts")
        for i, label in enumerate(xlabels):
            label.set_y(label.get_position()[1] - (i % 2) * 0.075)
        self.searched_alcohol_chart_2.axes.set_title('Alcohol involved collisions')
        self.alcohol_tab_layout.removeWidget(self.alcohol_chart)
        self.alcohol_tab_layout.removeWidget(self.alcohol_chart_2)
        self.alcohol_tab_layout.addWidget(self.searched_alcohol)
        self.alcohol_tab_layout.addWidget(self.searched_alcohol_chart_2)

###########################
# Running the application #
###########################
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pixmap = QPixmap('data/logo.png').scaled(250, 175)
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