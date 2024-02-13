import sqlite3
import pandas as pd
from unidecode import unidecode
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def extract_data(db_path, tables):
    conn = sqlite3.connect(db_path)
    dataframes = {}

    for table in tables:
        query = f'SELECT * FROM {table}'
        df = pd.read_sql_query(query, conn)
        dataframes[table] = df

    conn.close()
    return dataframes

def transform_data(dataframes):
    # Customer table transformation
    df_customers = dataframes['customers']
    df_customers['FirstName'] = df_customers['FirstName'].apply(unidecode)
    df_customers['LastName'] = df_customers['LastName'].apply(unidecode)
    df_customers['City'] = df_customers['City'].apply(unidecode)
    df_customers['Phone'] = df_customers['Phone'].str.replace(r'[()\s-]', '', regex=True)
    columns_to_drop = ['Company', 'State', 'Fax']
    df_customers = df_customers.drop(columns=columns_to_drop)
    dataframes['customers'] = df_customers

    # Track table transformation
    df_tracks = dataframes['tracks']
    columns_to_drop = ['Milliseconds', 'Bytes', 'Composer', 'MediaTypeId', 'GenreId']
    df_tracks = df_tracks.drop(columns=columns_to_drop)
    dataframes['tracks'] = df_tracks

    # Employees table transformation
    df_employees = dataframes['employees']
    df_employees['BirthDate'] = pd.to_datetime(df_employees['BirthDate']).dt.date
    df_employees['HireDate'] = pd.to_datetime(df_employees['HireDate']).dt.date
    for col in ['Phone', 'Fax']:
        df_employees[col] = df_employees[col].apply(lambda x: '+' + x if not x.startswith('+') else x)
    dataframes['employees'] = df_employees

    # Invoice table transformation
    df_invoices = dataframes['invoices']
    df_invoices['InvoiceDate'] = pd.to_datetime(df_invoices['InvoiceDate']).dt.date
    dataframes['invoices'] = df_invoices

    # Album table transformation
    df_albums = dataframes['albums']
    df_albums = df_albums.drop(columns=['ArtistId'])
    dataframes['albums'] = df_albums

    return dataframes

def load_data(dataframes, mysql_user, password, mysql_host, mysql_db, port):
    try:
        mysql_engine = create_engine(f'mysql+pymysql://{mysql_user}:{password}@{mysql_host}:{port}/{mysql_db}')

        for table, df in dataframes.items():
            df.to_sql(name=table, con=mysql_engine, index=False, if_exists='replace')

        mysql_engine.dispose()

    except SQLAlchemyError as e:
        print(f"Error during database connection or data loading: {e}")

def main():
    sqlite_db_path = 'chinook.db'
    desired_tables = ['tracks', 'invoice_items', 'invoices', 'customers', 'albums', 'employees']

    # Extract data
    extracted_data = extract_data(sqlite_db_path, desired_tables)

    # Transform data
    transformed_data = transform_data(extracted_data)

    # Load data into MySQL
    mysql_user = 'root'
    password = 'Mm%406676363'
    mysql_host = '127.0.0.1'
    mysql_db = 'etl'
    port = '3306'
    load_data(transformed_data, mysql_user, password, mysql_host, mysql_db, port)

if __name__ == "__main__":
    main()
