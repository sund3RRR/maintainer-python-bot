import sqlite3
from typing import Tuple


def get_db_conn_and_cursor() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect("data/db/maintainer.db")
    return conn, conn.cursor()

def create_repos_table(erase = False):
    conn, cursor = get_db_conn_and_cursor()
    if erase:
        cursor.execute("""
            DROP TABLE IF EXISTS repos;
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repos(
            id INTEGER,
            user INTEGER,
            owner TEXT,
            repo TEXT,
            last_tag_name TEXT,
            is_release INTEGER
        );
    """)

    conn.commit()

def create_users_table(erase = False):
    conn, cursor = get_db_conn_and_cursor()
    if erase:
        cursor.execute("""
            DROP TABLE IF EXISTS users;
        """)
        
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            user_id INTEGER
        );
    """)

    conn.commit()

if __name__=='__main__':
    create_repos_table(erase=True)
    create_users_table(erase=True)