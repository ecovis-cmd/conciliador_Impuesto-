import streamlit as st
import pandas as pd

# Configuración inicial
st.set_page_config(page_title="Centro de Impuestos", layout="wide")
st.title("🏦 Centro de Conciliación de Impuestos")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🏢 Selección de Empresa")
    empresa = st.selectbox("Seleccione el cliente:", ["Febeca", "Beval", "Sillaca"])
    st.info(f"Trabajando con: {empresa}")

# --- SECCIÓN DE INSTRUCCIONES (Expander) ---
with st.expander("📢 MANUAL PARA EL PERSONAL (Haz clic aquí)"):
    st.markdown(f"""
    ### Pasos para {empresa}:
    1. **Descarga:** Bajar el 'Libro de Compras' y el 'Resumen de Retenciones' en **.xlsx**.
    2. **No editar:** El sistema busca columnas específicas. No cambies nombres ni orden.
    3. **Subida:** Ve a la pestaña **Retenciones** y carga ambos archivos.
    4. **Resultado:** Si hay diferencias, aparecerán resaltadas en rojo.
    """)

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["📊 IVA", "📝 Retenciones"])

with tab2:
    st.subheader(f"Cruce de Retenciones - {empresa}")
    
    col1, col2 = st.columns(2)
    with col1:
        file_libro = st.file_uploader("1. Subir Libro de Compras", type=["xlsx"], key="l_compras")
    with col2:
        file_fiscal = st.file_uploader("2. Subir Resumen Fiscal (SENIAT)", type=["xlsx"], key="r_fiscal")

    # --- LÓGICA DE CONCILIACIÓN ---
    if file_libro and file_fiscal:
        try:
            # Leer los archivos
            df_libro = pd.read_excel(file_libro)
            df_fiscal = pd.read_excel(file_fiscal)

            st.success("¡Archivos cargados! Comparando montos...")

            # Ejemplo de lógica: Supongamos que ambos tienen una columna 'Rif' y 'Monto'
            # Aquí el programa busca diferencias
            total_libro = df_libro['Monto'].sum() if 'Monto' in df_libro.columns else 0
            total_fiscal = df_fiscal['Monto'].sum() if 'Monto' in df_fiscal.columns else 0
            diferencia = total_libro - total_fiscal

            # Mostrar resultados
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Libro", f"{total_libro:,.2f}")
            c2.metric("Total Fiscal", f"{total_fiscal:,.2f}")
            c3.metric("Diferencia", f"{diferencia:,.2f}", delta=-diferencia)

            if diferencia == 0:
                st.balloons()
                st.success("✅ ¡Todo coincide perfectamente!")
            else:
                st.error("⚠️ Se detectaron diferencias entre los reportes.")
        
        except Exception as e:
            st.warning("Asegúrate de que los Excel tengan una columna llamada 'Monto'.")

