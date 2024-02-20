import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
from tqdm import tqdm

# Initialize Faker
fake = Faker()


def generate_packet(timestamp):
    return {
        "timestamp": timestamp,
        "src_ip": fake.ipv4(),
        "dest_ip": fake.ipv4_public(),
        "protocol": random.choice(["TCP", "UDP"]),
        "length": random.choice(range(40, 1500)),
        "flags": random.choice(["", "SYN", "ACK"]),
        "info": "",
    }


def simulate_traffic(days=30, packets_per_day=10000):
    start_time = datetime.now() - timedelta(days=days)
    packets = []

    for day in range(days):
        daily_traffic = []
        for _ in range(packets_per_day):
            packet_time = start_time + timedelta(minutes=random.randint(0, 1440))
            packet = generate_packet(packet_time)
            daily_traffic.append(packet)

        # Insert malicious activity for simulation
        if day % 5 == 0:  # Simulate an attack every 5 days
            malicious_packet = generate_packet(
                start_time + timedelta(minutes=random.randint(0, 1440))
            )
            malicious_packet["info"] = "Malicious activity detected"
            daily_traffic.append(malicious_packet)

        packets.extend(daily_traffic)
        start_time += timedelta(days=1)

    return packets


if __name__ == "__main__":
    packets = simulate_traffic(days=30, packets_per_day=10000)
    print(f"Generated {len(packets)} packets")

    # Connect to the MySQL container
    db = mysql.connector.connect(
        host="localhost", user="user", password="password", database="timeseriesdb"
    )
    cursor = db.cursor()

    # Create table if it does not exist
    cursor.execute("DROP TABLE IF EXISTS network_flows;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS network_flows (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            src_ip VARCHAR(15),
            dest_ip VARCHAR(15),
            protocol VARCHAR(5),
            length INT,
            flags VARCHAR(10),
            info VARCHAR(512)
        );
    """
    )

    insert_query = """
        INSERT INTO network_flows (timestamp, src_ip, dest_ip, protocol, length, flags, info)
        VALUES (%(timestamp)s, %(src_ip)s, %(dest_ip)s, %(protocol)s, %(length)s, %(flags)s, %(info)s)
    """

    # Insert data into the database
    batches = [packets[i : i + 1000] for i in range(0, len(packets), 1000)]
    for batch in tqdm(batches):
        try:
            cursor.executemany(insert_query, batch)
        except Exception as e:
            print(f"An error occurred: {e}")

    db.commit()
    cursor.close()
    db.close()

    print(f"{len(packets)}  data inserted successfully!")
