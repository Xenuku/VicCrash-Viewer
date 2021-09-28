import sqlite3 as db
import subprocess
import time

conn = db.connect('./crash.db') # This automatically creates a database if it does not exist
cursor = conn.cursor()
conn.set_trace_callback(print)
query = "DROP TABLE IF EXISTS crashdata;" # Drop the table each time
cursor.execute(query)
conn.close()

subprocess.call(["sqlite3", "crash.db",
".mode csv",
".import 'Crash Statistics Victoria.csv' crashdata"]) # Import all the data back in 
time.sleep(2)

newconn = db.connect('./crash.db')
nc = newconn.cursor()
newconn.set_trace_callback(print)
# if date is like 15/5/2019
# if date is like 5/12/2019
# if date is like 5/5/2019
# if date is like 12/12/2019
# Sets all to proper format of yyyy-mm-dd
nc.executescript("""
    UPDATE crashdata SET accident_date = substr(accident_date, 6) || '-' || '0' || substr(accident_date, 4, 1) || '-' || substr(accident_date, 1, 2) WHERE accident_date LIKE '__/_/____';
    
    UPDATE crashdata SET accident_date = substr(accident_date, 6) || '-' || substr(accident_date, 3, 2) || '-' || '0' || substr(accident_date, 1, 1) WHERE accident_date LIKE '_/__/____';
    
    UPDATE crashdata SET accident_date = substr(accident_date, 5) || '-' || '0' || substr(accident_date, 3, 1) || '-' || '0' || substr(accident_date, 1, 1) WHERE accident_date LIKE '_/_/____';
    
    UPDATE crashdata SET accident_date = substr(accident_date, 7) || '-' || substr(accident_date, 4, 2) || '-' || substr(accident_date, 1, 2) WHERE accident_date LIKE '__/__/____';
""")
