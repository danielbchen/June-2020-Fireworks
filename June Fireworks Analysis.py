# Import packages for data analysis and visualization

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sodapy import Socrata

# Load 311 NYC fireworks complaing data. Publicly available at:
# https://data.cityofnewyork.us/Social-Services/311-Fireworks-Complaints/g4u2-tvag

# Use unathenticated client with publicly avaibale data set
# Return entire data set
client = Socrata('data.cityofnewyork.us', None)
results = client.get_all('g4u2-tvag')

# Convert data to pandas DataFrame
fireworks_df = pd.DataFrame.from_records(results)

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
fireworks = fireworks_grouped[(fireworks_grouped['Incident Date'] >= '2020-06-01') & (fireworks_grouped['Incident Date'] < '2020-06-23')]

# Drop the timestape from the 'Incident Date' column
pd.options.mode.chained_assignment = None
fireworks['Incident Date'] = pd.to_datetime(fireworks['Incident Date']).dt.date

# Convert the columns to a list object in order to graph
Date = list(fireworks['Incident Date'])
Count = list(fireworks['Number of Reports'])

# Set figure dimensions and create graph
plt.figure(figsize=(10,7))
plt.plot(Date, Count, color='red', alpha=0.6, linewidth=2)

# Add title and axis labels
plt.title('Illegal Fireworks Reported to 311 in June 2020', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Reports', fontsize=12)

# Formatting changes below
plt.margins(x=0, y=0) # Removes extra white space between spines and graph
sns.despine() # Removes the top and right spine

# Show and save plot
plt.savefig('Fireworks Graph.png')
plt.show()


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

# Create plot
plt.figure(figsize=(10,7))
plt.bar(Year, Occurances, color='darkblue')

# Add title and axis labels
plt.title('Illegal Fireworks Reported to 311 in June (2010 - 2020)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Reports', fontsize=12)

# Formatting changes below
sns.despine() # Removes the top and right spine

# Show and save plot
plt.savefig('Fireworks in June by Month.png')
plt.show()
