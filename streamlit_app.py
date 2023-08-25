# streamlit_app.py

# To Do
#
# - poner bien la hora, gtm +2
# - decidir que poner de delta en los card metrics
# - pensar y poner la estadistica de los tags
# - poner bien los puntos de los ontenedores y si es posible un label
# - ver si cambiar ID por board
# -  ver si se puede bloquear el zoon del map

import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import pydeck as pdk
import time

st.set_page_config(
    page_title="Ecovidrio",
    page_icon="recycle"
    #layout="wide",
    # initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': '',
    #     'Report a bug': "",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.

googlesheets_url = "https://docs.google.com/spreadsheets/d/1Pq9mMo7U9LTOG8XO5YpfRJdrx8TroQ1ZULX9UGQ9ON4/edit#gid=327610644"

@st.cache_data()

def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    data = pd.read_csv(csv_url,decimal=',')
    data['Date']= pd.to_datetime(data['Date'],format='%d/%m/%Y %H:%M:%S')
    return data


st.markdown("# Estado de los contenedores - Ecovidrio 2023")

st.markdown("### " + time.strftime("%H:%M, %d-%m-%Y ", time.localtime()))

data = load_data(googlesheets_url)

#if st.checkbox('Show graph'):
#    st.subheader('Raw data')
#    st.line_chart(data=data, x='Date', y='Battery')
#    st.line_chart(data=data, x='Date', y='Distance')
#    st.line_chart(data=data, x='Date', y='PowerBank')

st.markdown('#')
st.markdown('#')
st.markdown("## Estado actual de los contenedores")

col1, col2, col3, col4 = st.columns(4)

with col1:
   st.subheader("ECO01")
   st.metric(label="Batería", value="45.3 %", delta="1.2 %", help="help")
   ##my_bar = st.progress(0, text="bateria")
   st.metric(label="Distancia", value="138 cm", delta="1.2 %")
   st.metric(label="PowerBank", value="5.104 V", delta="1.2 %")
   st.metric(label="Tags", value="4", delta="1.2 %")

with col2:
   st.subheader("ECO02")
   st.metric(label="Batería", value="45.3 %", delta="1.2 %")
   ##my_bar = st.progress(0, text="bateria")
   st.metric(label="Distancia", value="138 cm", delta="1.2 %")
   st.metric(label="PowerBank", value="5.104 V", delta="1.2 %")
   st.metric(label="Tags", value="4", delta="1.2 %")

with col3:
   st.subheader("ECO03")
   st.metric(label="Batería", value="45.3 %", delta="1.2 %")
   ##my_bar = st.progress(0, text="bateria")
   st.metric(label="Distancia", value="138 cm", delta="1.2 %")
   st.metric(label="PowerBank", value="5.104 V", delta="1.2 %")
   st.metric(label="Tags", value="4", delta="1.2 %")

with col4:
   st.subheader("ECO04")
   st.metric(label="Batería", value="45.3 %", delta="1.2 %")
   ##my_bar = st.progress(0, text="bateria")
   st.metric(label="Distancia", value="138 cm", delta="1.2 %")
   st.metric(label="PowerBank", value="5.104 V", delta="1.2 %")
   st.metric(label="Tags", value="4", delta="1.2 %")
   
st.markdown('#')
st.markdown('#')
st.markdown("## Evolución temporal de los datos")

tab1, tab2, tab3, tab4 = st.tabs(["Batería", "Distancia", "PowerBank", "Tags"])

with tab1:
  chart = alt.Chart(data).mark_line().encode(
    x=alt.X('Date:T'),
    y=alt.Y('Battery'),
    color=alt.Color("ID:N")
  ).properties(title="Evolución del estado de las baterías")
  st.altair_chart(chart, use_container_width=True)

with tab2:
  chart = alt.Chart(data).mark_circle().encode(
    x=alt.X('Date:T'),
    y=alt.Y('Distance'),
    color=alt.Color("ID:N")
  ).properties(title="evolución de la detección de distancia")
  st.altair_chart(chart, theme="streamlit", use_container_width=True)

with tab3:
  chart = alt.Chart(data).mark_line().encode(
    x=alt.X('Date:T'),
    y=alt.Y('PowerBank'),
    color=alt.Color("ID:N")
  ).properties(title="Evoluciñon del estado de los Powerbanks")
  st.altair_chart(chart, use_container_width=True)

with tab4:
  chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('Date:T'),
    y=alt.Y('NTags'),
    color=alt.Color("ID:N")
  ).properties(title="Número de tags detectados")
  st.altair_chart(chart, use_container_width=True)

# chart = alt.Chart(data).mark_line().encode(
#   x=alt.X('Date:T'),
#   y=alt.Y('PowerBank'),
#   color=alt.Color("ID:N")
# ).properties(title="Distance")
# st.altair_chart(chart, use_container_width=True)



# progress_text = "Operation in progress. Please wait."
# my_bar = st.progress(0, text=progress_text)

# for percent_complete in range(100):
#     #time.sleep(0.1)
#     my_bar.progress(percent_complete + 1, text=progress_text)

st.markdown('#')
st.markdown('#')
st.markdown("## Localización de los contenedores")

df = pd.DataFrame(
    np.array([[40.423641579072424, -3.7097167830446405],
              [40.42017844890178, -3.7049102648037278],
              [40.428770604656876, -3.701562868171665],
              [40.4215833250859, -3.69117735554398]]),
    columns=['lat', 'lon'])

st.map(df)

st.markdown('#')
st.markdown('#')

if st.checkbox('Mostrar datos originales'):
    st.subheader('Datos originales')
    st.write(data)

# new_df = data[['Date','Battery']].copy()


# if st.checkbox('Show raw data2'):
#     st.subheader('Raw data')
#     st.write(new_df)

# chart_data = pd.DataFrame(
#     np.array([[40.423641579072424, -3.7097167830446405],
#             [40.42017844890178, -3.7049102648037278],
#             [40.428770604656876, -3.701562868171665],
#             [40.4215833250859, -3.69117735554398]]),
#     columns=['lat', 'lon']) 
#
# st.pydeck_chart(pdk.Deck(
#     map_style=None,
#     initial_view_state=pdk.ViewState(
#         latitude=40.42,
#         longitude=-3.7,
#         zoom=14,
#         pitch=50,
#     ),
#     layers=[
#         pdk.Layer(
#            'HexagonLayer',
#            data=chart_data,
#            get_position='[lon, lat]',
#            radius=200,
#            elevation_scale=4,
#            elevation_range=[0, 1000],
#            pickable=True,
#            extruded=True,
#         ),
#         pdk.Layer(
#             'ScatterplotLayer',
#             data=chart_data,
#             get_position='[lon, lat]',
#             get_color='[200, 30, 0, 160]',
#             get_radius=200,
#         ),
#     ],
# ))