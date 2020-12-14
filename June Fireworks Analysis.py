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

    '''Create first subplot showing daily reports'''
    daily_reports = incident_grouper(df, 'D')

    daily_reports = (daily_reports[(daily_reports['created_date'] >= '2020-06-01') &
                                   (daily_reports['created_date'] < '2020-07-11')])

    june_days = ['June ' + str(number) for number in range(1, 31)]
    july_days = ['July ' + str(number) for number in range(1, 11)]
    daily_reports_x_labels = june_days + july_days

    fig, axs = plt.subplots(2, 1, figsize=(15, 10))

    axs[0].bar(daily_reports['created_date'], daily_reports['fireworks'])

    axs[0].set_title('Number of Daily Reported Illegal Fireworks \n')
    axs[0].set_xticks(daily_reports['created_date'])
    axs[0].set_xticklabels(daily_reports_x_labels, rotation='vertical')

    axs[0].spines['top'].set_visible(False)
    axs[0].spines['right'].set_visible(False)

    plt.show();


################################################################################

# Now let's compare over the long term. Let's look at reports of fireworks by
# months over the long run.
fireworks_months = fireworks_df.groupby(pd.Grouper(key='created_date', freq='M')).sum().reset_index()

# Rename columns for clarity
fireworks_months.columns = ['Year', 'Number of Reports']

# Convert the Month column to strings to grab every June from the past decade
fireworks_months['Year'] = fireworks_months['Year'].astype(str)
June = fireworks_months[fireworks_months['Year'].str.endswith('06-30')]
June['Year'] = June['Year'].str[:-6]

# Turn each column into a list to plot with matplot
Year = list(June['Year'])
Occurances = list(June['Number of Reports'])


################################################################################

# Plot data

# Create a list of custom strings for x tick labels on axis 0
days = ['June ' + str(day) for day in range(1, 31)]

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Plot data analyzing trend in June 2020
ax.bar(Date, Count)

# Add titles and labels for axis zero
ax.set_title('Illegal Fireworks Reported to 311 (NYC) June 2020', fontsize=16,
              fontweight='bold')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Reports', fontsize=12)

# Assign custom x tick labels
ax.set_xticks(Date)
ax.set_xticklabels(days, rotation='vertical')

# Remove top and right spine
sns.despine()

# Save plot
plt.savefig('Trend in June.png', dpi=600)

###############################################################################

# Create new figure for second graph
fig, ax = plt.subplots(figsize=(10, 5))

# Plot data analyzing total calls in June from 2010 to 2020
ax.bar(Year, Occurances);

# Add titles and labels for axis one
ax.set_title('Illegal Fireworks Reported to 311 June 2010 - June 2020',
              fontsize=16,
              fontweight='bold')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Reports', fontsize=12)

# Remove top and right spine
sns.despine()

# Save plot
plt.savefig('Trend in June Over Past Decade.png', dpi=600)
