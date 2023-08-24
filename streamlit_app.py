# streamlit_app.py

import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import pydeck as pdk

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.

googlesheets_url = "https://docs.google.com/spreadsheets/d/1Pq9mMo7U9LTOG8XO5YpfRJdrx8TroQ1ZULX9UGQ9ON4/edit#gid=327610644"

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


chart = alt.Chart(data).mark_line().encode(
  x=alt.X('Date:T'),
  y=alt.Y('Battery'),
  color=alt.Color("ID:N")
).properties(title="Battery")
st.altair_chart(chart, use_container_width=True)

chart = alt.Chart(data).mark_circle().encode(
  x=alt.X('Date:T'),
  y=alt.Y('Distance'),
  color=alt.Color("ID:N")
).properties(title="Distance")
st.altair_chart(chart, theme="streamlit", use_container_width=True)

chart = alt.Chart(data).mark_line().encode(
  x=alt.X('Date:T'),
  y=alt.Y('PowerBank'),
  color=alt.Color("ID:N")
).properties(title="Powerbank")
st.altair_chart(chart, use_container_width=True)

chart = alt.Chart(data).mark_line().encode(
  x=alt.X('Date:T'),
  y=alt.Y('PowerBank'),
  color=alt.Color("ID:N")
).properties(title="Distance")
st.altair_chart(chart, use_container_width=True)

chart = alt.Chart(data).mark_bar().encode(
  x=alt.X('Date:T'),
  y=alt.Y('NTags'),
  color=alt.Color("ID:N")
).properties(title="Distance")
st.altair_chart(chart, use_container_width=True)

df = pd.DataFrame(
    np.array([[40.423641579072424, -3.7097167830446405],
              [40.42017844890178, -3.7049102648037278],
              [40.428770604656876, -3.701562868171665],
              [40.4215833250859, -3.69117735554398]]),
    columns=['lat', 'lon'])

st.map(df)

chart_data = pd.DataFrame(
    np.array([[40.423641579072424, -3.7097167830446405],
            [40.42017844890178, -3.7049102648037278],
            [40.428770604656876, -3.701562868171665],
            [40.4215833250859, -3.69117735554398]]),
    columns=['lat', 'lon']) 

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=40.42,
        longitude=-3.7,
        zoom=14,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=chart_data,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))