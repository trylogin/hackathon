import sqlite3
import os
import codecs


def get_template(template_name):
    # with open(os.path.join("templates", template_name)) as f:
    with open(os.path.join("templates", template_name), encoding="utf8") as f:
    # with codecs.open(template_name, "r",encoding='utf-8', errors='ignore') as f:
        template = f.read()
    return template

def create_conn():
    conn = sqlite3.connect('results.db')
    cur = conn.cursor()

    return conn, cur

def close_conn(conn):
    conn.commit()
    conn.close()