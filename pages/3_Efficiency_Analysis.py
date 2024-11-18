import streamlit as st
import pandas as pd
import plotly.express as px
from utils.funcs import load_repair_data,load_logo

load_logo()
repairs_data_df = load_repair_data()

# Convert RepairTime from hours to days
repairs_data_df['RepairTimeDays'] = repairs_data_df['RepairTime'] / 24

# Streamlit App
st.markdown(
    """
    <div style="background-color:#f86201;padding:10px;border-radius:5px;text-align:center;color:white;">
    <h1>Repair Process Efficiency Analysis</h1>
    </div>
        <br>

    """,
    unsafe_allow_html=True
)
# Forecast Return Demand Based on Repair Times
st.header("Demand Forecasting for Return Shipments")

# Aggregate the number of return shipments by month
forecasted_return_demand = repairs_data_df.groupby([pd.Grouper(key='OrderCompletedDate', freq='M')])['Retailer'].size().reset_index()
forecasted_return_demand.columns = ['Month', 'ReturnShipmentCount']
forecasted_return_demand = forecasted_return_demand.sort_values(by='Month',)

# Plot the forecasted return shipments
fig_forecasted_return = px.line(
    forecasted_return_demand,
    x='Month',
    y='ReturnShipmentCount',
    title='Forecasted Return Shipments Over Time',
    labels={'Month': 'Month', 'ReturnShipmentCount': 'Number of Return Shipments'},
    markers=True,
    text="ReturnShipmentCount",
    color_discrete_sequence=['#f86201']
)
fig_forecasted_return.update_traces(textposition="top left", textfont=dict(color="black"))
fig_forecasted_return.update_layout(
    xaxis_title='Month',
    yaxis_title='Number of Return Shipments',
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(fig_forecasted_return)

# Visualize repair time distribution
st.header("Distribution of Repair Times")
fig_repair_time_dist = px.histogram(
    repairs_data_df,
    x='RepairTimeDays',
    nbins=50,
    title='Distribution of Repair Times (in days)',
    labels={'RepairTimeDays': 'Repair Time (days)'},
    color_discrete_sequence=['#f86201']
)
fig_repair_time_dist.update_layout(
    xaxis_title='Repair Time (days)',
    yaxis_title='Number of Repairs',
    margin=dict(l=0, r=0, t=50, b=0)
)
st.plotly_chart(fig_repair_time_dist)


# Average repair time by Repair Partner
st.header("Average Repair Time by Repair Partner")
avg_repair_time = repairs_data_df.groupby('RepairPartner')['RepairTimeDays'].mean().round(1).reset_index()
avg_repair_time.sort_values(by='RepairTimeDays',ascending=False,inplace=True)
fig_avg_repair_time = px.bar(
    avg_repair_time,
    x='RepairPartner',
    y='RepairTimeDays',
    text='RepairTimeDays',
    title='Average Repair Time by Repair Partner',
    labels={'RepairPartner': 'Repair Partner', 'RepairTimeDays': 'Average Repair Time (days)'},
    color_discrete_sequence=['#f86201']
)
fig_avg_repair_time.update_layout(
    xaxis_title='Repair Partner',
    yaxis_title='Average Repair Time (hours)',
    margin=dict(l=0, r=0, t=50, b=0)
)
fig_avg_repair_time.update_traces(textposition="inside", textfont=dict(color="white",size=14))


st.plotly_chart(fig_avg_repair_time)
