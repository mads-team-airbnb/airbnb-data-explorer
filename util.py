import locale
import streamlit as st
import pandas as pd
import uuid


@st.cache_data
def convert_df(df: pd.DataFrame) -> str:
    return df.to_csv(index=False).encode('utf-8')


locale.setlocale(locale.LC_ALL, '')


def currency_to_num(currency):
    return locale.atof(currency.strip('$'))


stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'is', 'am', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'this', 'that', 'these', 'those',
                  'of', 'at', 'by', 'for', 'with', 'without', 'about', 'above', 'below', 'under', 'over', 'into', 'out', 'on', 'off', 'up', 'down', 'through', 'to', 'from', 'in', 'out'])
