import pyshark
import mysql.connector
from datetime import datetime
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from sqlalchemy import create_engine


# Function to connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost", user="user", password="password", database="timeseriesdb"
    )


def get_engine():
    engine = create_engine(
        "mysql+mysqlconnector://user:password@localhost:3306/timeseriesdb", echo=False
    )
    return engine


def create_table(drop: bool = False):
    db = connect_to_db()
    cursor = db.cursor()
    if drop:
        cursor.execute("DROP TABLE IF EXISTS packets")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS packets (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            timestamp DATETIME, 
            src_ip VARCHAR(15), 
            dest_ip VARCHAR(15), 
            bytes_transferred INT, 
            protocol VARCHAR(15),
            ttl INT,
            checksum_status INT
        )
    """
    )
    cursor.close()
    db.close()

    print("table created successfully!")


def explore_packet(packet):
    """Explore the packet using pyshark. Can't work on ipynb..."""
    packet = ...  # get a packet from somewhere

    # pretty print a packet
    print(packet.pretty_print())

    # get all the layers in a packet
    print(packet.layers)

    for layer in packet.layers:
        print(f"{layer.layer_name}: \t {layer.field_names}")


def read_pcap_file(input_pcap: str) -> pd.DataFrame:
    """Reads a pcap file and returns a pandas dataframe with the packet information

    Args:
        input_pcap: Path to the pcap file

    Returns:
        pd.DataFrame: DataFrame with the packet information
    """
    cap = pyshark.FileCapture(input_pcap, keep_packets=False)
    data = []
    for packet in tqdm(cap):
        if (
            hasattr(packet, "ip")
            and hasattr(packet.ip, "src")
            and hasattr(packet.ip, "dst")
        ):
            data.append(
                {
                    "timestamp": datetime.fromtimestamp(float(packet.sniff_timestamp)),
                    "src_ip": packet.ip.src,
                    "dest_ip": packet.ip.dst,
                    "bytes_transferred": int(packet.length),
                    "protocol": packet.transport_layer,
                    "ttl": packet.ip.ttl,
                    "checksum_status": packet.ip.checksum_status,
                }
            )

    df = pd.DataFrame(data)
    print(f"Extracted {len(df)} from {input_pcap}")
    return df


if __name__ == "__main__":
    # sudo tcpdump -i any -w captures/captures_file.pcap -C 5
    create_table()

    root_folder = Path(".") / "captures"
    for pcap_file in root_folder.glob("*.pcap*"):
        df = read_pcap_file(pcap_file)
        _rows_inserted = df.to_sql(
            "packets",
            con=get_engine(),
            if_exists="append",
            index=False,
        )
        print(f"Inserted {_rows_inserted} from {pcap_file}!")
