import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import numpy as np
import pandas as pd
import seaborn as sns
from sodapy import Socrata


def fireworks_data_loader():
    '''
    Loads in fireworks data from NYC 311.
    https://data.cityofnewyork.us/Social-Services/311-Fireworks-Complaints/g4u2-tvag
    '''

    client = Socrata('data.cityofnewyork.us', None)
    results = client.get_all('g4u2-tvag')

    df = pd.DataFrame.from_records(results)
    
    df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
    df['fireworks'] = [1 if complaint == 'Illegal Fireworks' else 0 for complaint in df['complaint_type']]

    return df 


def incident_grouper(dataframe, frequency):
    '''
    Takes in dataframe and returns a new dataframe grouped by a user-defined 
    frequency.
    '''

    df = dataframe.copy()

    df = (df.groupby(
          pd.Grouper(key='created_date', freq=frequency))
            .sum('fireworks')
            .reset_index())

    return df 


def date_filterer(dataframe, start, end):
    '''
    Subsets a dataframe by dates. 
    '''

    df = dataframe.copy()

    df = df[(df['created_date'] >= start) & (df['created_date'] < end)]

    return df


def plotter():
    '''
    Creates two subplots on one figure. 
    First shows reported illegal fireworks by day from June 1 to July 10 in 2020
    and 2019. 
    Second shows the total number of illegal fireworks reported in June from 
    2010 to 2020. 
    '''

    df = fireworks_data_loader()

    '''Prep data to create subplot showing daily reports'''
    daily_reports = incident_grouper(df, 'D')

    reports_2020 = date_filterer(daily_reports, '2020-06-01', '2020-07-11')
    reports_2019 = date_filterer(daily_reports, '2019-06-01', '2019-07-11')
    reports_2020['ID'] = range(len(reports_2020))
    reports_2019['ID'] = range(len(reports_2019))

    reports = reports_2020.merge(reports_2019, on='ID')

    reports = reports[['created_date_x', 'fireworks_x', 'fireworks_y']]
    reports.columns = ['Date', 'Fireworks_2020', 'Fireworks_2019']

    xaxis_dates = date2num(reports['Date'])

    width = .4

    june_days = ['June ' + str(number) for number in range(1, 31)]
    july_days = ['July ' + str(number) for number in range(1, 11)]
    daily_reports_x_labels = june_days + july_days

    '''Prep data to create subplot showing reports in June over time'''
    june_reports = incident_grouper(df, 'M')
    june_reports['created_date'] = june_reports['created_date'].astype(str)
    june_reports = june_reports[june_reports['created_date'].str.endswith('06-30')]
    june_reports_x_labels = ['June ' + str(year) for year in range(2010, 2021)]


    fig, axs = plt.subplots(2, 1, figsize=(20, 20))

    plt.rcParams['font.family'] = 'arial'

    '''Plot first subplot'''
    axs[0].bar(xaxis_dates - width / 2, reports['Fireworks_2020'], width, align='center')
    axs[0].bar(xaxis_dates + width / 2, reports['Fireworks_2019'], width, align='center')

    axs[0].set_title('Number of Daily Reported Illegal Fireworks in 2020 \n',
                     fontsize=16)
    axs[0].set_xticks(xaxis_dates)
    axs[0].set_xticklabels(daily_reports_x_labels, rotation='vertical')

    axs[0].margins(x=0, y=0)
    axs[0].spines['top'].set_visible(False)
    axs[0].spines['right'].set_visible(False)

    '''Plot second subplot'''
    axs[1].bar(june_reports['created_date'], june_reports['fireworks'])
    
    axs[1].set_title('\n Total Reported Cases in June Across the Past Decade \n',
                     fontsize=16)
    axs[1].set_xticklabels(june_reports_x_labels)

    axs[1].spines['top'].set_visible(False)
    axs[1].spines['right'].set_visible(False)

    fig.suptitle('Tracking Reported Cases of Illegal Fireworks in NYC',
                 fontsize=20, fontweight='bold',
                 x=0.5, y=0.94)
    fig.text(0.08, 0.5, 'Number of Calls to 311',
             ha='center', va='center', rotation=90, fontsize=16)

    #plt.show();
    plt.savefig('Reported Fireworks Cases in NYC.png', dpi=800, facecolor='white')
    plt.close()


def geo_loader():
    '''
    Loads in geojson of NYC zipcodes. 
    '''

    link = 'https://data.beta.nyc/dataset/3bf5fb73-edb5-4b05-bb29-7c95f4a727fc/resource/894e9162-871c-4552-a09c-c6915d8783fb/download/zip_code_040114.geojson'
    df = gpd.read_file(link)

    return df


def geo_fireworks_merger():
    '''
    Merges firework data from 311 with dataframe containing geometry.
    '''

    geo_df = geo_loader()
    fireworks_df = fireworks_data_loader()

    june_df = fireworks_df[(fireworks_df['created_date'] >= '2020-06-01') &
                           (fireworks_df['created_date'] < '2020-07-01')]
    june_df = (june_df.groupby('incident_zip')
                      .sum('fireworks')
                      .reset_index()
                      .rename(columns={'incident_zip': 'ZIPCODE',
                                       'fireworks'   : 'INCIDENT_COUNT'}))
    
    df = geo_df.merge(june_df, on='ZIPCODE', how='inner')

    return df


def choropleth_creator():
    '''
    Returns a choropleth showing the number of illegal fireworks reported to 
    311 in June by zip code. 
    '''

    df = geo_fireworks_merger()

    fig, ax = plt.subplots(figsize=(12, 12))

    df.plot(ax=ax, column='INCIDENT_COUNT', linewidth=0.5, edgecolor='black',
            legend=True, cmap='Reds', legend_kwds={'shrink': 0.7})
    #df.apply(lambda x: ax.annotate(s=x.ZIPCODE, color='black',
    #                               xy=x.geometry.centroid.coords[0], ha='center', fontsize=4),
    #                               axis=1)

    ax.axis('off')
    ax.set_title('Reports of Illegal Fireworks by Zip Code in June 2020',
                 fontsize=18, fontweight='bold')

    #plt.show();
    plt.savefig('Fireworks Choropleth.png', dpi=800, facecolor='white')
    plt.close()


if __name__ == '__main__':
    plotter()
    choropleth_creator()
