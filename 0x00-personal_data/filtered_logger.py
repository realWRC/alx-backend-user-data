#!/usr/bin/env python3
"""
Obfuscation functions for user data
"""

import re
import logging
import os
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates user data in a logfile"""
    pattern = r'(' + '|'.join(fields) + r')=([^' + separator + r']*)'
    return re.sub(pattern, r'\1=' + redaction, message)


def get_logger() -> logging.Logger:
    """Creates configured logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connects to the MySQL database"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=db_name
    )


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialises formater"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def main():
    """Retrieves data and logs it"""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    if cursor.description:
        field_names = [i[0] for i in cursor.description]

    for row in cursor:
        message_items = []
        for name, value in zip(field_names, row):
            message_items.append(f"{name}={value}")
        message = "; ".join(message_items) + ";"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == '__main__':
    pass
