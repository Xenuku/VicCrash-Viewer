import unittest
import sqlite3
from functions.user_period import find_data
from functions.time_of_day import get_time_data
from functions.alcohol_incident import get_alcohol_incidents
from functions import alcohol_incident 
from functions import user_period
from functions import time_of_day
import main


class TestMain(unittest.TestCase):

    def test_alcohol_incident(self):
        result = alcohol_incident.get_alcohol_incident('2016-01-15', '2017-01-15', )
        self.assertEqual(result, )

if __name__ == '__main__':
    unittest.main()