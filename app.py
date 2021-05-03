#import librairies
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sb

##Data Cleaning
df_2017 = pd.read_csv('IST_Civil_Pav_2017_Ene_Cons.csv')
df_2018 = pd.read_csv('IST_Civil_Pav_2018_Ene_Cons.csv')
df_holiday = pd.read_csv('holiday_17_18_19.csv')
df_meteo = pd.read_csv('IST_meteo_data_2017_2018_2019.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.concat([df_2017,df_2018])
df['Date_start'] = pd.to_datetime(df['Date_start'])
df = df.set_index ('Date_start', drop = True)
df_meteo.rename(columns = {'yyyy-mm-dd hh:mm:ss': 'Date'}, inplace = True)
df_meteo['Date'] = pd.to_datetime(df_meteo['Date'])
df_meteo = df_meteo.set_index ('Date', drop = True)
df_meteo = df_meteo.iloc[:186028,:] #Year 2019 removed
df_meteo = df_meteo.resample('H').mean() 
df = pd.merge(df, df_meteo, left_index=True, right_index=True, how ='outer')
df['Hour'] = df.index.hour
df['Day week'] = df.index.dayofweek
df['Date'] = df.index.date
df = df.set_index ('Date', drop = True)
df_holiday['Date'] = pd.to_datetime(df_holiday['Date'])
df_holiday = df_holiday.set_index ('Date', drop = True)
df_holiday = df_holiday.iloc[:28,:] #Year 2019 removed
df = pd.merge(df, df_holiday, left_index=True, right_index=True, how ='outer')
df['Holiday'] = df['Holiday'].fillna(0)  # NaN must be replaced by 0
df = df.reindex(columns=['Power_kW','temp_C','Hour','Day week','Holiday','HR','windSpeed_m/s','pres_mbar','solarRad_W/m2','rain_mm/h','rain_day']) 
    # Create a copy before removing some values to save initial data for later
dfi = df.copy()
index_with_nan = df.index[df.isnull().any(axis=1)]
df.drop(index_with_nan,0, inplace=True)


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='IST Energy Monitor- TEST '),

html.Div(children='''
        Visualization of total electricity consumption at IST over the last years
    '''),
    
## Exploratory data analysis
fig = plt.figure(2,figsize=(15,4))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)
fig.add_subplot(121)
plt.plot(df['Power_kW'])
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Power_kW')
fig.add_subplot(122)
sb.boxplot(x=df['Power_kW'])

 


if __name__ == '__main__':
    app.run_server(debug=False)
