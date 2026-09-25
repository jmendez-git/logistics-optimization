import os
import io
import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

user = st.session_state.user_info
st.title("📁 Panel de Vista")
st.info(f"Sesión activa como Administrativo: {user.get('name')} ({user.get('email')})")
st.divider()

SERVER_FOLDER = './databases'
NAME_FILE = 'test_01.xlsx'
COMPLETE_PATH = os.path.join(SERVER_FOLDER, NAME_FILE)


def generar_pdf(dataframe):
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30,
        title="Reporte de Clientes"
    )

    story = []
    styles = getSampleStyleSheet()

    titulo_estilo = ParagraphStyle(
        'TituloReporte',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=15
    )
    
    texto_estilo = ParagraphStyle(
        'TextoCelda',
        parent=styles['Normal'],
        fontSize=9,
        leading=11
    )

    story.append(Paragraph("📋 Reporte General de Clientes", titulo_estilo))
    story.append(Paragraph(f"Generado por: {user.get('name')} ({user.get('email')})", styles['Normal']))
    story.append(Spacer(1, 15))

    tabla_datos = []

    columnas_principales = list(dataframe.columns)
    tabla_datos.append([Paragraph(f"<b>{col}</b>", texto_estilo) for col in columnas_principales])

    # rows
    for _, fila in dataframe.iterrows():
        fila_texto = []
        for col in columnas_principales:
            val = str(fila[col]) if pd.notna(fila[col]) else ""
            fila_texto.append(Paragraph(val, texto_estilo))
        tabla_datos.append(fila_texto)

    ancho_columnas = (612 - 60) / len(columnas_principales)
    tabla_pdf = Table(tabla_datos, colWidths=[ancho_columnas] * len(columnas_principales))
    
    tabla_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f2f6')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e6e6e6')),
    ]))

    story.append(tabla_pdf)

    story.append(Spacer(1, 20))
    story.append(Paragraph("<font size=7 color=gray>This is for informational purposes only. For medical advice or diagnosis, consult a professional. AI responses may include mistakes.</font>", styles['Normal']))


    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


if os.path.exists(COMPLETE_PATH):
    st.write("### Datos almacenados en el servidor")
    
    df_vista = pd.read_excel(COMPLETE_PATH)
    
    st.dataframe(df_vista, use_container_width=True)
    
    st.divider()
    st.write("##### Exportar Información")

    try:
        pdf_data = generar_pdf(df_vista)
        
        st.download_button(
            label="Descargar Reporte en PDF",
            data=pdf_data,
            file_name="reporte_clientes.pdf",
            mime="application/pdf",
            type="primary"
        )
    except Exception as e:
        st.error(f"Hubo un problema al estructurar el PDF: {e}")
        
else:
    st.warning(f"⚠️ No se encontró ningún archivo guardado en la ruta: `{COMPLETE_PATH}`. Primero debes procesar y guardar un archivo desde el Panel de Administración.")