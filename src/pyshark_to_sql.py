import pyshark
import mysql.connector
from datetime import datetime

# Function to connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="timeseriesdb"
    )

def insert_packet_data(src_ip, dest_ip, length, protocol):
    db = connect_to_db()
    cursor = db.cursor()
    query = "INSERT INTO packets (timestamp, src_ip, dest_ip, bytes_transferred, protocol) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (datetime.now(), src_ip, dest_ip, length, protocol))
    db.commit()
    cursor.close()
    db.close()

    print(f"Inserted {src_ip} packet data into the database")

def capture_packets(interface='your_network_interface'):
    capture = pyshark.LiveCapture(interface=interface)

    for packet in capture.sniff_continuously():
        try:
            src_ip = packet.ip.src
            dest_ip = packet.ip.dst
            length = packet.length
            protocol = packet.highest_layer
            insert_packet_data(src_ip, dest_ip, length, protocol)
        except AttributeError:
            continue

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
    capture_packets(interface='en0')
