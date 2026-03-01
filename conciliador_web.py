import streamlit as st
import pandas as pd
from io import BytesIO

# 1. Configuración de la Página
st.set_page_config(page_title="Dep. Impuestos | Conciliador Pro", layout="wide", page_icon="🏦")

# 2. Estilo Visual Profesional (CSS corregido)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 3. Encabezado del Departamento
st.title("🏦 Departamento de Impuestos")
st.subheader("Sistema de Conciliación y Validación Fiscal")

# 4. Barra Lateral: Selección de Empresa
with st.sidebar:
    st.header("🏢 Configuración")
    empresa = st.selectbox("Seleccione la Empresa:", ["Febeca", "Beval", "Sillaca"])
    mes = st.selectbox("Mes de Proceso:", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"])
    st.divider()
    if empresa == "Febeca":
        st.info("📂 Conectado a: Febeca")
    else:
        st.info(f"📂 Conectado a: {empresa}")

# 5. Manual de Instrucciones para el Personal
with st.expander("📢 MANUAL DE USUARIO (Instrucciones de Carga)"):
    st.markdown(f"""
    1. **Descarga:** Obtener el reporte en formato **Excel (.xlsx)** del sistema.
    2. **Columnas:** El archivo debe contener: *Fecha, Nit, Débito VES, Crédito VES*.
    3. **Carga:** Arrastre los archivos al recuadro de abajo.
    4. **Resumen:** El sistema agrupará los totales por NIT automáticamente para su validación fiscal.
    """)

st.divider()

# 6. Área de Carga de Archivos (Corregido: st.file_uploader)
archivos = st.file_uploader(f"Subir archivos Excel para {empresa}", type=["xlsx"], accept_multiple_files=True)

if archivos:
    lista_df = []
    for archivo in archivos:
        df = pd.read_excel(archivo)
        df['origen'] = archivo.name
        lista_df.append(df)
    
    # Unión de todos los archivos
    df_total = pd.concat(lista_df, ignore_index=True)

    # Ordenar columnas según tu requerimiento visual
    columnas_ordenadas = ['origen', 'Fuente', 'Asiento', 'Referencia', 'Cuenta Conta', 'Fecha', 'Nit', 'Débito VES', 'Crédito VES']
    cols_presentes = [c for c in columnas_ordenadas if c in df_total.columns]
    df_total = df_total[cols_presentes]

    # --- LÓGICA DE RESUMEN AGRUPADO POR NIT ---
    # Sumamos débitos y créditos por cada NIT único
    df_resumen = df_total.groupby('Nit', as_index=False).agg({
        'Débito VES': 'sum',
        'Crédito VES': 'sum'
    })
    
    # Diferencia: Mayor menos Menor (Valor Absoluto)
    df_resumen['Diferencia Total'] = (df_resumen['Débito VES'] - df_resumen['Crédito VES']).abs()

    # --- MOSTRAR RESULTADOS EN PANTALLA ---
    st.success(f"✅ Se han procesado {len(archivos)} archivos correctamente.")
    
    tab_detalle, tab_resumen = st.tabs(["📝 Detalle de Movimientos", "📊 Resumen por NIT (Fiscal)"])
    
    with tab_detalle:
        st.dataframe(df_total, use_container_width=True)
        
    with tab_resumen:
        st.write("Esta tabla suma todos los movimientos y muestra el saldo neto por RIF:")
        st.dataframe(df_resumen, use_container_width=True)

    # --- GENERAR EXCEL FINAL CON DOS PESTAÑAS ---
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_total.to_excel(writer, index=False, sheet_name='Detalle_Movimientos')
        df_resumen.to_excel(writer, index=False, sheet_name='Resumen_Fiscal')
        
        # Ajuste de formato para que se vea profesional
        workbook = writer.book
        formato_cabecera = workbook.add_format({'bold': True, 'bg_color': '#D9EAD3', 'border': 1})
        for hoja in ['Detalle_Movimientos', 'Resumen_Fiscal']:
            ws = writer.sheets[hoja]
            ws.set_column(0, 10, 18)

    st.download_button(
        label="📥 Descargar Reporte Final (2 Pestañas)",
        data=buffer.getvalue(),
        file_name=f"Reporte_{empresa}_{mes}.xlsx",
        mime="application/vnd.ms-excel"
    )
    st.balloons()
