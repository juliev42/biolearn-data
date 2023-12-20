import streamlit as st
import pandas as pd
import seaborn as sns
import biolearn

st.title('Biolearn Epigenetic Clock Models')

st.write("Welcome to this demo of data sources and clock models from biolearn.")

data = pd.read_csv("biolearn_docs/biolearn_modules.csv")
clocks = pd.read_csv("biolearn_docs/biolearn_clocks.csv")

st.show(data)


#st.cache
def load_data(nrows=None):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
