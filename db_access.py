import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def connect_to_database(connection_params: dict):
    """
    Connects to the PostgreSQL database.
    paramters:
        connection_params is a dictionary that define the following:
        {
            'dbname': 'your_database_name',
            'user': 'your_username',
            'password': 'your_password',
            'host': 'your_host',
            'port': 'your_port'
            }
    """
    try:
        connection = psycopg2.connect(**connection_params)
        return connection
    except psycopg2.Error as e:
        print(f"Error: Unable to connect to the database. {e}")
        return None

def read_table_to_dataframe(table_name, connection_params):
    """
    Reads a PostgreSQL table into a pandas dataframe.
    """
    connection = connect_to_database(connection_params)
    if connection:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, connection)
        connection.close()
        return df
    else:
        print("Error, no connection detected!")
        return None

def write_dataframe_to_table(df, table_name, connection_params):
    """
    Writes a pandas dataframe to a new table in the PostgreSQL database.
    """
    engine = create_engine(f"postgresql://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['dbname']}")
    df.to_sql(table_name, engine, index=False, if_exists='replace')
    print(f"Dataframe successfully written to the '{table_name}' table.")

def update_table_by_appending(df, table_name, connection_params):
    """
    Appends a pandas dataframe to an existing PostgreSQL table.
    """
    engine = create_engine(f"postgresql://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}:{connection_params['port']}/{connection_params['dbname']}")
    df.to_sql(table_name, engine, index=False, if_exists='append')
    print(f"Dataframe successfully appended to the '{table_name}' table.")

def delete_table(table_name, connection_params):
    """
    Deletes a table from the PostgreSQL database.
    """
    connection = connect_to_database(connection_params)
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        connection.commit()
        connection.close()
        print(f"Table '{table_name}' successfully deleted.")
    else:
        print("Error: Unable to connect to the database.")

