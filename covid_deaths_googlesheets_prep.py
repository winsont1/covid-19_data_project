import pandas as pd
import numpy as np
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# 1. Download a timeseries of daily deaths per country

def donwload_csv(url):
  # Download raw csv file and save to Pandas dataframe
  deaths_df = pd.read_csv(url, error_bad_lines=False)

  # Write daily deaths dataframe to CSV file (for reference)
  deaths_df.to_csv('time_series_covid19_deaths_global.csv', index = False, header=True)
  return deaths_df


# 2. Convert the table so that each country and each day is a separate row

def convert_table(deaths_df):
  # Aggregate deaths by country
  grouped_deaths_df = deaths_df.groupby('Country/Region').sum()
  # Drop 'Lat' and 'Long' columns
  grouped_deaths_df = grouped_deaths_df.drop(["Lat", "Long"], axis=1)

  # Reset index
  grouped_deaths_df = grouped_deaths_df.reset_index()

  # Convert data from wide form to long form
  date_headers = list(grouped_deaths_df.columns[1:].values)
  long_df = pd.melt(grouped_deaths_df, id_vars= ['Country/Region'], value_vars= date_headers)

  # Rename Columns
  long_df = long_df.rename(columns={"Country/Region": "country", "variable": "date", "value": "total_deaths"}, errors="raise")

  # Change date column type
  long_df['date'] = pd.to_datetime(long_df['date'])
  return long_df


# 3. Upload the table from step 2 into an SQL table named deaths_total

def upload_deaths_total_to_sql(deaths_long_df, engine):
  deaths_long_df.to_sql('deaths_total', con = engine, if_exists = 'replace', index = False)


# 4. Calculate the daily change in deaths for each country

def calculate_deaths_change(deaths_long_df):
  # Add deaths_change column to dataframe in Step 2
  deaths_long_df.insert(3, 'deaths_change',0)

  # Get list of unique country names
  countries = list(deaths_long_df['country'].unique())

  # Calculate deaths_change for each country in 'countries' list

  for country in countries:
      # Set temporary df for country
      temp_df = deaths_long_df.loc[deaths_long_df['country'] == country]

      # Find difference between rows (returns difference results dataframe)
      diff = temp_df['total_deaths'].diff()

      # Apply difference calculation to original deaths_long_df according to index
      deaths_long_df.iloc[diff.index,3] = diff

  # Remove NaN values from dataframe
  deaths_long_df = deaths_long_df.fillna(0)

  # Select relevant columns
  deaths_change_df = deaths_long_df[['country','date','deaths_change']]

  return deaths_change_df


# 5. Upload the table from step 4 into an SQL table named deaths_change_python
def upload_deaths_change_to_sql(deaths_change_df, engine):
  deaths_change_df.to_sql('deaths_change_python', con = engine, if_exists = 'replace', index = False)


def main():
  if __name__=="__main__":
    daily_deaths_csv_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'

    deaths_df = donwload_csv(daily_deaths_csv_url) #1
    deaths_long_df = convert_table(deaths_df) #2

    # Connect to PostgreSQL database (change accordingly)
    engine = create_engine('postgresql://postgres:password@localhost:5432/covid-19')

    upload_deaths_total_to_sql(deaths_long_df, engine) #3
    deaths_change_df = calculate_deaths_change(deaths_long_df) #4
    upload_deaths_change_to_sql(deaths_change_df, engine) #5

main()
