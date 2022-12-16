import pandas as pd
import numpy as np
import os
import requests
import datetime
import json
import re
import time 

def get_json(url):
    response = requests.get(url)
    j = json.loads(response.text)
    
    return j

def get_code(target_value, url):
    code = ''
    j = get_json(url)
    
    for entry in j['Data']:
        if entry['value_represented'] == target_value:
            code = entry['code']
            
    return code

def get_state_code(state_name):
    url = 'https://aqs.epa.gov/data/api/list/states?email=test@aqs.api&key=test'
    state_code = get_code(state_name, url)

    return state_code

def get_county_code(state_code, county_name):
    url = f'https://aqs.epa.gov/data/api/list/countiesByState?email=test@aqs.api&key=test&state={state_code}'
    county_code = get_code(county_name, url)
    
    return county_code

'''def get_county_code_list(county_names):
    county_codes = []
    for county in county_names:
        county_codes.append()'''

def get_county_code_list(state_code):
    url = f'https://aqs.epa.gov/data/api/list/countiesByState?email=test@aqs.api&key=test&state={state_code}'

    j = get_json(url)
    county_codes = []
    
    for county in j['Data']:
        if re.fullmatch('Bronx|Kings|New York|Queens|Richmond', county['value_represented']):
            county_codes.append(county['code'])  
    
    return county_codes


#start_date = str(traffic_vol_daily['date'].min()).replace('-', '')
#end_date = str(traffic_vol_daily['date'].max()).replace('-', '')
#start_date = '20160101'
#end_date = '20160229'
#county_code = '005'

def get_daily_air_quality_list(state_code, county_codes):
    email = 'daguila000@citymail.cuny.edu'
    key = 'cobaltcrane81'
    param_code = '88101'
    daily_air_quality_list = []

    #year_counter = traffic_vol_daily['date'].min().year
    #end_year = traffic_vol_daily['date'].max().year
    year_counter = 2009
    end_year = 2020

    while year_counter <= end_year:
        for county_code in county_codes: 
            start_date = str(year_counter) + '0101'
            end_date = str(year_counter) + '1231'
            url = f'https://aqs.epa.gov/data/api/dailyData/byCounty?email={email}&key={key}&param={param_code}&bdate={start_date}&edate={end_date}&state={state_code}&county={county_code}'
            j = get_json(url)
            print(j['Header'])
            daily_air_quality_list.extend(j['Data'])
            time.sleep(6)
        year_counter += 1
        
    return daily_air_quality_list

def create_air_quality_csv():
    state_code = get_state_code(state)
    county_code_list = get_county_code_list(state_code)
    daily_air_quality_list = get_daily_air_quality_list(county_code_list)
    daily_air_quality_df = pd.DataFrame(daily_air_quality_list)
    daily_air_quality_df.to_csv('datasets/daily_air_quality.csv')


def download_data(csv_name):
    """Download data from link matching key in dictionary and save in datasets folder

    Args:
        csv_name (str): The name of the csv.
    """
    url_dict = {'air_quality': 'https://data.cityofnewyork.us/api/views/c3uy-2p5r/rows.csv', 
                'mobility_global': 'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv', 
                'traffic_volume': 'https://data.cityofnewyork.us/api/views/7ym2-wayt/rows.csv'}
    
    response = requests.get(url_dict[csv_name])
    path = f'datasets/{csv_name}.csv'
    with open(path, 'wb') as f:
        f.write(response.content)
        
        
def csv_exists(csv_name):
    """Check if the csv exists.

    Args:
        csv_name (str): The string of the name of the csv file.

    Returns:
        bool
    """
    path = f'datasets/{csv_name}.csv'
    file_exists = os.path.exists(path)
    return file_exists


def create_df(csv_name):
    """Create a dataframe from a csv from a preset path.

    Args:
        csv_name (str): The string of the name of the csv file.

    Returns:
        df
    """
    if not csv_exists(csv_name):
        download_data(csv_name)
    path = f'datasets/{csv_name}.csv'
    df = pd.read_csv(path)
    return df


def mkdir_if_not_exist():
    """
    Create dataset directory if it does not exist.
    """
    directory = 'datasets'
    if not os.path.exists(f'{directory}/'):
        os.mkdir(directory)

        
def create_all_df(csv_names):
    """Create a list of DataFrames from an input list of csv file names.

    Args:
        csv_names (list): List of strings of csv file names.

    Returns:
        list: DataFrames
    """
    mkdir_if_not_exist()
    df_list = []
    
    for csv_name in csv_names:
        print(f'Creating {csv_name} df')
        df = create_df(csv_name)
        df_list.append(df)
        
    return df_list


def clean_air_quality(air_quality_df):
    air_quality_df = air_quality_df.drop(['Message'], axis=1)
    air_quality_df = air_quality_df.drop(['Unique ID'], axis=1)
    air_quality_df = air_quality_df.drop(['Geo Join ID'], axis=1)
    air_quality_df['Start_Date'] = pd.to_datetime(air_quality_df['Start_Date'], infer_datetime_format=True)

    return air_quality_df


def clean_mobility(mobility_df):
    mobility_nyc = mobility_df[mobility_df['country_region_code'].eq('US') & 
                               mobility_df['sub_region_1'].eq('New York') & 
                               mobility_df['sub_region_2'].str.contains('Bronx|Kings|New York|Queens|Richmond')]

    mobility_nyc = mobility_nyc.drop(['metro_area', 'iso_3166_2_code'], axis=1)
    mobility_nyc = mobility_nyc.drop(['country_region_code', 'country_region', 'sub_region_1'], axis=1)
    mobility_nyc = mobility_nyc.drop(['census_fips_code', 'place_id'], axis=1)

    return mobility_nyc


def clean_traffic_volume(traffic_volume_df):
    traffic_volume_df = traffic_volume_df[traffic_volume_df['Yr'] > 2008]
    traffic_volume_df['date_time'] = pd.to_datetime(dict(year=traffic_volume_df.Yr, 
                                                    month=traffic_volume_df.M, 
                                                    day=traffic_volume_df.D, 
                                                    hour=traffic_volume_df.HH, 
                                                    minute=traffic_volume_df.MM))
    traffic_volume_df = traffic_volume_df.drop(['Yr', 'M', 'D', 'HH', 'MM'], axis=1)

    return traffic_volume_df


def main():
    csv_names = ['air_quality', 'mobility_global', 'traffic_volume']

    air_quality, mobility_global, traffic_volume = create_all_df(csv_names)

    air_quality_cleaned = clean_air_quality(air_quality)
    mobility_nyc = clean_mobility(mobility_global)
    traffic_volume_cleaned = clean_traffic_volume(traffic_volume)

    print(air_quality_cleaned.sample(10))
    print(mobility_nyc.sample(10))
    print(traffic_volume_cleaned.sample(10))

main()
