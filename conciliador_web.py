import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Conciliador Pro", layout="wide")
st.title("📊 Mi Conciliador Automático")

archivos = st.file_uploader("Arrastra aquí tus archivos Excel", type="xlsx", accept_multiple_files=True)

if archivos:
    lista_df = []
    for archivo in archivos:
        df = pd.read_excel(archivo)
        df['origen'] = archivo.name
        lista_df.append(df)
    
    df_total = pd.concat(lista_df, ignore_index=True)

    # Formato de Fecha y Diferencia Positiva
    if 'Fecha' in df_total.columns:
        df_total['Fecha'] = pd.to_datetime(df_total['Fecha'], errors='coerce').dt.strftime('%d/%m/%Y')
    
    if 'Débito VES' in df_total.columns and 'Crédito VES' in df_total.columns:
        df_total['Débito VES'] = df_total['Débito VES'].fillna(0)
        df_total['Crédito VES'] = df_total['Crédito VES'].fillna(0)
        df_total['Diferencia_Neta'] = (df_total['Débito VES'] - df_total['Crédito VES']).abs()

    st.write("### Vista previa de los datos:")
    st.dataframe(df_total)

    # --- NUEVA DESCARGA EN EXCEL REAL ---
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_total.to_excel(writer, index=False, sheet_name='Conciliacion')
    
    st.download_button(
        label="📥 Descargar Excel Profesional (.xlsx)",
        data=output.getvalue(),
        file_name="conciliacion_final.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )