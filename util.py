import locale
import joblib
import streamlit as st
import pandas as pd
import boto3
from io import BytesIO


s3 = boto3.client('s3')

bucket_name = 'mads-team-airbnb-s3'


def read_csv(path: str):
    obj = s3.get_object(Bucket=bucket_name, Key=path)
    return pd.read_csv(obj.get('Body'), compression='gzip', low_memory=False)


def read_model(path: str):
    with BytesIO() as data:
        s3.download_fileobj(bucket_name, path, data)
        data.seek(0)
        return joblib.load(data)


@ st.cache_data
def convert_df(df: pd.DataFrame) -> str:
    return df.to_csv(index=False).encode('utf-8')


locale.setlocale(locale.LC_ALL, '')


def currency_to_num(currency):
    currency = currency.replace(',', '')
    return locale.atof(currency.strip('$'))


stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'is', 'am', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'this', 'that', 'these', 'those',
                  'of', 'at', 'by', 'for', 'with', 'without', 'about', 'above', 'below', 'under', 'over', 'into', 'out', 'on', 'off', 'up', 'down', 'through', 'to', 'from', 'in', 'out'])
