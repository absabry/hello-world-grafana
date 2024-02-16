import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Connect to the MySQL container
db = mysql.connector.connect(
  host="localhost",
  user="user",
  password="password",
  database="timeseriesdb"
)
cursor = db.cursor()

# Function to generate synthetic network flow data
def generate_data():
    timestamp = datetime.now() - timedelta(days=30)
    for _ in range(1000):  # Generate 1000 records
        timestamp += timedelta(minutes=5)
        src_ip = fake.ipv4()
        dest_ip = fake.ipv4()
        bytes_transferred = random.randint(1000, 1000000)
        src_port = random.randint(1024, 65535)
        dest_port = random.randint(1024, 65535)
        latency = random.uniform(0.1, 2.0)
        # Introduce anomalies: mark every 100th record as an anomaly
        is_anomaly = True if _ % 100 == 0 else False
        yield (timestamp, src_ip, dest_ip, bytes_transferred, src_port, dest_port, latency, is_anomaly)



# Create table if it does not exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS network_flows (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        src_ip VARCHAR(15),
        dest_ip VARCHAR(15),
        src_port INT,
        dest_port INT,
        latency DOUBLE,
        bytes_transferred BIGINT,
        is_anomaly BOOLEAN
    );
""")

# Insert data into the database
data = generate_data()
cursor.executemany("INSERT INTO network_flows (timestamp, src_ip, dest_ip,src_port,dest_port,latency,bytes_transferred,is_anomaly) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", list(data))

db.commit()
cursor.close()
db.close()
