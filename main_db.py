# import necessary modules
import sqlite3
from sqlite3 import Error
import news_bot

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    # return connection object
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# create Articles table
def make_table_attributes(database_conn):
    sql_create_articles_table = """ CREATE TABLE IF NOT EXISTS Articles (
                                        title text NOT NULL,
                                        link text NOT NULL,
                                        comments text,
                                        score text
                                    ); """
    conn = database_conn
    # create tables
    if conn is not None:
        # create Aritcles db_table
        create_table(conn, sql_create_articles_table)
    else:
        print("Error! cannot create the database connection.")

# insert rows to each attribute
def insert_articles(conn, row_values):
    """
    Create a new row into the Articles table
    :param conn: Connection object
    :param project: row_values
    :return: project id
    """
    query = ''' INSERT INTO Articles(title,link,comments,score)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(query, row_values)
    conn.commit()

def store_articles_links(articles_and_links):
    database = r"./News_Database.db"

    # create a database connection
    conn = create_connection(database)
    make_table_attributes(conn)
    with conn:
        # insert values into Articles Table
        for feed in articles_and_links:
            rows_insert = (feed['title'], feed['link'], feed['comments'], feed['score']);
            insert_articles(conn, rows_insert)

def select_title_and_link(conn):
    """
    Select 'title' and 'links' from the Articles table
    :param conn: Connection object
    :return: records | results
    """
    try:
        # query database to get the 'title' and 'link' of recommended articles
        cur = conn.cursor()
        cur.execute("SELECT title, link FROM Articles")

        records = cur.fetchall()
        cur.close()

    except Error as e:
        print("Failed to read data from sqlite table", e)
    finally:
        # close connection
        if (conn):
            conn.close()
            print("The SQLite connection is closed")

    return records

def delete_all_records(conn):
    """
    Delete all rows in the Articles table
    :param conn: Connection to the SQLite database
    :return:
    """

    sql = 'DELETE FROM Articles'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
