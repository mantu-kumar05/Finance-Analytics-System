import os
import sqlite3


DATABASE_NAME = "database/finance.db"


def get_connection():

    os.makedirs(os.path.dirname(DATABASE_NAME), exist_ok=True)

    conn = sqlite3.connect(DATABASE_NAME)

    return conn