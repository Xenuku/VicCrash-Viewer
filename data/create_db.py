import sqlite3 as db
import subprocess

conn = db.connect('./crash.db') # This automatically creates a database if it does not exist
cursor = conn.cursor()
query = "DROP TABLE IF EXISTS crashdata;" # Drop the table each time
cursor.execute(query)

subprocess.call(["sqlite3", "crash.db",
".mode csv",
".import 'Crash Statistics Victoria.csv' crashdata"]) # Import all the data back in 

