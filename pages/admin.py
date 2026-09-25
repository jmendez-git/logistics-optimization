import streamlit as st
import pandas as pd
import os
from services import geocoders

user = st.session_state.user_info
st.title("🧑 Panel de Administración")
st.success(f"Bienvenido Administrador/a: {user.get('name')} ({user.get('email')})")
st.divider()


file = st.file_uploader(
    'Seleccione el archivo a cargar',
    help='El archivo tiene que ser en extension .xlsx',
    type='xlsx',
    key='file',
    accept_multiple_files=False
)

st.divider()
st.write('##### Previsualización')

if st.session_state.file is not None:
    df = pd.read_excel(st.session_state.file)
    df_editado = st.data_editor(df, num_rows="dynamic")
    save_data = st.button('Seleccionar Archivo y Procesar Archivo', type='primary')

    for index, fila in df_editado.iterrows():
        # st.write(fila['direccion'])
        geocoders.get_geographic_coordinates(fila['direccion'])

    if save_data:
        server_folder = './databases'
        name_file = st.session_state.file.name

        complete_path = os.path.join(server_folder, name_file)

        df_editado['latitud'] = None
        df_editado['longitud'] = None

        progreso = st.progress(0)
        total_filas = len(df_editado)

        for index, fila in df_editado.iterrows():
            coordenadas = geocoders.get_geographic_coordinates(fila['direccion'])

            if coordenadas and len(coordenadas) == 2:
                df_editado.at[index, 'latitud'] = coordenadas[0]
                df_editado.at[index, 'longitud'] = coordenadas[1]
            else:
                df_editado.at[index, 'latitud'] = None
                df_editado.at[index, 'longitud'] = None
            
            progreso.progress((index + 1) / total_filas)


        try:
            if not os.path.exists(server_folder):
                os.makedirs(server_folder)

            with pd.ExcelWriter(complete_path, engine='openpyxl') as writer:
                df_editado.to_excel(writer, index=False)

                st.success(f'✅ Archivo Guardado Correctamente en: {complete_path}')

                st.dataframe(df_editado)
        except Exception as e:
            st.error(f'❌ Error al Guardar el Archivo: {e}')