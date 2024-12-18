import streamlit as st
import pandas as pd

st.title("Business Bureau of Labor Statistic Monthly Data")

data = pd.read_csv('https://raw.githubusercontent.com/jgamboaurrego/SemesterProject_Gamboa/refs/heads/Test/bls_data.csv')

data['Period Type'] = data['period'].str.slice(0,1)
data["Month"] = data["period"].str.slice(1)
data["Month"] = data["Month"].astype(int)
seriesID = ["CES0000000001", "LNS14000000","LNS11000000","LNS11300000", "SUUR0000SA0E"]
seriesName = ["Total NonFarm (Seas)", "Unemployment Rate (Seas)","Civilian Labor Force Level (Seas)","Labor Force Participation Rate", "CPI Energy in U.S City Average (Seas)"]

data["Series Name"] = data['seriesId'].replace(seriesID, seriesName)

data["Date"] = pd.to_datetime({'year': data['year'], 'month': data['Month'], 'day': 1})

#box to select category in dashboard

select_seriesname = st.selectbox('Select Series', data['Series Name'].unique())

f_data = data[data['Series Name'] == select_seriesname]

st.line_chart(f_data, x='Date', y='value')