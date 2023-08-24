# streamlit_app.py

import pandas as pd
import streamlit as st

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.

googlesheets_url = "https://docs.google.com/spreadsheets/d/1Pq9mMo7U9LTOG8XO5YpfRJdrx8TroQ1ZULX9UGQ9ON4/edit#gid=0"

@st.cache_data()

def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    data = pd.read_csv(csv_url,decimal=',')
    data['Date']= pd.to_datetime(data['Date'],format='%d/%m/%Y %H:%M:%S')
    return data



data = load_data(googlesheets_url)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


new_df = data[['Date','Battery']].copy()

print(new_df.dtypes)

if st.checkbox('Show raw data2'):
    st.subheader('Raw data')
    st.write(new_df)

if st.checkbox('Show graph'):
    st.subheader('Raw data')
    st.line_chart(data=data, x='Date', y='Battery')
    st.line_chart(data=data, x='Date', y='Distance')
    st.line_chart(data=data, x='Date', y='PowerBank')
