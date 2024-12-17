import pandas as pd
import requests
import json
from datetime import date
import os

today = date.today()
year = today.year

key = os.getenv("API_KEYS") #API key
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
def bls_data_r (series, latest,**kwargs):
    # series is functional argument to allow a list of seriesID codes to be pulled from BLS
    if not isinstance(series, list):
        raise TypeError('series is not a list')
    #**kwargs allows for multiple parameters to be added to the function such as startyear and endyear, this done such **kwargs allows for multiple key arguments like startyear: 2022 if function paramtert reads startyear = 2022
    if latest not in ('true', 'false'):
        raise TypeError('latest is required true or false')
    headers = {'Content-type': 'application/json'}
    #as instructed by BLS keywords are written in this particular manner to call series id and regeistration key use the following keywords to call additional information from BLS.
    p = {'seriesid': series, 'registrationKey': key, 'latest': latest,}
    p.update(kwargs)
    # allows for the additional keyword arguments like startyear and endyear to be included in the API request to BLS
    p = json.dumps(p)
    bls = requests.post(url, data= p, headers=headers)
    data = json.loads(bls.text)
    return data

series = ["CES0000000001", "LNS14000000","LNS11000000","LNS11300000", "SUUR0000SA0E"]
#series of data from BLS being collected

#following code checks if the "SemesterProject_Gamboa repository has bls_data
username = "jgamboaurrego"
repository = "SemesterProject_Gamboa"
file_path = "bls_data.csv"
urlg = f'https://api.github.com/repos/{username}/{repository}/contents/{file_path}'
response = requests.get(urlg)

#if response does have a csv with bls data then it will add new data to prevent accidental duplication if github workflow is run more than once a month it removes duplicate in csv file. If there is no bls data found it will pull history starting from 2022 to now
if response.status_code == 200:
    json_data_l = bls_data_r(series,latest='true')
    bls_df_l = []
    for series in json_data_l['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            bls_df_l.append([seriesId, year, period, value])
    bls_df_l = pd.DataFrame(bls_df_l, columns = ['seriesId', 'year', 'period', 'value'])
    bls_df_l.to_csv("bls_data.csv", mode='a', header=False, index=False)
    bls_df_c = pd.read_csv("bls_data.csv")
    bls_df_c.drop_duplicates(inplace=True) #removes duplicates if new BLS data isn't available or accidential refreash
    bls_df_c.to_csv("bls_data.csv", index = False) # replaces bls_data.csv with clean results
else:
    json_data =bls_data_r(series, latest= "false" ,startyear = 2022 , endyear = (year)) # pulls data from most resent year and starting year of 2022
    bls_df = []
    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            bls_df.append([seriesId, year, period, value])
    bls_df = pd.DataFrame(bls_df, columns = ['seriesId', 'year', 'period', 'value'])
    bls_df.to_csv("bls_data.csv", index=False)