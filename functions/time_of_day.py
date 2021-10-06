def get_time_data(start_date, end_date, data):
    startdate = start_date.toString('yyyy-MM-dd')
    enddate = end_date.toString('yyyy-MM-dd')
    c = data.cursor()
    c.execute(f"""
                SELECT CAST(substr(accident_time, 1, 2) as INTEGER) AS rounded_time, COUNT(*) AS incident_count
                FROM crashdata WHERE date(accident_date) BETWEEN date('{startdate}') AND date('{enddate}')
                GROUP BY rounded_time
            """)
    result = c.fetchall()
    return result