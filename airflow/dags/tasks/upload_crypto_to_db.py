import pandas as pd
from sqlalchemy import create_engine 

def send_data():
    todays_crypto = pd.read_csv('temp_csvs/todays_coin.csv')
    engine = create_engine('postgresql://airflow:airflow@localhost:5432/my_dump')
    todays_crypto.to_sql('trial_crypto', engine, schema = 'crypto', if_exists = 'append', method = 'multi')
    return None