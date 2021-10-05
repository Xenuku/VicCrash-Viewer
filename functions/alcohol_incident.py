from PyQt5.QtCore import QDate, QDateTime


def get_time_data(start_date, end_date, data):
    startdate = start_date.toString('yyyy-MM-dd')
    enddate = end_date.toString('yyyy-MM-dd')
    c = data.cursor()
    # If there is a search term, check certain columns
    # Otherwise, just grab data from selected columns between selected dates (defaults to all if nothing changed)
    c.execute(f"""
                SELECT accident_type, COUNT(*) AS incident_count
                FROM crashdata 
                WHERE date(accident_date) BETWEEN date('{startdate}') AND date('{enddate}')
                AND alcohol_related='Yes'
                GROUP BY accident_type
            """)
    result = c.fetchall()
    # debug to check inputs
    #print(f"Time of day data retrieved! START: {startdate} and END: {enddate}")
    #print(result)
    return result 
