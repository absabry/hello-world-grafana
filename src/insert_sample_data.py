import mysql.connector
from datetime import datetime, timedelta
import random


if __name__ == "__main__":
  # Connect to the MySQL container
  db = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="timeseriesdb"
  )

  cursor = db.cursor()

  # Create table if it does not exist
  cursor.execute("CREATE TABLE IF NOT EXISTS measurements (timestamp DATETIME, value DOUBLE)")

  # Insert some data
  start_time = datetime.now()
  for i in range(100):
      timestamp = start_time + timedelta(minutes=i)
      value = random.random() * 100  # Example metric
      cursor.execute("INSERT INTO measurements (timestamp, value) VALUES (%s, %s)", (timestamp, value))

  db.commit()
  cursor.close()
  db.close()
