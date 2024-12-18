import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Business Bureau of Labor Statistic Monthly Data")

data = pd.read_csv('https://raw.githubusercontent.com/jgamboaurrego/SemesterProject_Gamboa/refs/heads/Test/bls_data.csv')

data['Period Type'] = data['period'].str.slice(0,1)
data["Month"] = data["period"].str.slice(1)
data["Month"] = data["Month"].astype(int)
seriesID = ["CES0000000001", "LNS14000000","LNS11000000","LNS11300000", "SUUR0000SA0E"]
seriesName = ["Total NonFarm (Seas)", "Unemployment Rate (Seas)","Civilian Labor Force Level (Seas)","Labor Force Participation Rate", "CPI Energy in U.S City Average (Seas)"]

data["Series Name"] = data['seriesId'].replace(seriesID, seriesName)

data["Date"] = pd.to_datetime({'year': data['year'], 'month': data['Month'], 'day': 1})

data = data.sort_values('Date')

def catgroup(bls_name):
    if bls_name in ['"CES0000000001"',"LNS14000000","LNS11300000"]:
        return "Employment"
    elif bls_name in ["SUUR0000SA0E"]:
        return "Price"
    else:
        return "Other"

data['BLS Category'] = data['seriesId'].apply(catgroup)

st.header("BLS TimeSeries Analysis of Pricing Data")
#box to select category in dashboard

select_seriesname = st.selectbox('Select Series', data['Series Name'].unique())

f_data = data[data['Series Name'] == select_seriesname]

fig = px.line(f_data, x = "Date", y = "value", title = select_seriesname)

if f_data['Series Name'] == "Total NonFarm (Seas)":
    fig.update_layout(xaxis = "Date", yaxis = "All Employess (Thousands)")
elif f_data['Series Name'] == 'Unemployment Rate (Seas)':
    fig.update_layout(xaxis = "Date", yaxis = "Percent of rate")
elif f_data['Series Name'] == 'Labor Force Participation Rate':
    fig.update_layout(xaxis = "Date", yaxis = "Percent of rate")
elif f_data['Series Name'] == 'Civilian Labor Force Level (Seas)':
    fig.update_layout(xaxis = "Date", yaxis = "Labor Force (Thousands)")
elif f_data['Series Name'] == 'CPI Energy in U.S City Average (Seas)':
    fig.update_layout(xaxis = "Date", yaxis = "Price Energy")
else:
    fig.update_layout(xaxis = "Date", yaxis = "value")

st.plotly_chart(fig, use_container_width=True)