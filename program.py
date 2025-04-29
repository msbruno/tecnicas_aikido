import pandas as pd
import plotly.express as px
import streamlit as st

path = r'./exame.csv'
df = pd.read_csv(path, sep=',', decimal=',')

global_filter_graduacao = st.sidebar.multiselect("GRADUACAO", df.GRADUACAO.unique().tolist())
global_filter_tipo = st.sidebar.multiselect("TIPO WAZA", df.TIPO.unique().tolist())
global_filter_uke = st.sidebar.multiselect("ATAQUE", df.UKE.unique().tolist())
global_filter_nage = st.sidebar.multiselect("TÉCNICA", df.NAGE.unique().tolist())

filtered_df = df.copy()
if global_filter_graduacao:
    filtered_df = filtered_df[filtered_df['GRADUACAO'].isin(global_filter_graduacao)]
if global_filter_tipo:
    filtered_df = filtered_df[filtered_df['TIPO'].isin(global_filter_tipo)]
if global_filter_uke:
    filtered_df = filtered_df[filtered_df['UKE'].isin(global_filter_uke)]
if global_filter_nage:
    filtered_df = filtered_df[filtered_df['NAGE'].isin(global_filter_nage)]

container = st.container()
col1 = container.columns(1)[0]
col1.markdown('# Técnicas do exame (cumulativo)')  
tab1, tab2 = col1.tabs(['Gráfico', 'Dados'])

agrupamento_tecnica = filtered_df.drop_duplicates(subset=['TIPO', 'UKE', 'NAGE', 'HANMI', 'OBS'])
filter_columns = tab1.selectbox("Filtro", ['TIPO', 'UKE', 'NAGE', 'HANMI', 'OBS'])
values = agrupamento_tecnica[filter_columns].value_counts().reset_index()
graduacao = agrupamento_tecnica.groupby('GRADUACAO')[filter_columns].value_counts().reset_index()
print(agrupamento_tecnica)
print(values)
fig1 = px.bar(graduacao, 
              title='QUANTIDADE DE TÉCNICAS POR GRADUAÇÃO',
              x='GRADUACAO', 
              y='count',
              color=filter_columns, 
              labels='TIPO',
              orientation='v')
tab1.plotly_chart(fig1)
tab2.dataframe(filtered_df)

col2 = container.columns(1)[0]
fig3 = px.pie(values,
              title='QUANTIDADE DE TÉCNICAS ACUMULADAS', 
              values='count',
            names=filter_columns)
col2.plotly_chart(fig3)


