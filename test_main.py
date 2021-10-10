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


    # # TIME OF DAY PAGE FUNCTIONS

    # # Test load page
    # def test_load_page_tod(self):
    #     data = sqlite3.connect('./data/crash.db')
    #     result = time_of_day.get_time_data('2013-07-01', '2019-03-21', data)
    #     self.assertEqual(result, )

    # # Test setting start and end date
    # def test_set_dates_tod(self):
    #     data = sqlite3.connect('./data/crash.db')
    #     result = time_of_day.get_time_data('2015-07-01', '2017-03-21', data)
    #     self.assertEqual(result, )

    # # Test setting start date as greater than end date
    # def test_date_validity_tod(self):
    #     data = sqlite3.connect('./data/crash.db')
    #     result = time_of_day.get_time_data('2017-01-15', '2016-01-15', data)
    #     self.assertEqual(result, )


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


    # # ALCOHOL PAGE FUNCTIONS

    # # Test load page
    # def test_load_page_alcohol(self):
    #     data = sqlite3.connect('./data/crash.db')
    #     result = alcohol_incident.get_alcohol_incidents('2013-07-01', '2019-03-21', data)
    #     self.assertEqual(result, )

    # # Test setting start and end date
    # def test_set_dates_alcohol(self):
    #     data = sqlite3.connect('./data/crash.db')
    #     result = alcohol_incident.get_alcohol_incidents('2015-07-01', '2017-03-21', data)
    #     self.assertEqual(result, )

    # # Test setting start date as greater than end date
    # def test_date_validity_alcohol(self):
    #     data = sqlite3.connect('./data/crash.db')
    #     result = alcohol_incident.get_alcohol_incidents('2017-01-15', '2016-01-15', data)
    #     self.assertEqual(result, )



if __name__ == '__main__':
    unittest.main(verbosity=2)