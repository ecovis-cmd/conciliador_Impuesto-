import streamlit as st

# 1. Configuración de la página y Logo Principal
st.set_page_config(page_title="Centro de Impuestos", layout="wide")

# Puedes colocar un logo general aquí
# st.image("URL_DE_TU_LOGO_PRINCIPAL") 

st.title("🏦 Centro de Conciliación de Impuestos")

# 2. Selección de Empresa en la barra lateral
with st.sidebar:
    st.header("🏢 Selección de Empresa")
    empresa = st.selectbox(
        "Seleccione el cliente:",
        ["Empresa A, C.A.", "Corporación B", "Servicios C, S.A."]
    )
    
    # Mostrar logo según la empresa elegida
    if empresa == "Empresa A, C.A.":
        st.info("📂 Departamento de Impuestos - Empresa A")
        # st.image("URL_LOGO_A")
    elif empresa == "Corporación B":
        st.info("📂 Departamento de Impuestos - Corp B")

st.divider()

# 3. Crear pestañas para diferentes tipos de conciliaciones
# Esto te permite tener múltiples "Browse Files" organizados
tab1, tab2, tab3 = st.tabs(["📊 IVA", "💰 ISLR", "📝 Retenciones"])

with tab1:
    st.subheader(f"Conciliación de IVA - {empresa}")
    col1, col2 = st.columns(2)
    with col1:
        file_ventas = st.file_uploader("Subir Libro de Ventas", type=["xlsx"], key="iva_v")
    with col2:
        file_fiscal = st.file_uploader("Subir Resumen Fiscal", type=["xlsx"], key="iva_f")

with tab2:
    st.subheader(f"Conciliación de ISLR - {empresa}")
    file_islr = st.file_uploader("Subir Estado de Resultados", type=["xlsx"], key="islr")

with tab3:
    st.subheader(f"Cruce de Retenciones - {empresa}")
    file_ret = st.file_uploader("Subir Comprobantes de Retención", type=["xlsx"], key="ret")
