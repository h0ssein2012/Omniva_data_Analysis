import streamlit as st
import pandas as pd
import plotly.express as px
from utils.funcs import load_repair_data,load_logo

load_logo()

repairs_data_df = load_repair_data()

# Streamlit App
st.markdown(
    """
    <div style="background-color:#f86201;padding:10px;border-radius:5px;text-align:center;color:white;">
    <h1>Geographic Analysis for Shipping Locations</h1>
    </div>
        <br>
    """,
    unsafe_allow_html=True
)

# Aggregate data to count the number of shipments per country
shipments_per_country = repairs_data_df['ShipLocCy'].value_counts().reset_index()
shipments_per_country.columns = ['Country', 'ShipmentCount']

# Convert 2-letter country codes to 3-letter ISO codes
country_code_mapping = {
    'SE': 'SWE',
    'NO': 'NOR',
    'FI': 'FIN',
    'EE': 'EST',
    'DK': 'DNK'
}
shipments_per_country['Country'] = shipments_per_country['Country'].map(country_code_mapping)

# Map country codes back to latitude and longitude (hardcoded for the demo)
country_coordinates = {
    'SWE': {'lat': 60.1282, 'lon': 18.6435},
    'NOR': {'lat': 60.4720, 'lon': 8.4689},
    'FIN': {'lat': 61.9241, 'lon': 25.7482},
    'EST': {'lat': 58.5953, 'lon': 25.0136},
    'DNK': {'lat': 56.2639, 'lon': 9.5018}
}

shipments_per_country['Latitude'] = shipments_per_country['Country'].map(lambda x: country_coordinates[x]['lat'])
shipments_per_country['Longitude'] = shipments_per_country['Country'].map(lambda x: country_coordinates[x]['lon'])

# Plot the distribution using Scatter Mapbox
fig_shipments_mapbox = px.scatter_mapbox(
    shipments_per_country,
    lat='Latitude',
    lon='Longitude',
    size='ShipmentCount',
    color='ShipmentCount',
    hover_name='Country',
    color_continuous_scale=[[0, "#d3d3d3"], [1, "#f86201"]],
    size_max=30,
    zoom=3
)

fig_shipments_mapbox.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    title={
        'text': 'Distribution of Shipping Locations by Country',
        'x': 0.5,
        'xanchor': 'center',
        'y': .99,
        'yanchor': 'top',
        'font': {
            'size': 24
        }
    },
)

st.plotly_chart(fig_shipments_mapbox)

st.header("Transportation Demand per region")

# Display countries with the highest number of shipments
fig = px.bar(shipments_per_country, x='Country'
             , y='ShipmentCount', title='Number of Orders per country'
             ,text='ShipmentCount'
             , color_discrete_sequence=['#f86201'])
fig.update_layout(xaxis_title='Country', yaxis_title='Number of Orders')
fig.update_traces(textposition="inside", textfont=dict(color="white",size=14))

st.plotly_chart(fig)
