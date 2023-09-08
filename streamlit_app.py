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
from pydeck.types import String
import time
from datetime import datetime
import pytz
from dateutil import tz

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

googlesheets_url = "https://docs.google.com/spreadsheets/d/1Pq9mMo7U9LTOG8XO5YpfRJdrx8TroQ1ZULX9UGQ9ON4/edit#gid=0"

#@st.cache_data()

def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    data = pd.read_csv(csv_url,decimal=',')
    data['Date']= pd.to_datetime(data['Date'],format='%d/%m/%Y %H:%M:%S').dt.tz_localize(tz='Europe/Amsterdam')
    return data

def separate_df(df):
  
  df_eco01 = df[df['Board'] == 'ECO01']
  df_eco02 = df[df['Board'] == 'ECO02']
  df_eco03 = df[df['Board'] == 'ECO03']
  df_eco04 = df[df['Board'] == 'ECO04']

  return [df_eco01, df_eco02, df_eco03, df_eco04]

data = load_data(googlesheets_url)



def dataframe_tags(df):
  tags = pd.DataFrame(columns=data.columns)
  print(tags)
  df = df.dropna()
   
  for index, row in df.iterrows():
    tags_detected = str(row['Tags']).split(',')

    for tag in tags_detected:
      print(tag)
      if tag not in tags['Tags'].unique() and tag != '':
        tags.loc[len(tags)] = row
        tags.iloc[-1,tags.columns.get_loc('Tags')] = tag


  new_tags = tags[['Date','Board','Tags']].copy()
  
  return new_tags.sort_values('Tags')



    

st.markdown("# Estado de los contenedores - Ecovidrio 2023")

st.markdown("### " + time.strftime("%H:%M, %d-%m-%Y ", time.localtime()))





#if st.checkbox('Show graph'):
#    st.subheader('Raw data')
#    st.line_chart(data=data, x='Date', y='Battery')
#    st.line_chart(data=data, x='Date', y='Distance')
#    st.line_chart(data=data, x='Date', y='PowerBank')



###############################

st.markdown('#')
st.markdown('#')
st.markdown("## Estado actual de los contenedores")

df_eco = separate_df(data)

col1, col2, col3, col4 = st.columns(4)
col = [col1, col2, col3, col4]

for i in range(len(col)):

  dist_limite_lleno = 46

  with col[i]:
    st.subheader("ECO" + str(i+1))

    st.markdown("Ultimo mensaje")
    st.markdown(str(df_eco[i].iloc[-1]['Date']))
    
    st.metric(label="Batería", 
              value=str(df_eco[i].iloc[-1]['Battery']) + ' %', 
              delta="OK" if df_eco[i].iloc[-1]['Battery'] > 10 else "Recargar",
              delta_color="normal" if df_eco[i].iloc[-1]['Battery'] > 10 else "inverse", 
              help="Porcentaje de la batería LiPo")
    st.metric(label="Distancia", 
              value=str(df_eco[i].iloc[-1]['Distance']) + ' cm', 
              delta="OK" if df_eco[i].iloc[-1]['Distance'] > dist_limite_lleno else "Muy lleno",
              delta_color="normal" if df_eco[i].iloc[-1]['Distance'] > dist_limite_lleno else "inverse",
              help="Distancia desde el sensor al suelo")
    st.metric(label="PowerBank", 
              value=str(df_eco[i].iloc[-1]['PowerBank']) + ' V', 
              delta="OK" if df_eco[i].iloc[-1]['PowerBank'] > 5.06 else "Recargar",
              delta_color="normal" if df_eco[i].iloc[-1]['PowerBank'] > 5.03 else "inverse",
              help="Voltaje de la batería power bank, esta casi descargada con menos de 5.03 V")
    st.metric(label="Tags", 
              value=df_eco[i].iloc[-1]['NTags'], 
              help="Número de tags detectados")


################################

st.markdown('#')
st.markdown('#')
st.markdown("## Evolución temporal de los datos")

tab1, tab2, tab3, tab4 = st.tabs(["Batería", "Distancia", "PowerBank", "Tags"])

with tab1:
  chart = alt.Chart(data).mark_line().encode(
    x=alt.X('Date:T'),
    y=alt.Y('Battery'),
    color=alt.Color("Board:N")
  ).properties(title="Evolución del estado de las baterías")
  st.altair_chart(chart, use_container_width=True)

with tab2:
  chart = alt.Chart(data).mark_circle().encode(
    x=alt.X('Date:T'),
    y=alt.Y('Distance'),
    color=alt.Color("Board:N")
  ).properties(title="evolución de la detección de distancia")
  st.altair_chart(chart, theme="streamlit", use_container_width=True)

with tab3:
  chart = alt.Chart(data).mark_line().encode(
    x=alt.X('Date:T'),
    y=alt.Y('PowerBank'),
    color=alt.Color("Board:N")
  ).properties(title="Evoluciñon del estado de los Powerbanks")
  st.altair_chart(chart, use_container_width=True)

with tab4:
  chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('Date:T'),
    y=alt.Y('NTags'),
    color=alt.Color("Board:N")
  ).properties(title="Número de tags detectados")
  st.altair_chart(chart, use_container_width=True)

# chart = alt.Chart(data).mark_line().encode(
#   x=alt.X('Date:T'),
#   y=alt.Y('PowerBank'),
#   color=alt.Color("Board:N")
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

# df = pd.DataFrame(
#     np.array([[40.41285562276367, -3.845885828653413], #Paseo de los Almendros
#               [40.40879654807273, -3.841979173370437], #Paseo de los Tilos
#               [40.4063734444676, -3.8417234741936377], #Paseo de los Olmos
#               [40.40424821121487, -3.8414530351276253]]), #Paseo de los Sauces
#     columns=['lat', 'lon'])

# st.map(df)

st.markdown('#')
st.markdown('#')

if st.checkbox('Mostrar Tags encontrados'):
    st.subheader('Tags')
    st.write(dataframe_tags(data))

st.markdown('#')

if st.checkbox('Mostrar datos originales'):
    st.subheader('Datos originales')
    st.write(data)

chart_data = pd.DataFrame(
    np.array([['ECO01','Paseo de los Almendros',40.41285562276367, -3.845885828653413], #Paseo de los Almendros
              ['ECO02','Paseo de los Tilos',40.40879654807273, -3.841979173370437], #Paseo de los Tilos
              ['ECO03','Paseo de los Olmos',40.4063734444676, -3.8417234741936377], #Paseo de los Olmos
              ['ECO04','Paseo de los Sauces',40.40424821121487, -3.8414530351276253]]), #Paseo de los Sauces
    columns=['name','address','lat', 'lon']) 


chart_data['name'] = chart_data['name'].astype('str') 
chart_data['address'] = chart_data['address'].astype('str') 
chart_data['lon'] = chart_data['lon'].astype('float') 
chart_data['lat'] = chart_data['lat'].astype('float') 

print(chart_data.dtypes)

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=40.4085, 
        longitude=-3.8452,
        zoom=14.5,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            type='ScatterplotLayer',
            id='scatter',
            data=chart_data,
            get_position=['lon', 'lat'],
            getFillColor='[20, 130, 40, 160]',
            get_radius=30,
        ),
        pdk.Layer(
            type="TextLayer",
            id='text-name',
            data=chart_data,
            pickable=True,
            get_position=['lon', 'lat'],
            get_text='name',
            get_size=10,
            get_color='[0, 0, 0]',
            get_angle=0,
            # Note that string constants in pydeck are explicitly passed as strings
            # This distinguishes them from columns in a data set
            get_text_anchor=String("middle"),
            get_alignment_baseline=String("center"),
        ),
        pdk.Layer(
            type="TextLayer",
            id='text-address',
            data=chart_data,
            pickable=True,
            get_position=['lon', 'lat'],
            get_text='address',
            get_size=10,
            get_color='[0, 0, 0]',
            get_angle=0,
            # Note that string constants in pydeck are explicitly passed as strings
            # This distinguishes them from columns in a data set
            get_text_anchor=String("middle"),
            get_alignment_baseline=String("center"),
        ),
    ],

))

# import streamlit.components.v1 as components, html

# def p5js_sketch(sketch_file, js_params=None, height=200, width=200):
# 	sketch = '<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.5.0/p5.min.js"></script>'
	
# 	sketch += '<script>'
# 	if js_params:
# 		sketch += js_params + "\n"
# 	sketch += open(sketch_file, 'r', encoding='utf-8').read()
# 	sketch += '</script>'
# 	components.html(sketch, height=height, width=width)



# st.header("sketch 0")
# p5js_sketch(
#   sketch_file="sketch.js",
#   js_params="const WIDTH=150; " 
#         "const HEIGHT=150; "
#         "let BACKGROUND_COLOR='red'; "
#         "let CIRCLE_SIZE=30;",
# )
