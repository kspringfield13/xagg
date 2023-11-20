import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = "articles.db"

    sql_create_articles_table = """CREATE TABLE IF NOT EXISTS articles (
                                    id integer PRIMARY KEY,
                                    headline text NOT NULL,
                                    published_date date,
                                    url text,
                                    screenshot BLOB
                                );"""

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        # Create articles table
        create_table(conn, sql_create_articles_table)
        
        # Close connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()