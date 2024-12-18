import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.title("Business Bureau of Labor Statistic Monthly Data")

data = pd.read_csv('https://raw.githubusercontent.com/jgamboaurrego/SemesterProject_Gamboa/refs/heads/Test/bls_data.csv')

data['Period Type'] = data['period'].str.slice(0,1)
data["Month"] = data["period"].str.slice(1)
data["Month"] = data["Month"].astype(int)
seriesID = ["CES0000000001", "LNS14000000","LNS11000000","LNS11300000", "SUUR0000SA0E"]
seriesName = ["Total NonFarm (Seas)", "Unemployment Rate (Seas)","Civilian Labor Force Level (Seas)","Labor Force Participation Rate", "CPI Energy in U.S City Average"]

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
#creates time slicer to affect graphics
e = data['Date'].min()
l = data['Date'].max()
#due to pandas converting dates to timestamps to_pydateime() was used to convert it to method streamlit can understand
earliest_date = e.to_pydatetime()
latest_date = l.to_pydatetime()
select_time = st.sidebar.slider('Select Time Period', min_value=earliest_date, max_value= latest_date,
                                value = (earliest_date, latest_date), format = "YYYY-MM")

#box to select category in dashboard to affect graphics displayed
select_seriesname = st.sidebar.selectbox('Select Series', data['Series Name'].unique())

#pd.to_datetime was used to convert back selected time from datetime.datetime to timestamp so pandas dataframe could filter
f_time = data[(data['Date'].dt.to_period("M") >= pd.to_datetime(select_time[0]).to_period("M"))
              & (data['Date'].dt.to_period("M") <= pd.to_datetime(select_time[1]).to_period("M"))]

f_data = f_time[f_time['Series Name'] == select_seriesname]

fig = px.line(f_data, x = "Date", y = "value", title = select_seriesname)

if select_seriesname == "Total NonFarm (Seas)":
    fig.update_layout(yaxis_title = "All Employess (Thousands)")
elif select_seriesname == 'Unemployment Rate (Seas)':
    fig.update_layout( yaxis_title = "Percent of rate")
elif select_seriesname == 'Labor Force Participation Rate':
    fig.update_layout( yaxis_title = "Percent of rate")
elif select_seriesname == 'Civilian Labor Force Level (Seas)':
    fig.update_layout(yaxis_title = "Labor Force (Thousands)")
elif select_seriesname == 'CPI Energy in U.S City Average':
    fig.update_layout( yaxis_title = "Price Energy")
else:
    fig.update_layout( yaxis_title = "value")

st.plotly_chart(fig, use_container_width=True)