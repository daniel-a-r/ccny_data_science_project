import pandas as pd
import numpy as np
import os
import requests

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
