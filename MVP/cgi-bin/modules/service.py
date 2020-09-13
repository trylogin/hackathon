import sqlite3
import os


def get_template(template_name):
    with open(os.path.join("templates", template_name)) as f:
        template = f.read()
    return template

def create_conn():
    conn = sqlite3.connect('results.db')
    cur = conn.cursor()

    return conn, cur

def close_conn(conn):
    conn.commit()
    conn.close()