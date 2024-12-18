import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

st.title("Business Bureau of Labor Statistic Monthly Data")

data = pd.read_csv('https://raw.githubusercontent.com/jgamboaurrego/SemesterProject_Gamboa/refs/heads/main/bls_data.csv')

#split period to "Period Type" and Month based on position of value this was
# done to account for changes in the data that my change "M" in M01 from M to lower case m for example.
data['Period Type'] = data['period'].str.slice(0,1)
data["Month"] = data["period"].str.slice(1)
data["Month"] = data["Month"].astype(int)
seriesID = ["CES0000000001", "LNS14000000","LNS11000000","LNS11300000", "SUUR0000SA0E"]
seriesName = ["Total NonFarm (Seas)", "Unemployment Rate (Seas)",
              "Civilian Labor Force Level (Seas)","Labor Force Participation Rate", "CPI Energy in U.S City Average"]

data["Series Name"] = data['seriesId'].replace(seriesID, seriesName)

#created Date column based on the year and month column
data["Date"] = pd.to_datetime({'year': data['year'], 'month': data['Month'], 'day': 1})

#sorted values based on date for the plotly graphs otherwise plotting of data may come with errors
data = data.sort_values('Date')
#created function to group values in seriesID together if they cover similar topics like employment and price
def catgroup(bls_name):
    if bls_name in ['"CES0000000001"',"LNS14000000","LNS11300000"]:
        return "Employment"
    elif bls_name in ["SUUR0000SA0E"]:
        return "Price"
    else:
        return "Other"

#Created BLS Category column using the created function
data['BLS Category'] = data['seriesId'].apply(catgroup)

st.header("BLS Timeseries Analysis of Data", divider="blue")
st.write("The graph below shows a time series of the monthly data provided by BLS for selected BLS data series. "
         "To select a specific BLS data series, go to the left sidebar filter and select the data series by its name. "
         "The chart's time periods in the x-axis can also be altered by the user from "
         "the time slider in the left sidebar to examine results between different points in time. ")


#header for Sidebar Filters
st.sidebar.header("Filters for BLS Time Series Line Charts")
e = data['Date'].min()
l = data['Date'].max()
#due to pandas converting dates to timestamps to_pydateime() was used to convert it to method streamlit can understand
earliest_date = e.to_pydatetime()
latest_date = l.to_pydatetime()
#creates time slicer to affect graphics
select_time = st.sidebar.slider('Select Time Period', min_value=earliest_date, max_value= latest_date,
                                value = (earliest_date, latest_date), format = "YYYY-MM")

#box to select category in dashboard to affect graphics displayed
select_seriesname = st.sidebar.selectbox('Select Series', data['Series Name'].unique())

#pd.to_datetime was used to convert back selected time from datetime.datetime to timestamp so pandas dataframe could filter
f_time = data[(data['Date'].dt.to_period("M") >= pd.to_datetime(select_time[0]).to_period("M"))
              & (data['Date'].dt.to_period("M") <= pd.to_datetime(select_time[1]).to_period("M"))]

f_data = f_time[f_time['Series Name'] == select_seriesname]

fig = px.line(f_data, x = "Date", y = "value", title = select_seriesname, markers=True ,
              color_discrete_sequence= px.colors.qualitative.Prism)

#based on selected category yaxis title will dynamically change
if select_seriesname == "Total NonFarm (Seas)":
    fig.update_layout(yaxis_title = "All Employees (Thousands)")
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

#used to plot plotly graphs on streamlit.
st.plotly_chart(fig, use_container_width=True)

st.header("BLS Annual Average Analysis", divider="green")
st.write("This bar chart, generated below, shows the annual average values for the selected BLS "
         "data series for all available years. To select a data series, "
         "navigate to the left sidebar and select it from the Select Series for Bar Chart drop-down menu.")

#create new data frame that averages values based on series name and year to provide annual average results.
annual_data = data.groupby(['Series Name', 'year'])['value'].mean().reset_index()

#header for second sidebar filters
st.sidebar.header("Filters for BLS Avg Analysis Bar Chart")
select_seriesname2 = st.sidebar.selectbox('Select Series for Bar Chart',
                                          annual_data['Series Name'].unique())

fa_data = annual_data[annual_data['Series Name'] == select_seriesname2]

fa_data['year'] = fa_data['year'].astype(str)

figb = px.bar(fa_data, x = 'year', y = 'value',text_auto= True ,
              color='year' ,title = select_seriesname2, color_discrete_sequence= px.colors.qualitative.G10_r)

#Renames yaxis based on selected series name
if select_seriesname == "Total NonFarm (Seas)":
    figb.update_layout(xaxis_title = "Year" ,yaxis_title = "Annual Average All Employees (Thousands)")
elif select_seriesname == 'Unemployment Rate (Seas)':
    figb.update_layout( xaxis_title = "Year",yaxis_title = "Average Percent of rate")
elif select_seriesname == 'Labor Force Participation Rate':
    figb.update_layout( xaxis_title = "Year", yaxis_title = "Average Percent of rate")
elif select_seriesname == 'Civilian Labor Force Level (Seas)':
    figb.update_layout(xaxis_title = "Year", yaxis_title = "Average Labor Force (Thousands)")
elif select_seriesname == 'CPI Energy in U.S City Average':
    figb.update_layout(xaxis_title = "Year" ,yaxis_title = "Average Price Energy")
else:
    figb.update_layout( xaxis_title = "Year" ,yaxis_title = "Average value")

#postioned data labels outside and font size control, cliponaxis preventing cut off when data label moves beyond axis
figb.update_traces(textfont_size= 12, textposition='outside', cliponaxis= False)

#This is to prevent weird tick marks from appearing in the x axes for year in the chart,
# dtick controls results to one year
figb.update_xaxes(dtick="Y1")

st.plotly_chart(figb, use_container_width=True)



#Below is the Third section showing scatter plot generator
st.header("BLS Scatter Plot: Looking for Relationships", divider="red")

st.write("This section of the dashbaord allows the user to play around with avaialbe bls data to determine a realationship "
         "between series values based on scatter plot. The dropdowns below allow user to select "
         "the x and y axis of scatter plot from available series names. Once those are selected user can click on"
         "create scatter plot button to generate the plot")


#pivoted data table in order to have series name be column name and its corresponding value in column value below
#used Date as index for the transformation
pdata = data.pivot(index='Date', columns='Series Name', values='value')

#Created a list of column names for the section box for x and y
columns = pdata.columns.tolist()

# allows you in streamlit to select the desired Series for X axis
x_c = st.selectbox('Select Series x axis', columns)
# allows you in streamlit to select the desired Series for Y axis
y_c = st.selectbox('Select Series y axis', columns)

#filtered pdate dataframe by selected x_c and y_c columns
pdata_f = pdata[[x_c, y_c]]
#renamed columns based on position this allows you to select the same series for both x and y.
pdata_f = pdata_f.set_axis(['x','y'], axis=1)

#created scatter plot based on selection
figs = px.scatter(pdata_f, x='x', y='y', color_discrete_sequence= px.colors.qualitative.G10_r)

#updated x and y axes name based on selected values
figs.update_layout(xaxis_title = x_c ,yaxis_title = y_c)

#created generation button to create Scatter plot once it is clicked
if st.button("Create Scatter Plot"):
    st.plotly_chart(figs, use_container_width=True)
