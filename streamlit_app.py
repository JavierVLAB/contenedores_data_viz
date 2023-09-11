# streamlit_app.py

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


# Configuración inicial del APP

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

# URL de los datos en google sheet
googlesheets_url = "https://docs.google.com/spreadsheets/d/1Pq9mMo7U9LTOG8XO5YpfRJdrx8TroQ1ZULX9UGQ9ON4/edit#gid=0"


#  Load los datos y convertirlos en un dataframe
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    data = pd.read_csv(csv_url,decimal=',')
    data['Date']= pd.to_datetime(data['Date'],format='%d/%m/%Y %H:%M:%S').dt.tz_localize(tz='Europe/Amsterdam')
    return data

# Separa los datos en dataframes con los tags encontrados por cada contenedor
def separate_df(df):
  
  df_eco01 = df[df['Board'] == 'ECO01']
  df_eco02 = df[df['Board'] == 'ECO02']
  df_eco03 = df[df['Board'] == 'ECO03']
  df_eco04 = df[df['Board'] == 'ECO04']

  return [df_eco01, df_eco02, df_eco03, df_eco04]

data = load_data(googlesheets_url)



# limpia los datos y devuelve solo la primera vez que se encontro un tag
def dataframe_tags(df):
  tags = pd.DataFrame(columns=data.columns)
  #print(tags)
  df = df.dropna()
   
  for index, row in df.iterrows():
    tags_detected = str(row['Tags']).split(',')

    for tag in tags_detected:
      #print(tag)
      if tag not in tags['Tags'].unique() and tag != '':
        tags.loc[len(tags)] = row
        tags.iloc[-1,tags.columns.get_loc('Tags')] = tag

  new_tags = tags[['Date','Board','Tags']].copy()
  
  return new_tags.sort_values('Tags')

    


########################

st.markdown("# Estado de los contenedores - Ecovidrio 2023")

st.markdown("### " + time.strftime("%H:%M, %d-%m-%Y ", time.localtime()))


#############################

# st.markdown('#')
# st.markdown('#')
# st.markdown("## Resumen")

# tags = dataframe_tags(data)

# print(tags['Board'].value_counts())
# df = tags['Board'].value_counts().rename_axis('Board').reset_index(name='counts').sort_values(by=['Board'])
# print(df)

# st.markdown('#')
# st.markdown('### Número total de Tags: ' + str(len(tags.axes[0])) )
# st.markdown('### Tags encontrados en cada contenedor: ')

# for idx, contenedor in enumerate(tags['Board'].value_counts().index.tolist()):
#   st.markdown('### - ' + contenedor + ': ' + str(tags['Board'].value_counts()[idx]))



# st.markdown('#')


############################### 
# Estado de los contenedores

st.markdown('#')
st.markdown('#')
st.markdown("## Estado actual de los contenedores")

df_eco = separate_df(data)

tags = dataframe_tags(data)

df = tags['Board'].value_counts().rename_axis('Board').reset_index(name='counts').sort_values(by=['Board'])

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
              value=df.iloc[i]['counts'], 
              help="Número de tags detectados")
    
st.markdown('#')
st.markdown('### Número total de Tags: ' + str(len(tags.axes[0])) )
    
if st.checkbox('Mostrar Tags encontrados'):
    st.subheader('Tags')
    st.write(tags)
    st.download_button(
        label="Descargar Tags (CSV)",
        data=tags.to_csv().encode('utf-8'),
        file_name='tags.csv',
        mime='text/csv',
    )

if st.checkbox('Mostrar datos originales'):
    st.subheader('Datos originales')
    st.write(data)
    st.download_button(
        label="Descargar datos (CSV)",
        data=tags.to_csv().encode('utf-8'),
        file_name='data.csv',
        mime='text/csv',
    )



################################
# Evolución temporal de los datos

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
  ).properties(title="Evolución del estado de los Powerbanks")
  st.altair_chart(chart, use_container_width=True)

with tab4:
  chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('Date:T'),
    y=alt.Y('NTags'),
    color=alt.Color("Board:N")
  ).properties(title="Número de tags detectados")
  st.altair_chart(chart, use_container_width=True)

##############################
# Localización de los contenedores 

st.markdown('#')
st.markdown('#')
st.markdown("## Localización de los contenedores")

st.markdown('#')

# Datos de localización
chart_data = pd.DataFrame(
    np.array([['ECO01','Paseo de los Almendros',40.41285562276367, -3.845885828653413], #Paseo de los Almendros
              ['ECO02','Paseo de los Tilos',40.4088124, -3.8420954], #Paseo de los Tilos
              ['ECO03','Paseo de los Olmos',40.4063784, -3.8417471], #Paseo de los Olmos
              ['ECO04','Paseo de los Sauces',40.4042731, -3.8414437]]), #Paseo de los Sauces
    columns=['name','address','lat', 'lon']) 


chart_data['name'] = chart_data['name'].astype('str') 
chart_data['address'] = chart_data['address'].astype('str') 
chart_data['lon'] = chart_data['lon'].astype('float') 
chart_data['lat'] = chart_data['lat'].astype('float') 

# localizaciñon de los textos
dir_chart_data = chart_data.copy()
name_chart_data = chart_data.copy()

dir_chart_data['lat'] = dir_chart_data['lat'] + 0.0005
name_chart_data['lon'] = name_chart_data['lon'] - 0.0013

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
            data=name_chart_data,
            pickable=True,
            get_position=['lon', 'lat'],
            get_text='name',
            get_size=18,
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
            data=dir_chart_data,
            pickable=True,
            get_position=['lon', 'lat'],
            get_text='address',
            get_size=15,
            get_color='[0, 0, 0]',
            get_angle=0,
            # Note that string constants in pydeck are explicitly passed as strings
            # This distinguishes them from columns in a data set
            get_text_anchor=String("middle"),
            get_alignment_baseline=String("center"),
        ),
    ],

))

st.markdown('#')


