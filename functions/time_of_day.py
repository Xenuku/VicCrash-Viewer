# This function takes in two dates from the GUI in main.py
# It then performs an SQL query and returns the data to the main to be processed and plotted
def get_time_data(start_date, end_date, data):
    startdate = start_date.toString('yyyy-MM-dd')
    enddate = end_date.toString('yyyy-MM-dd')
    c = data.cursor()
    c.execute(f"""
                SELECT CAST(substr(accident_time, 1, 2) as INTEGER) AS rounded_time, COUNT(*) AS incident_count
                FROM crashdata WHERE date(accident_date) BETWEEN date('{startdate}') AND date('{enddate}')
                GROUP BY rounded_time
            """)
    result = c.fetchall() # This data has the amount of accidents for each hour of the time of day (0-23) between the two dates
    return result