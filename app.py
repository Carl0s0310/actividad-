"""
Streamlit dashboard para la actividad - Universidad de la Costa, Programa Minería de Datos
Integrantes: Hernando Luiz Calvo Ochoa, Carlos Antonio Ardila Ruiz
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Dashboard - Universidad de la Costa")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data("/mnt/data/university_student_data.csv")

st.title("Dashboard: Admisión · Retención · Satisfacción")
st.write("Universidad de la Costa — Programa Minería de Datos")
# Filtros
years = sorted(df['Year'].dropna().unique().tolist()) if 'Year' in df.columns else []
terms = sorted(df['Term'].dropna().unique().tolist()) if 'Term' in df.columns else []
depts = sorted(df['None'].dropna().unique().tolist()) if 'None' in df.columns else []

col1, col2, col3 = st.sidebar.columns([1,1,1])
with st.sidebar:
    selected_year = st.selectbox("Año", options=['Todos']+years, index=0)
    selected_term = st.selectbox("Término", options=['Todos']+terms, index=0)
    selected_dept = st.selectbox("Departamento", options=['Todos']+depts, index=0)

filtered = df.copy()
if selected_year != 'Todos':
    filtered = filtered[filtered['Year'] == selected_year]
if selected_term != 'Todos':
    filtered = filtered[filtered['Term'] == selected_term]
if selected_dept != 'Todos':
    filtered = filtered[filtered['None'] == selected_dept]

st.subheader("Indicadores clave")
cols = st.columns(3)
# KPIs simples si las columnas existen
if 'Retention Rate (%)' in df.columns:
    kpi_ret = filtered['Retention Rate (%)'].mean()
    cols[0].metric("Tasa de retención (media)", f"{kpi_ret:.2f}")
else:
    cols[0].write("Tasa de retención: columna no encontrada")

if 'Student Satisfaction (%)' in df.columns:
    kpi_sat = filtered['Student Satisfaction (%)'].mean()
    cols[1].metric("Satisfacción (media)", f"{kpi_sat:.2f}")
else:
    cols[1].write("Satisfacción: columna no encontrada")

cols[2].write("Integrantes:\n- Hernando Luiz Calvo Ochoa\n- Carlos Antonio Ardila Ruiz")


st.subheader("Visualizaciones")
# Retention over time
if 'Year' in df.columns and 'Retention Rate (%)' in df.columns:
    ret_by_year = filtered.groupby('Year')['Retention Rate (%)'].mean().reset_index()
    st.line_chart(ret_by_year.set_index('Year'))

# Satisfaction by year
if 'Year' in df.columns and 'Student Satisfaction (%)' in df.columns:
    sat_by_year = filtered.groupby('Year')['Student Satisfaction (%)'].mean().reset_index()
    st.bar_chart(sat_by_year.set_index('Year'))

# Satisfaction by term
if 'Term' in df.columns and 'Student Satisfaction (%)' in df.columns:
    sat_by_term = filtered.groupby('Term')['Student Satisfaction (%)'].mean().reset_index()
    st.write(sat_by_term)
    fig, ax = plt.subplots()
    ax.pie(sat_by_term['Student Satisfaction (%)'], labels=sat_by_term['Term'], autopct='%1.1f%%')
    st.pyplot(fig)

st.write("---")
st.write("Repositorio y despliegue: sube este repo a GitHub y luego conéctalo a Streamlit Cloud (https://streamlit.io/cloud)")
