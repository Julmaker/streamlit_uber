import streamlit as st
import pandas as pd
import numpy as np

st.title('Abordaje de Clientes UBER en NY') #titulo de la Aplicación

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')  #Carga de data por URL

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Cree un elemento de texto e informe al lector que los datos se están cargando.
data_load_state = st.text('Loading data...')
# Cargue 10,000 filas de datos en el marco de datos.
data = load_data(10000)
# Notifique al lector que los datos se cargaron correctamente.
data_load_state.text("¡Listo! Los datos se cargaron correctamente...")

if st.checkbox('Muestra de Datos'):
    st.subheader('Datos')
    st.write(data)


st.subheader('Número de ABORDAJES por hora')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

hour_to_filter = st.slider('Filtro x hora', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map de todos los abordajes a las {hour_to_filter}:00')
st.map(filtered_data)


# pip freeze > requirements.txt -Para generar archivo de librerias del proyecto
