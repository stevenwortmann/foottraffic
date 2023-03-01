import psycopg2
import pandas as pd
import os

def create_database(database_name, db_user, db_password):
    """
    Connects to PostgreSQL server and creates a database.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host="localhost"
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {database_name}")
        cur.close()
        conn.close()
        print("Database created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")

def create_tables(db_name, db_user, db_password, sql_file_path):
    """
    Connects to the specified PostgreSQL database and creates tables using an SQL file.
    """
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host="localhost"
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        with open(sql_file_path, 'r') as sql_file:
            cur.execute(sql_file.read())
        cur.close()
        conn.close()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

def create_stored_procedures(db_name, db_user, db_password, sql_file_path):
    """
    Connects to the specified PostgreSQL database and creates stored procedures using an SQL file.
    """
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host="localhost"
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        with open(sql_file_path, 'r') as sql_file:
            cur.execute(sql_file.read())
        cur.close()
        conn.close()
        print("Stored procedures created successfully.")
    except Exception as e:
        print(f"Error creating stored procedures: {e}")

def insert_data(db_name, db_user, db_password, directory_path):
    """
    Connects to the specified PostgreSQL database and inserts data into tables from CSV files in a directory.
    """
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host="localhost"
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        for file in os.listdir(directory_path):
            if file.endswith(".csv"):
                file_path = os.path.join(directory_path, file)
                df = pd.read_csv(file_path)
                table_name = file.split(".")[0]
                df.to_sql(table_name, conn, if_exists='append', index=False)
        cur.close()
        conn.close()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
