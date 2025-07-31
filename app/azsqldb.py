# sql_db.py

import sqlite3
from sqlite3 import Error
import random
from datetime import date, timedelta
from tqdm import tqdm
import pandas as pd
import pyodbc
import os
import json


def create_connection():
    SERVER = os.environ["SERVER"]
    DATABASE = os.environ["DATABASE"]
    USERNAME = os.environ["db_user"]
    PASSWORD = os.environ["PASSWORD"]

    connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"

    conn = pyodbc.connect(connectionString)

    # DATABASE_NAME = "mydatabase.db"
    return conn


def query_database(query):
    """Run SQL query and return results in a dataframe"""
    conn = create_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def get_schema_representation_commercial():
    """Get the database schema in a JSON-like format"""
    conn = create_connection()
    cursor = conn.cursor()
   
    query = """

            SELECT 
                '{'+string_agg(''''+c.name +''':'+''''+ t.Name  +'''',',')+'}'
            
        FROM    
            sys.columns c
        INNER JOIN 
            sys.types t ON c.user_type_id = t.user_type_id
        LEFT OUTER JOIN 
            sys.index_columns ic ON ic.object_id = c.object_id AND ic.column_id = c.column_id

        WHERE
            c.object_id = OBJECT_ID('crematrix.commercial_data')

    """
    # print(query)
    cursor.execute(query)
    tables = cursor.fetchall()
    schema = tables[0][0]

    return schema


def get_schema_representation_residential():
    """Get the database schema for residential data in a JSON-like format"""
    conn = create_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            '{'+string_agg(''''+c.name +''':'+''''+ t.Name  +'''',',')+'}'
        FROM    
            sys.columns c
        INNER JOIN 
            sys.types t ON c.user_type_id = t.user_type_id
        LEFT OUTER JOIN 
            sys.index_columns ic ON ic.object_id = c.object_id AND ic.column_id = c.column_id
        WHERE
            c.object_id = OBJECT_ID('crematrix.residential_data')
    """

    cursor.execute(query)
    tables = cursor.fetchall()
    schema = tables[0][0]
    return schema



# This will create the table and insert 100 rows when you run sql_db.py
if __name__ == "__main__":

    # Setting up the financial table
    # setup_financial_table()

    # Querying the database
    # print(query_database("SELECT * FROM finances"))

    # Getting the schema representation
    print(get_schema_representation_finances())
