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
        self.assertEqual(len(result),  74908)

    # Test filter function when start date greater than end date
    def test_date_validity_home(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data(QtCore.QDate(2017, 1, 15), QtCore.QDate(2016, 1, 15), "Collision", data)
        self.assertEqual(len(result), 0)

    # Test filter function when dates are out of range
    def test_date_range_home(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data(QtCore.QDate(2020, 1, 15), QtCore.QDate(2021, 1, 15), "Collision", data)
        self.assertEqual(len(result), 0)

    # Test filter function when no keyword with no matches is used
    def test_no_keyword_matches_home(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data(QtCore.QDate(2013, 7, 1), QtCore.QDate(2019, 3, 21), "Testing123", data)
        self.assertEqual(len(result), 0)

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
        self.assertEqual(len(result), 0)


    # # SPEED PAGE FUNCTIONS

    # # Test load page
    # def test_load_page_speed(self):
    #     data = sqlite3.connect('./data/crash.db')

    # # Test setting start and end date
    # def test_set_dates_speed(self):
    #     data = sqlite3.connect('./data/crash.db')

    # # Test setting start date as greater than end date
    # def test_date_validity_speed(self):
    #     data = sqlite3.connect('./data/crash.db')


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
        self.assertEqual(len(result[1]), 0) #achohol count



if __name__ == '__main__':
    unittest.main(verbosity=2)