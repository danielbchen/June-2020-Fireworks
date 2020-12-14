import matplotlib.pyplot as plt
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


def plotter():
    '''
    '''

    df = fireworks_data_loader()

    '''Prep data to create subplot showing daily reports'''
    daily_reports = incident_grouper(df, 'D')

    daily_reports = (daily_reports[(daily_reports['created_date'] >= '2020-06-01') &
                                   (daily_reports['created_date'] < '2020-07-11')])

    june_days = ['June ' + str(number) for number in range(1, 31)]
    july_days = ['July ' + str(number) for number in range(1, 11)]
    daily_reports_x_labels = june_days + july_days

    '''Prep data to create subplot showing reports in June over time'''
    june_reports = incident_grouper(df, 'M')
    june_reports['created_date'] = june_reports['created_date'].astype(str)
    june_reports = june_reports[june_reports['created_date'].str.endswith('06-30')]
    june_reports_x_labels = ['June ' + str(year) for year in range(2010, 2021)]


    fig, axs = plt.subplots(2, 1, figsize=(18, 20))

    plt.rcParams['font.family'] = 'arial'

    '''Plot first subplot'''
    axs[0].fill_between(daily_reports['created_date'], daily_reports['fireworks'],
                        color='skyblue', alpha=0.4)
    axs[0].plot(daily_reports['created_date'], daily_reports['fireworks'])

    axs[0].set_title('Number of Daily Reported Illegal Fireworks in 2020 \n',
                     fontsize=16)
    axs[0].set_xticks(daily_reports['created_date'])
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

    plt.show();
    #plt.save_fig('', dpi=600)
    #plt.close()



