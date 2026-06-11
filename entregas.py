# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
#import webbrowser
import plotly.express as px
import yfinance as yf

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format','{:.2f}'.format)

caminho = 'Entregas.xlsx'

euro = yf.Ticker('EURBRL=X')


df_entregas = pd.read_excel(caminho)
df_entregas['Data'] = pd.to_datetime(df_entregas['Data'])
df_entregas['Mês'] = df_entregas['Data'].dt.month_name()
df_entregas['Data'] = pd.to_datetime(df_entregas['Data']).dt.date
df_entregas['Data'] = pd.to_datetime(df_entregas['Data'])  # converte antes!
df_entregas = df_entregas.fillna(0)                                                # fillna depois

df_entregas['Paack'] = df_entregas['Paack'].astype(int)
df_entregas['Ecoscouting'] = df_entregas['Ecoscouting'].astype(int)


valor_paack = float(0.80)
valor_Ecoscouting = float(0.60)
conveu = euro.history(period='1d')['Close'].iloc[-1]

df_entregas['qtdias'] = df_entregas['Data'].value_counts()
df_entregas['Dias'] = df_entregas['qtdias'].fillna(1).astype(int)
df_entregas['Total € Paack'] = (df_entregas['Paack']*valor_paack).round(2)
df_entregas['Total € Ecoscouting'] = (df_entregas['Ecoscouting']*valor_Ecoscouting).round(2)
df_entregas['Total €'] = (df_entregas['Total € Paack'] + df_entregas['Total € Ecoscouting']).round(2)
df_entregas['Total Conv R$'] = (df_entregas['Total €']*conveu).round(2)

consolidado = df_entregas.groupby('Mês')[[
    'Dias',
    'Paack',
    'Ecoscouting',
    'Total € Paack',
    'Total € Ecoscouting',
    'Total €',
    'Total Conv R$'
    ]].sum().reset_index()

pordia = df_entregas[[
    'Data',
    'Paack',
    'Total € Paack',
    'Ecoscouting',
    'Total € Ecoscouting',
    'Total €',
    'Total Conv R$'
    ]]

pri_quinzena = df_entregas['Data']<pd.to_datetime('2026-05-16')
seg_quinzena = df_entregas['Data']>pd.to_datetime('2026-05-15')

priquin_dias = df_entregas[pri_quinzena][[
    'Data',
    'Paack',
    'Total € Paack',
    'Ecoscouting',
    'Total € Ecoscouting',
    'Total €',
    'Total Conv R$'
    ]]


quin_dias = df_entregas[seg_quinzena][[
    'Data',
    'Paack',
    'Total € Paack',
    'Ecoscouting',
    'Total € Ecoscouting',
    'Total €',
    'Total Conv R$'
    ]]


graf = px.bar(consolidado, x='Mês', y=['Paack', 'Ecoscouting'], barmode='group')
graf_eu = px.bar(consolidado, x='Mês', y=['Total € Paack', 'Total € Ecoscouting'], barmode='group')

st.header('Dashboard de Entregas')

st.metric('Cotação Euro/R$', f'R$ {conveu:.2f}')

st.subheader('Consolidado Mês')
st.dataframe(consolidado)

st.subheader('1º quinzena')

col1,col2,col3  = st.columns(3)


col1.metric('Dias',f"{df_entregas[pri_quinzena]['Dias'].sum()}")
col2.metric('Paack', f"{df_entregas[pri_quinzena]['Paack'].sum()}")
col3.metric('Ecoscouting', f"{df_entregas[pri_quinzena]['Ecoscouting'].sum()}")

st.caption('Valor arrecadado')
col4,col5,col6,col7 = st.columns(4)

col4.metric('Total € Paack', f"€ {df_entregas[pri_quinzena]['Total € Paack'].sum():.2f}")
col5.metric('Total € Ecoscouting', f"€ {df_entregas[pri_quinzena]['Total € Ecoscouting'].sum():.2f}")
col6.metric('Total €', f"€ {df_entregas[pri_quinzena]['Total €'].sum():.2f}")
col7.metric('Total Conv R$', f"R$ {df_entregas[pri_quinzena]['Total Conv R$'].sum():.2f}")

st.dataframe(priquin_dias)

st.subheader('2º quinzena')

col1,col2,col3  = st.columns(3)


col1.metric('Dias',f"{df_entregas[seg_quinzena]['Dias'].sum()}")
col2.metric('Paack', f"{df_entregas[seg_quinzena]['Paack'].sum()}")
col3.metric('Ecoscouting', f"{df_entregas[seg_quinzena]['Ecoscouting'].sum()}")

st.caption('Valor arrecadado')
col4,col5,col6,col7 = st.columns(4)

col4.metric('Total € Paack', f"€ {df_entregas[seg_quinzena]['Total € Paack'].sum():.2f}")
col5.metric('Total € Ecoscouting', f"€ {df_entregas[seg_quinzena]['Total € Ecoscouting'].sum():.2f}")
col6.metric('Total €', f"€ {df_entregas[seg_quinzena]['Total €'].sum():.2f}")
col7.metric('Total Conv R$', f"R$ {df_entregas[seg_quinzena]['Total Conv R$'].sum():.2f}")


st.dataframe(quin_dias)
st.subheader('Por dia')
st.dataframe(pordia)

st.subheader('Quantidade de Produto Entregue')
st.plotly_chart(graf)

st.subheader('Valor Arrecadado')
st.plotly_chart(graf_eu)

#st.bar_chart(consolidado.set_index('Mês')[['Paack', 'Ecoscouting']])

#webbrowser.open('http://localhost:8501')

