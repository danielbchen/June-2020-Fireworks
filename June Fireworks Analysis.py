# Import packages for data analysis and visualization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sodapy import Socrata

# Load 311 NYC fireworks complaing data. Publicly available at:
# https://data.cityofnewyork.us/Social-Services/311-Fireworks-Complaints/g4u2-tvag

# Use unathenticated client with publicly avaibale data set
# Return entire data set
client = Socrata('data.cityofnewyork.us', None)
results = client.get_all('g4u2-tvag')

    df = pd.DataFrame.from_records(results)
    
    df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce')
    df['fireworks'] = [1 if complaint == 'Illegal Fireworks' else 0 for complaint in fireworks_df['complaint_type']]

    return df 


# Convert 'created_date' column to datetime object to plot
fireworks_df['created_date'] = pd.to_datetime(fireworks_df['created_date'], errors='coerce')

# Create a new dummy column. If 'complaint_type' equals illegal fireworks
# then the column will contain a 1. Otherwise, it will be zero.
fireworks_df['fireworks'] = [1 if complaint == 'Illegal Fireworks' else 0 for
complaint in fireworks_df['complaint_type']]

# Group incidents by date of occurance.
fireworks_grouped = fireworks_df.groupby(pd.Grouper(key='created_date', freq='D')).sum().reset_index()

# Renme columns for clarity
fireworks_grouped.columns = ['Incident Date', 'Number of Reports']

# Select the incidents from the beginning of June to the most recent data
fireworks = fireworks_grouped[(fireworks_grouped['Incident Date'] >= '2020-06-01') & (fireworks_grouped['Incident Date'] < '2020-07-01')]

# Drop the timestape from the 'Incident Date' column
pd.options.mode.chained_assignment = None
fireworks['Incident Date'] = pd.to_datetime(fireworks['Incident Date']).dt.date

# Convert the columns to a list object in order to graph
Date = list(fireworks['Incident Date'])
Count = list(fireworks['Number of Reports'])

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
