import mysql.connector
from datetime import datetime, timedelta
import random

if __name__ == "__main__":
    # Connect to the MySQL container
    db = mysql.connector.connect(
        host="localhost", user="user", password="password", database="timeseriesdb"
    )

    cursor = db.cursor()

    # Create table if it does not exist
    cursor.execute(
        """
        CREATE TABLE `simple_table` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `username` varchar(45) DEFAULT NULL,
        `total` decimal(10,0) DEFAULT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1
    """
    )

    cursor.execute(
        """INSERT INTO `simple_table`
        (`username`,
        `total`)
        VALUES
        ('Cat',56),
        ('Dog',35),
        ('Lizard',41),
        ('Crocodile',22),
        ('Koala',26),
        ('Cassowary',29),
        ('Peacock',19),
        ('Emu',10),
        ('Kangaroo',13);
    """
    )

    db.commit()
    cursor.close()
    db.close()
