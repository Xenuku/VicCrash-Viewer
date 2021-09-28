from PyQt5.QtCore import QDate, QDateTime
### The start of one of the functions? Sep file for each one? or one file for all????



def find_data(start_date, end_date, search_term, data):
    startdate = start_date.toString('d/M/yyyy')
    enddate = end_date.toString('d/M/yyyy')
    c = data.cursor()
    data.set_trace_callback(print)
    c.execute(f"select * from crashdata WHERE region_name LIKE '%{search_term}%'")
    print(len(c.fetchall()))

    # debug to check inputs
    print(f"Search input from home page! START: {startdate} and END: {enddate} and the keyword is {search_term}")