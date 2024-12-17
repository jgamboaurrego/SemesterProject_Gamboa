import pandas as pd
import requests
import json
from datetime import date

today = date.today()
year = today.year

key = "b30c43cc00de4e1ebf5a9674bdddefdb"
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
def bls_data_r (series, latest,**kwargs):
    #as instructed by BLS keywords are written in this particular manner to call series id and regeistration key use the following key words to call additional information from BLS.
    if latest not in ('true', 'false'):
        raise 'latest is required true or false'
    headers = {'Content-type': 'application/json'}
    p = {'seriesid': series, 'registrationKey': key, 'latest': latest}
    #kwargs allows the method to accept multiple arugments such as startyear, endyear, 'annualaverage'
    p.update(kwargs)
    p = json.dumps(p)
    bls = requests.post(url, data= p, headers=headers)
    data = json.loads(bls.text)
    return data

#sellection of various BLS series IDs  pulled from BLS
series = ["CES0000000001", "LNS14000000","LNS11000000","LNS11300000", "SUUR0000SA0E"]

username = "jgamboaurrego"
repository = "SemesterProject_Gamboa"
file_path = "bls_data.csv"

urlg = f'https://api.github.com/repos/{username}/{repository}/contents/{file_path}'

response = requests.get(urlg)

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
else:
    json_data =bls_data_r(series, latest= "false" ,startyear = 2022 , endyear = (year))
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