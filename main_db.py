# import necessary modules
import sqlite3
from sqlite3 import Error
# import scraper

class StoryDB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def create_connection(self):
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        # return connection object
        # return self.conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    # create Articles table
    def make_table_attributes(self):
        sql_create_articles_table = """ CREATE TABLE IF NOT EXISTS Articles (
                                            title text NOT NULL,
                                            link text NOT NULL,
                                            summary text,
                                        ); """
        # create tables
        if self.conn is not None:
            # create Aritcles db_table
            self.create_table(sql_create_articles_table)
        else:
            print("Error! cannot create the database connection.")

    # insert rows to each attribute
    def insert_articles(self, row_values):
        """
        Create a new row into the Articles table
        :param conn: Connection object
        :param project: row_values
        :return: project id
        """
        query = ''' INSERT INTO Articles(title,link,summary)
                  VALUES(?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(query, row_values)
        self.conn.commit()

    def save_keep(self, articles_and_links):
        # create a database connection
        self.create_connection()
        self.make_table_attributes()

        with self.conn:
            # insert values into Articles Table
            for feed in articles_and_links:
                rows_insert = (feed['title'], feed['link'], feed['summary']);
                self.insert_articles(rows_insert)

    def select_title_and_link(self):
        """
        Select 'title' and 'links' from the Articles table
        :param conn: Connection object
        :return: records | results
        """
        records = None
        try:
            # query database to get the 'title' and 'link' of recommended articles
            cur = self.conn.cursor()
            cur.execute("SELECT title, link FROM Articles")

            records = cur.fetchall()
            cur.close()

        except Error as e:
            print("Failed to read data from sqlite table", e)
        finally:
            # close connection
            if (self.conn):
                self.conn.close()
                print("The SQLite connection is closed")

        return records

    def delete_all_records(self):
        """
        Delete all rows in the Articles table
        :param conn: Connection to the SQLite database
        :return:
        """

        sql = 'DELETE FROM Articles'
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
