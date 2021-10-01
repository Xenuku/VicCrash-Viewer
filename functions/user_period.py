from PyQt5.QtCore import QDate, QDateTime


def find_data(start_date, end_date, search_term, data):
    startdate = start_date.toString('yyyy-MM-dd')
    enddate = end_date.toString('yyyy-MM-dd')
    c = data.cursor()
    data.set_trace_callback(print)
    if len(search_term) > 0:
        c.execute(f"select * from crashdata WHERE date(accident_date) BETWEEN date('{startdate}') AND date('{enddate}' AND WHERE a)")
    else:
        c.execute(f"select * from crashdata WHERE date(accident_date) BETWEEN date('{startdate}') AND date('{enddate}')")
    print(len(c.fetchall()))

    # debug to check inputs
    print(f"Search input from home page! START: {startdate} and END: {enddate} and the keyword is {search_term}")