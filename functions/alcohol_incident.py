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
    incidents = c.fetchall()

    c.execute(f"""SELECT  
            ( SELECT COUNT(*) FROM crashdata WHERE alcohol_related = "Yes" AND (DATE(accident_date) 
                                BETWEEN DATE('{startdate}') AND DATE('{enddate}')) ),
            ( SELECT COUNT(*) FROM crashdata WHERE alcohol_related = "No" AND (DATE(accident_date) 
                                BETWEEN DATE('{startdate}') AND DATE('{enddate}')) );
    """)
    alcohol_count = c.fetchall()
    return [incidents, alcohol_count]
