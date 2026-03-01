import streamlit as st
import pandas as pd
from io import BytesIO

# 1. Configuración de Marca y Estilo
st.set_page_config(page_title="Dep. Impuestos | Conciliador", layout="wide", page_icon="🏦")

# Estilo personalizado con CSS para mejorar la estética
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. Encabezado Profesional
col_logo, col_titulo = st.columns([1, 5])
with col_titulo:
    st.title("🏦 Departamento de Impuestos")
    st.subheader("Sistema de Conciliación Automática")

# 3. Instrucciones para el Personal (Lo que pediste antes)
with st.expander("📢 Guía de uso para el equipo"):
    st.info("""
    1. Selecciona la empresa en el menú lateral.
    2. Sube los archivos (Libro de Compras/Ventas y Resumen Fiscal).
    3. Asegúrate de que las columnas se llamen 'Fecha', 'Débito VES' y 'Crédito VES'.
    """)

# 4. Filtros en la barra lateral
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2652/2652134.png", width=100) # Icono genérico de impuestos
    st.header("Configuración")
    empresa = st.selectbox("Empresa:", ["Febeca", "Beval", "Sillaca"])
    mes = st.selectbox("Mes de Conciliación:", ["Enero", "Febrero", "Marzo", "Abril"])
    st.divider()
    st.success(f"Sesión activa: {empresa}")

# 5. Área de Carga de Archivos
st.markdown("---")
archivos = st.file_uploader(f"📂 Arrastra aquí los archivos Excel de {empresa}", type="xlsx", accept_multiple_files=True)

if archivos:
    lista_df = []
    for archivo in archivos:
        df = pd.read_excel(archivo)
        df['origen'] = archivo.name
        lista_df.append(df)
    
    df_total = pd.concat(lista_df, ignore_index=True)

    # Lógica de limpieza que ya tenías
    if 'Fecha' in df_total.columns:
        df_total['Fecha'] = pd.to_datetime(df_total['Fecha'], errors='coerce').dt.strftime('%d/%m/%Y')
    
    if 'Débito VES' in df_total.columns and 'Crédito VES' in df_total.columns:
        df_total['Débito VES'] = df_total['Débito VES'].fillna(0)
        df_total['Crédito VES'] = df_total['Crédito VES'].fillna(0)
        df_total['Diferencia_Neta'] = (df_total['Débito VES'] - df_total['Crédito VES']).abs()

    # 6. RESUMEN VISUAL (Métricas)
    st.markdown(f"### 📊 Resumen de Resultados: {empresa}")
    m1, m2, m3 = st.columns(3)
    
    total_debito = df_total['Débito VES'].sum() if 'Débito VES' in df_total.columns else 0
    total_credito = df_total['Crédito VES'].sum() if 'Crédito VES' in df_total.columns else 0
    
    m1.metric("Total Débitos", f"Bs. {total_debito:,.2f}")
    m2.metric("Total Créditos", f"Bs. {total_credito:,.2f}")
    m3.metric("Diferencia Neta", f"Bs. {(total_debito - total_credito):,.2f}")

    # 7. Vista Previa y Descarga
    with st.container():
        st.write("### 📝 Vista Previa del Análisis")
        st.dataframe(df_total, use_container_width=True)

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_total.to_excel(writer, index=False, sheet_name='Resultado')
        
        st.download_button(
            label="📥 Descargar Reporte Final para Auditoría",
            data=buffer.getvalue(),
            file_name=f"conciliacion_{empresa}_{mes}.xlsx",
            mime="application/vnd.ms-excel",
            help="Haz clic para bajar el archivo procesado"
        )
        st.balloons()

