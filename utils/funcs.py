
import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.distance import geodesic
from pathlib import Path
from PIL import Image


# Load the dataset
path = Path(__file__).parent.parent
delivery_cost_path = path / 'data/DeliveryCost.csv'
repair_centers_path = path / 'data/RepairCenters.csv'
repairs_data_path = path / 'data/Repairs-Data.csv'
repairs_cleaned_path = path / 'data/repairs_data_cleaned.csv'


def load_data(path,delimiter,dates_cols=None):
    return pd.read_csv(path,sep=delimiter,parse_dates=dates_cols)

delivery_cost_df = load_data(delivery_cost_path, delimiter=';')
repair_centers_df = load_data(repair_centers_path, delimiter=';')


# Calculate distances between shipping locations and repair centers
def calculate_distance(row):
    ship_location = (row['ShipLocLat'], row['ShipLocLon'])
    repair_center = repair_centers_df[repair_centers_df['RepairCenter'] == row['RepairPartner']].iloc[0]
    repair_location = (repair_center['RCLocLat'], repair_center['RCLocLon'])
    return geodesic(ship_location, repair_location).km

def clean_centers_df(repair_centers_df):
    repair_centers_df['RCLocLat'] = repair_centers_df['RCLocLat'].astype(float)
    repair_centers_df['RCLocLon'] = repair_centers_df['RCLocLon'].astype(float)
    return repair_centers_df

def clean_repair_df(repairs_data_df,repair_centers_df=repair_centers_df):
    # Data Cleaning
    repairs_data_df['ShipLocLat'] = repairs_data_df['ShipLocLat'].str.replace(',', '.').astype(float)
    repairs_data_df['ShipLocLon'] = repairs_data_df['ShipLocLon'].str.replace(',', '.').astype(float)
    delivery_cost_df['TransportCostUnitKm'] = delivery_cost_df['TransportCostUnitKm'].str.replace(',', '.').astype(float)

    # Calculate repair time
    repairs_data_df['OrderCreatedDate'] = repairs_data_df['OrderCreatedDate'].astype('str') + ' +02:00' #I assumed OrderCreatedDate is EE time and converted it to UTC timezone
    repairs_data_df['OrderCreatedDate'] = pd.to_datetime(repairs_data_df['OrderCreatedDate'],  utc=True)
    repairs_data_df['OrderCompletedDate'] = pd.to_datetime(repairs_data_df['OrderCompletedDate'], utc=True)
    repairs_data_df['RepairTime'] = (repairs_data_df['OrderCompletedDate'] - repairs_data_df['OrderCreatedDate']).dt.total_seconds() / 3600
    repairs_data_df = repairs_data_df.query('RepairTime > 0 ')

    repairs_data_df.dropna(subset='ShipLocLat',axis=0,inplace=True) # remove null values
    # calc distance
    repairs_data_df['DistanceToRepairCenter'] = repairs_data_df.apply(calculate_distance, axis=1)
    repair_centers_df = clean_centers_df(repair_centers_df)
    #get cost per km
    repairs_data_df = repairs_data_df.merge(delivery_cost_df,on=['TransportPartner','ProductCategory'],how='inner')
    repairs_data_df['TransportCost'] = repairs_data_df['DistanceToRepairCenter'] * repairs_data_df['TransportCostUnitKm']
    repairs_data_df.to_csv(path /'data/repairs_data_cleaned.csv',index=False)
    return repairs_data_df

def load_repair_data(path_raw_data=repairs_data_path, path_clean_data=repairs_cleaned_path):
    # Check if cleaned file exists
    if path_clean_data.is_file():
        repairs_data_df = load_data(path_clean_data, delimiter=',', dates_cols=['OrderCreatedDate', 'OrderCompletedDate'])
    else:
        repairs_data_df = pd.read_csv(path_raw_data, sep=',')
        clean_repair_df(repairs_data_df)
        if path_clean_data.is_file():
            repairs_data_df = load_data(path_clean_data, delimiter=',', dates_cols=['OrderCreatedDate', 'OrderCompletedDate'])
        else:
            raise FileNotFoundError("Cleaned file was not created properly")

    return repairs_data_df

def load_logo():
    # Load the dataset
    path = Path(__file__).parent.parent
    logo_path = path / 'img/logo.png'
    image = Image.open(logo_path)

    st.logo(image, size="large", link=None, icon_image=None)
    return None


