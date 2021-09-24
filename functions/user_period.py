from PyQt5.QtCore import QDate, QDateTime
### The start of one of the functions? Sep file for each one? or one file for all????
def find_data(start_date, end_date, search_term):
    print(f"Search input from home page! START: {start_date.toPyDate()} and END: {end_date.toPyDate()} and the keyword is {search_term}")