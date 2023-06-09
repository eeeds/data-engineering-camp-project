#!/usr/bin/env python

import pandas as pd
from sqlalchemy import create_engine
from time import time 
import argparse
import os 

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    #donwload csv file
    file_name = './jena_climate_2009_2016.csv'
    #os.system(f"wget {url} -O {file_name}")
    df = pd.read_csv(file_name)
    #Create engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    ## Change data type
    df.rename(columns={'Date Time':'Date_Time'}, inplace=True)
    df.Date_Time = pd.to_datetime(df.Date_Time, format = '%d.%m.%Y %H:%M:%S')

    df.to_sql(name = 'jena_climate', con = engine, if_exists='replace')

parser = argparse.ArgumentParser(description= "Ingest CSV data to Postgres")

#user, password, host, port, database name, table name
#url of the csv

parser.add_argument('--user', help='user name for postgres')
parser.add_argument('--password', help='password name for postgres')
parser.add_argument('--host', help='host name for postgres')
parser.add_argument('--port', help='port name for postgres')
parser.add_argument('--db', help='database name for postgres')
parser.add_argument('--table_name', help='table name for postgres')
parser.add_argument('--url', help='url of the csv')


args = parser.parse_args()


if __name__ == "__main__":
    main(args)

