import streamlit as st
from utils.funcs import load_repair_data, load_logo

from pathlib import Path
from PIL import Image

load_logo()

repairs_data_df = load_repair_data()

# Set wide layout for the app
st.set_page_config(layout='wide')

# Streamlit App - Main Overview Page
st.markdown(
    """
    <div style="background-color:#f86201;padding:10px;border-radius:5px;text-align:center;color:white;">
    <h1>Exploratory Data Analysis for the Device Repair Orders</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    This app provides an overview of the analysis conducted on the device repair order dataset, focusing on different aspects such as cost, geography, and efficiency. Below are the main steps involved in this Exploratory Data Analysis (EDA):

    ### Steps for Exploratory Data Analysis:

    1. **Data Preprocessing**: Data preprocessing was the initial step, involving cleaning, handling missing values, and formatting data types to ensure the dataset was consistent and ready for analysis.

    ```python
    from geopy.distance import geodesic
    def calculate_distance(row):
        ship_location = (row['ShipLocLat'], row['ShipLocLon'])
        repair_center = repair_centers_df[repair_centers_df['RepairCenter'] == row['RepairPartner']].iloc[0]
        repair_location = (repair_center['RCLocLat'], repair_center['RCLocLon'])
        return geodesic(ship_location, repair_location).km

    def clean_repair_df(repairs_data_df, repair_centers_df=repair_centers_df):
        # Data Cleaning
        repairs_data_df['ShipLocLat'] = repairs_data_df['ShipLocLat'].str.replace(',', '.').astype(float)
        repairs_data_df['ShipLocLon'] = repairs_data_df['ShipLocLon'].str.replace(',', '.').astype(float)
        delivery_cost_df['TransportCostUnitKm'] = delivery_cost_df['TransportCostUnitKm'].str.replace(',', '.').astype(float)

        # Calculate repair time
        repairs_data_df['OrderCreatedDate'] = repairs_data_df['OrderCreatedDate'].astype('str') + ' +02:00' #I assumed OrderCreatedDate is EE time and converted it to UTC timezone
        repairs_data_df['OrderCreatedDate'] = pd.to_datetime(repairs_data_df['OrderCreatedDate'], utc=True)
        repairs_data_df['OrderCompletedDate'] = pd.to_datetime(repairs_data_df['OrderCompletedDate'], utc=True)
        repairs_data_df['RepairTime'] = (repairs_data_df['OrderCompletedDate'] - repairs_data_df['OrderCreatedDate']).dt.total_seconds() / 3600
        repairs_data_df = repairs_data_df.query('RepairTime > 0 ')
        ...
    ```

    2. **Cost Analysis**: The cost analysis provided insights into transportation costs incurred during the repair process. We visualized both the total and average costs for each Transport Partner, allowing us to compare and identify the partners with the highest and lowest costs.

    3. **Geographic Analysis**: The geographic analysis aimed to understand the distribution of repair orders across various regions, helping to identify high-demand areas and optimize the logistics network accordingly.

    4. **Efficiency Analysis**: We evaluated the efficiency of the repair process by analyzing repair times. This involved calculating average repair times and identifying outliers to determine which repair centers were underperforming and where improvements could be made.

    ### Use the Sidebar to Explore Further:
    - Navigate through different pages to explore the specific analyses in more detail, such as cost analysis, geography analysis, and efficiency assessment.
    ### Below is the overall data flow to clean data.
    """
)

# Load the dataset
path = Path(__file__).parent
preprocess_path = path / 'img/Cleaning_Process.png'
image = Image.open(preprocess_path)
image = image.resize((int(1320*0.8), int(930*0.8)))
st.image(image)

