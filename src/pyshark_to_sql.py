import pyshark
import mysql.connector
from datetime import datetime
import pandas as pd
from pathlib import Path

# Function to connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="timeseriesdb"
    )

def pcap_to_parquet(input_pcap):
    cap = pyshark.FileCapture(input_pcap, keep_packets=False)
    data = []
    for packet in cap:
        if hasattr(packet, "ip") and hasattr(packet.ip, "src") and hasattr(packet.ip, "dst"):
            print(packet)

    # df = pd.DataFrame(data)
    # print(df)

def create_table():
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packets (id INT AUTO_INCREMENT PRIMARY KEY, timestamp DATETIME, src_ip VARCHAR(15), dest_ip VARCHAR(15), bytes_transferred INT, protocol VARCHAR(15))
    """)
    cursor.close()
    db.close()


if __name__ == '__main__':
    create_table()
    print("table created successfully!")

    root_folder = Path(".") / "captures"
    for pcap_file in root_folder.glob("*.pcap"):
        pcap_to_parquet(pcap_file)

    # get data in a test.pcap file
    # continoulsy read new files that is coming here
    # push them to the dataset

