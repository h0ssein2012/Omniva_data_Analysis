import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.funcs import load_repair_data, load_logo

# Load the logo and data
load_logo()
repairs_data_df = load_repair_data()

# Set wide layout for the app
st.set_page_config(layout="wide")

# Streamlit App
st.markdown(
    """
    <div style="background-color:#f86201;padding:10px;border-radius:5px;text-align:center;color:white;">
    <h1>Cost Analysis</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Calculate total transport cost by Transport Partner
total_transport_cost = repairs_data_df.groupby('TransportPartner')['TransportCost'].sum().reset_index()
avg_transport_cost = repairs_data_df.groupby('TransportPartner')['TransportCost'].mean().round(1).reset_index()

# Create dual-axis bar chart for total transport cost and average transport cost
fig_transport_cost = go.Figure()
fig_transport_cost.add_trace(go.Bar(
    x=total_transport_cost['TransportPartner'],
    y=total_transport_cost['TransportCost'],
    name='Total Transport Cost',
    marker=dict(color='#f86201')
))

fig_transport_cost.add_trace(go.Scatter(
    x=avg_transport_cost['TransportPartner'],
    y=avg_transport_cost['TransportCost'],
    name='Average Transport Cost',
    yaxis='y2',
    mode='markers+text',
    text='Avg Cost: ' + avg_transport_cost['TransportCost'].astype(str),
    textposition='top center',
    marker=dict(size=10, color='black'),
    textfont=dict(color='black')
))

# Update layout for dual y-axis
fig_transport_cost.update_layout(
    title={
        'text': 'Total and Average Transport Cost by Transport Partner',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.9,
        'yanchor': 'top',
        'font': {
            'size': 24
        }
    },
    xaxis_title='Transport Partner',
    yaxis=dict(
        title='Total Transport Cost',
        side='left'
    ),
    yaxis2=dict(
        title='Average Transport Cost',
        overlaying='y',
        side='right'
    ),
    legend=dict(
        x=0.01,
        y=0.99
    )
)

st.plotly_chart(fig_transport_cost)

# Number of orders per Transport Partner
orders_per_partner = repairs_data_df['TransportPartner'].value_counts().reset_index()
orders_per_partner.columns = ['TransportPartner', 'OrderCount']
fig_orders_per_partner = px.bar(orders_per_partner, x='TransportPartner', y='OrderCount', title='Number of Orders per Transport Partner', color_discrete_sequence=['#f86201'])
fig_orders_per_partner.update_layout(
    title={
        'text': 'Number of Orders per Transport Partner',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.9,
        'yanchor': 'top',
        'font': {
            'size': 24
        }
    },
    xaxis_title='Transport Partner',
    yaxis_title='Number of Orders'
)
st.plotly_chart(fig_orders_per_partner)

# Cost analysis over time (Weekly) for each Transport Partner
weekly_transport_cost = repairs_data_df.groupby(['TransportPartner', pd.Grouper(key='OrderCreatedDate', freq='W')])['TransportCost'].sum().reset_index()
weekly_transport_cost.rename(columns={'OrderCreatedDate':'YearWeek'}, inplace=True)
fig_weekly_cost = px.area(
    weekly_transport_cost,
    x='YearWeek',
    y='TransportCost',
    color='TransportPartner',
    title='Weekly Transport Cost by Transport Partner',
    hover_name='TransportPartner'
)
fig_weekly_cost.update_layout(
    title={
        'text': 'Weekly Transport Cost by Transport Partner',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.9,
        'yanchor': 'top',
        'font': {
            'size': 24
        }
    },
    xaxis_title='Year-Week',
    yaxis_title='Total Transport Cost',
    margin=dict(l=0, r=0, t=50, b=0),
    template='plotly_white',
    title_font_size=20,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True),
    legend_title='Transport Partner'
)
st.plotly_chart(fig_weekly_cost)

# Orders analysis over time (Weekly) for each Transport Partner
weekly_order_count = repairs_data_df.groupby(['TransportPartner', pd.Grouper(key='OrderCreatedDate', freq='W')])['Retailer'].count().reset_index()
weekly_order_count.rename(columns={'OrderCreatedDate':'YearWeek', 'Retailer': 'OrderCount'}, inplace=True)
fig_weekly_orders = px.area(
    weekly_order_count,
    x='YearWeek',
    y='OrderCount',
    color='TransportPartner',
    title='Weekly Orders by Transport Partner',
    hover_name='TransportPartner'
)
fig_weekly_orders.update_layout(
    title={
        'text': 'Weekly Orders by Transport Partner',
        'x': 0.5,
        'xanchor': 'center',
        'y': 0.9,
        'yanchor': 'top',
        'font': {
            'size': 24
        }
    },
    xaxis_title='Year-Week',
    yaxis_title='Total Orders',
    margin=dict(l=0, r=0, t=50, b=0),
    template='plotly_white',
    title_font_size=20,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True),
    legend_title='Transport Partner'
)
st.plotly_chart(fig_weekly_orders)
