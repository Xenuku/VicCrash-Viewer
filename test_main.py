import unittest
import sqlite3
from functions.user_period import find_data
from functions.time_of_day import get_time_data
from functions.alcohol_incident import get_alcohol_incidents
from functions import user_period
from functions import time_of_day
from functions import alcohol_incident 
import main


class TestMain(unittest.TestCase):

    # Testing with end date before start date
    def test_user_period(self):
        data = sqlite3.connect('./data/crash.db')
        result = user_period.find_data('2017-01-15', '2016-01-15', "", data)
        print(result)
        
   
    # Test that time of day function can extract data between dates
    def test_time_of_day(self):
        data = sqlite3.connect('./data/crash.db')
        result = time_of_day.get_time_data('2016-01-15', '2017-01-15', data)
        self.assertEqual(result, )


    # Test that time of day function can extract data between dates
    def test_alcohol_incident(self):
        data = sqlite3.connect('./data/crash.db')
        result = alcohol_incident.get_alcohol_incidents('2016-01-15', '2017-01-15', data)
        self.assertEqual(result, )



if __name__ == '__main__':
    unittest.main()