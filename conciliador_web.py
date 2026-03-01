# --- 1. LOGICA DE AGRUPACIÓN (SOLO ESTE CAMBIO) ---
    # Agrupamos por Nit y sumamos Débitos y Créditos
    df_resumen = df_total.groupby('Nit', as_index=False).agg({
        'Débito VES': 'sum',
        'Crédito VES': 'sum'
    })

    # Cálculo: El mayor menos el menor (Resta total absoluta)
    df_resumen['Diferencia Total'] = (df_resumen['Débito VES'] - df_resumen['Crédito VES']).abs()

    # --- 2. VISTA PREVIA DEL RESUMEN EN LA WEB ---
    st.markdown("---")
    st.subheader(f"📊 Resumen Agrupado por NIT - {empresa}")
    st.dataframe(df_resumen, use_container_width=True)

    # --- 3. GENERAR EXCEL CON LAS DOS PESTAÑAS ---
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Mantenemos tu pestaña de detalle igual
        df_total.to_excel(writer, index=False, sheet_name='Detalle_Movimientos')
        
        # Agregamos la nueva pestaña de resumen
        df_resumen.to_excel(writer, index=False, sheet_name='Resumen')

        # Formato para que el Excel se vea profesional
        workbook = writer.book
        formato_v = workbook.add_format({'bold': True, 'bg_color': '#D9EAD3', 'border': 1})
        
        ws_res = writer.sheets['Resumen']
        for col_num, value in enumerate(df_resumen.columns.values):
            ws_res.write(0, col_num, value, formato_v)
            ws_res.set_column(col_num, col_num, 20)

    st.download_button(
        label="📥 Descargar Reporte Final (Detalle + Resumen)",
        data=buffer.getvalue(),
        file_name=f"Conciliacion_{empresa}_Final.xlsx",
        mime="application/vnd.ms-excel"
    )
