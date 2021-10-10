import unittest
import sqlite3
import datetime
from functions.user_period import find_data
from functions.time_of_day import get_time_data
from functions.alcohol_incident import get_alcohol_incidents
from functions import user_period
from functions import time_of_day
from functions import alcohol_incident
from PyQt5 import QtCore
import main


class TestMain(unittest.TestCase):
    # HOME PAGE FUNCTIONS
    # Test filter function when no keyword is used
    def test_blank_keyword_home(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data(QtCore.QDate(2013, 7, 1), QtCore.QDate(2019, 3, 21), "", data)
        self.assertEqual(len(result),  74908) # Should have the entire dataset of results

    # Test filter function when start date greater than end date
    def test_date_validity_home(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data(QtCore.QDate(2017, 1, 15), QtCore.QDate(2016, 1, 15), "Collision", data)
        self.assertEqual(len(result), 0) # Should have no results due to end date begin less than start date

    # Test filter function when dates are out of range
    def test_date_range_home(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data(QtCore.QDate(2020, 1, 15), QtCore.QDate(2021, 1, 15), "Collision", data)
        self.assertEqual(len(result), 0) # Should return no results due to dates being beyond data range

    # Test filter function when no keyword with no matches is used
    def test_no_keyword_matches_home(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data(QtCore.QDate(2013, 7, 1), QtCore.QDate(2019, 3, 21), "Testing123", data)
        self.assertEqual(len(result), 0) # Should return no results due to invalid keyword

    # Test filter for when 'Animal' keyword is used between a set date
    def test_search_keyword_returns_correctly_home(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data(QtCore.QDate(2013, 7, 1), QtCore.QDate(2014, 3, 21), "Animal", data)
        self.assertEqual(len(result), 104) # Should have 104 results for 'animal'


    # TIME OF DAY PAGE FUNCTIONS

    # Test load page
    def test_load_page_tod(self):
        data = sqlite3.connect('./data/crash.db')
        result = time_of_day.get_time_data(QtCore.QDate(2013, 7, 1), QtCore.QDate(2019, 3, 21), data)
        self.assertEqual(len(result), 24) # Should have 24 results

    # Test setting start and end date
    def test_set_dates_tod(self):
        data = sqlite3.connect('./data/crash.db')
        result = time_of_day.get_time_data(QtCore.QDate(2013, 7, 1), QtCore.QDate(2015, 3, 21), data)
        self.assertEqual(len(result), 24) # Should have 24 results

    # Test setting start date as greater than end date
    def test_date_validity_tod(self):
        data = sqlite3.connect('./data/crash.db')
        result = time_of_day.get_time_data(QtCore.QDate(2017, 7, 1), QtCore.QDate(2015, 7, 1), data)
        self.assertEqual(len(result), 0) # Should have no results


    # # SPEED PAGE FUNCTIONS

    def speedTest(self, start_date, end_date, data):
        #replicating the speed GUI function
        speed_start_date = start_date.toPyDate()
        speed_end_date = end_date.toPyDate()
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
        cursor = data.cursor()
        speeddata = cursor.execute(speed_query)
        speed_results = speeddata.fetchall()
        speed_results = list(speed_results[0])
        return speed_results

    # Test load page
    def test_load_page_speed(self):
        data = sqlite3.connect('./data/crash.db')
        result = self.speedTest(QtCore.QDate(2013, 7, 1), QtCore.QDate(2019, 3, 21), data)
        self.assertEqual(len(result), 8)

    # Test setting start and end date
    def test_set_dates_speed(self):
        data = sqlite3.connect('./data/crash.db')
        result = self.speedTest(QtCore.QDate(2013, 7, 1), QtCore.QDate(2014, 3, 21), data)
        self.assertEqual(len(result), 8)

    # Test setting start date as greater than end date
    def test_date_validity_speed(self):
        data = sqlite3.connect('./data/crash.db')
        result = self.speedTest(QtCore.QDate(2018, 7, 1), QtCore.QDate(2014, 3, 21), data)
        self.assertEqual(result[0], 0) # Make sure no data exists
        self.assertEqual(result[1], 0) # Make sure no data exists
        self.assertEqual(result[2], 0) # Make sure no data exists
        self.assertEqual(result[3], 0) # Make sure no data exists
        self.assertEqual(result[4], 0) # Make sure no data exists
        self.assertEqual(result[5], 0) # Make sure no data exists
        self.assertEqual(result[6], 0) # Make sure no data exists
        self.assertEqual(result[7], 0) # Make sure no data exists


    # ALCOHOL PAGE FUNCTIONS

    # Test load page
    def test_load_page_alcohol(self):
        data = sqlite3.connect('./data/crash.db')
        result = alcohol_incident.get_alcohol_incidents(QtCore.QDate(2013, 7, 1), QtCore.QDate(2019, 3, 21), data)
        self.assertEqual(len(result[0]), 9) #incidents
        # Should have 9 results
        self.assertEqual(len(result[1]), 1) #achohol count
        # Should have 1 result

    # Test setting start and end date
    def test_set_dates_alcohol(self):
        data = sqlite3.connect('./data/crash.db')
        result = alcohol_incident.get_alcohol_incidents(QtCore.QDate(2015, 7, 1), QtCore.QDate(2017, 3, 21), data)
        self.assertEqual(len(result[0]), 8) #incidents
        # Should have 9 results
        self.assertEqual(len(result[1]), 1) #achohol count
        # Should have 1 result

    # Test setting start date as greater than end date
    def test_date_validity_alcohol(self):
        data = sqlite3.connect('./data/crash.db')
        result = alcohol_incident.get_alcohol_incidents(QtCore.QDate(2017, 1, 15), QtCore.QDate(2016, 1, 15), data)
        self.assertEqual(len(result[0]), 0) #incidents
        self.assertEqual(len(result[1]), 1) #achohol count



if __name__ == '__main__':
    unittest.main(verbosity=2)