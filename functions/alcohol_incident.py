def get_alcohol_incidents(start_date, end_date, data):
    startdate = start_date.toString('yyyy-MM-dd')
    enddate = end_date.toString('yyyy-MM-dd')
    c = data.cursor()
    c.execute(f"""
                SELECT accident_type, COUNT(*) AS incident_count
                FROM crashdata 
                WHERE date(accident_date) BETWEEN date('{startdate}') AND date('{enddate}')
                AND alcohol_related='Yes'
                GROUP BY accident_type
            """)
    result = c.fetchall()
    return result 
