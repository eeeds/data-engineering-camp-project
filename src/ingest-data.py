#!/usr/bin/env python

import pandas as pd
from sqlalchemy import create_engine
from time import time 
import argparse
import os 
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_sqlalchemy import SqlAlchemyConnector


@task(log_prints = True, tags = ['extract'])
def extract_data(url:str='./jena_climate_2009_2016.csv'):

    csv_name = './jena_climate_2009_2016.csv'
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=10000)
    
    df = next(df_iter)

    df.rename(columns={'Date Time':'Date_Time'}, inplace=True)
    df.Date_Time = pd.to_datetime(df.Date_Time, format = '%d.%m.%Y %H:%M:%S')
    
 

    return df
@task(log_prints = True, retries = 3)
def load_data(table_name, df):
    connection_block = SqlAlchemyConnector.load("data-engineering-camp-postgres-connector")
    with connection_block.get_connection(begin = False) as engine:
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')


@task(log_prints = True, retries=3)
def ingest_data(user, password, host, port, db, table_name, df):
    postgres_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    engine = create_engine(postgres_url)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

@flow(name="Subflow", log_prints=True)
def log_subflow(table_name: str):
    print(f"Logging Subflow for: {table_name}")


@flow(name="Ingest Data")
def main_flow(table_name: str = "jena_climate"):
    user = "root"
    password = "root"
    host = "localhost"
    port = "5432"
    db = "climate_data"
    table_name = "jena_climate"


    #csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    log_subflow(table_name)
    data = extract_data()
    #data = transform_data(raw_data)
    load_data(table_name, data)
    #ingest_data(user, password, host, port, db, table_name, data)


if __name__ == '__main__':
    main_flow(table_name = "jena_climate")