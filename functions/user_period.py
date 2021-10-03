from PyQt5.QtCore import QDate, QDateTime


def find_data(start_date, end_date, search_term, data):
    startdate = start_date.toString('yyyy-MM-dd')
    enddate = end_date.toString('yyyy-MM-dd')
    c = data.cursor()
    # If there is a search term, check certain columns
    # Otherwise, just grab data from selected columns between selected dates (defaults to all if nothing changed)
    if len(search_term) > 0:
        c.execute(f"""
                    SELECT accident_no, accident_status, accident_date, accident_time, accident_type, 
                    day_of_week, alcohol_related, hit_run_flag, light_condition, police_attend, 
                    road_geometry, severity, speed_zone, run_offroad, region_name, total_persons, 
                    fatality, seriousinjury, otherinjury, noninjured, males, females, old_driver, 
                    young_driver, unlicencsed, no_of_vehicles 
                    FROM crashdata 
                    WHERE (DATE(accident_date) BETWEEN DATE('{startdate}') AND DATE('{enddate}')) AND
                    accident_type LIKE '%{search_term}%' OR 
                    road_geometry LIKE '%{search_term}%' OR
                    day_of_week LIKE '%{search_term}%' OR
                    region_name LIKE '%{search_term}%';
                 """)
    else:
        c.execute(f"""
                    SELECT accident_no, accident_status, accident_date, accident_time, accident_type, 
                    day_of_week, alcohol_related, hit_run_flag, light_condition, police_attend, 
                    road_geometry, severity, speed_zone, run_offroad, region_name, total_persons, 
                    fatality, seriousinjury, otherinjury, noninjured, males, females, old_driver, 
                    young_driver, unlicencsed, no_of_vehicles 
                    FROM crashdata WHERE date(accident_date) BETWEEN date('{startdate}') AND date('{enddate}')
                """)
    result = c.fetchall()
    # debug to check inputs
    print(f"Search input from home page! START: {startdate} and END: {enddate} and the keyword is {search_term}")
    return result