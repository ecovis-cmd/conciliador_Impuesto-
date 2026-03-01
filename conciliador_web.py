import streamlit as st
# Selección de Empresa en la barra lateral
with st.sidebar:
    st.header("🏢 Selección de Empresa")
    empresa = st.selectbox(
        "Seleccione el cliente:",
        ["Febeca", "Beval", "Sillaca"] # Aquí agregas tus 3 empresas
    )
    
    # Esto cambia el mensaje informativo según la empresa elegida
    if empresa == "Febeca":
        st.info("📂 Departamento de Impuestos - Febeca")
    elif empresa == "Beval":
        st.info("📂 Departamento de Impuestos - Beval")
    elif empresa == "Sillaca":
        st.info("📂 Departamento de Impuestos - Sillaca")

