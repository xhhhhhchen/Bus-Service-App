import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import folium_static

# Load the bus arrival data from 
@st.cache_data
def load_data():
     return pd.read_excel("C:/Users/xhhhh/AAAAAAAA schoool/A NP DDP/data/Bus_Services.xlsx")

# Load the data
BusService = load_data()


# Header 
st.markdown("## 🚌 Bus Arrival Checker")

# Create a new column to combine Bus Stop Code and Name
BusService['BusStopDisplay'] = BusService['BusStopCode'].astype(str) + " - " + BusService['BusStop_Description']


# To adjust the length of the drop down selection box 
st.markdown(
    """
    <style>
    div[data-baseweb="select"] {
        width: 400px !important;  /* Adjust width as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Layout with two columns for bus stop dropdown and MRT condition
col1, col2 = st.columns([2, 1]) 

# for user to select bus stop and busses
with col1:
    # Dropdown for selecting Bus Stop Code with Name
    bus_stop_options = BusService[['BusStopCode', 'BusStopDisplay']].drop_duplicates()
    selected_display = st.selectbox("Select a Bus Stop:", bus_stop_options['BusStopDisplay'])

    # Extract the selected Bus Stop Code from the selected display
    selected_stop = bus_stop_options.loc[
        bus_stop_options['BusStopDisplay'] == selected_display, 'BusStopCode'
    ].values[0]

    # Filter data based on selected bus stop
    filtered_data = BusService[BusService['BusStopCode'] == selected_stop]

    # Show available bus services for the selected bus stop
    st.markdown("#### Available Bus Services")
    bus_services = filtered_data['ServiceNo'].unique()
    selected_service = st.selectbox("Select a Bus Service:", bus_services)

    # Display bus arrival time and  details 
    bus_info = filtered_data[filtered_data['ServiceNo'] == selected_service]

# To display MRT condition
with col2:
    def load_mrt_data():
            return pd.read_excel("C:/Users/xhhhh/AAAAAAAA schoool/A NP DDP/data/MRT crowd density.xlsx")

    # Load the data
    MRT_CrowdLevel = load_mrt_data()

    # Extract information from the first row (assuming one row for demo)
    crowd_level = MRT_CrowdLevel.loc[0, 'CrowdLevel']
    station_code = MRT_CrowdLevel.loc[0, 'Station']
    last_updated = MRT_CrowdLevel.loc[0, 'Last Updated'].strftime('%d %B %Y, %I:%M %p')

    # Define crowd level color coding
    crowd_color_map = {
        'Low': 'green',
        'Moderate': 'orange',
        'High': 'red'
    }

    # Get appropriate color for crowd level
    color = crowd_color_map.get(crowd_level, 'black')

    # Display the MRT crowd level box
    st.markdown(
        '<h4 style="white-space: nowrap;">🚇 Bedok MRT Crowd Level</h4>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            border: 1px solid #ddd; 
            padding: 15px; 
            border-radius: 10px; 
            background-color: #f9f9f9; 
            width: 250px;
            height: 180px;
            text-align: center;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        ">
            <span style="font-size: 36px; font-weight: bold; color: {color};">
                {crowd_level}
            </span>
            <br>
            <span style="font-size: 20px; color: gray;">Station: {station_code}</span>
            <br>
            <span style="font-size: 18px; color: gray;">Updated: {last_updated}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# Check if bus_info is not empty
if not bus_info.empty:

    # Create layout with two columns
    col3, col4 = st.columns([1, 2])  # 1:2 ratio to balance bus info and map

    with col3:

        st.markdown("#### Bus Arrival⏳")

        # Define crowd level color coding and wheelchair accessibility symbol
        crowd_color_map = {
            'Seats Available': 'green',  # Seating Available
            'Standing Available': 'orange',  # Standing Available
            'Limited Standing': 'red'      # Limited Standing
        }

        wheelchair_symbol_map = {
            'Wheelchair Accessible': '♿',  # Accessible
            '': ''    # Not accessible
        }

        # Select required columns to display
        display_columns = ['TimeToArrive', 'BusSequence', 'EstArrival', 'Load', 'Type', 'Feature']

        for index, row in bus_info[display_columns].iterrows():
            arrival_time = row['TimeToArrive']
            formatted_time = row['EstArrival'].strftime('%I:%M %p')
            crowd_level = row['Load']
            bus_type = row['Type']
            wheelchair_access = row['Feature']

            # Determine color based on crowd level
            color = crowd_color_map.get(crowd_level, 'black')
            wheelchair_symbol = wheelchair_symbol_map.get(wheelchair_access, '')

            # Display bus arrival time with color coding and additional info
            st.markdown(
                f"""
                <div style="border: 6px solid #ddd; 
                            padding: 13px; 
                            border-radius: 10px; 
                            margin-bottom: 10px;
                            width: 200px;  
                            height: 150px; ">
                    <span style="font-size: 36px; font-weight: bold; color: {color};">{arrival_time} </span>
                    <br>
                    <span style="font-size: 18px; color: gray;">{bus_type}{wheelchair_symbol}</span>
                    <br>
                    <span style="font-size: 18px; color: gray;">Arrival: {formatted_time}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col4:
        st.markdown("#### Bus Locations & Traffic Condition 🗺️")

        # Extract bus location data from the dataframe
        bus_locations = bus_info[['Latitude', 'Longitude', 'ServiceNo', 'BusSequence']].dropna().to_dict(orient='records')


        # Check if there are bus locations available
        if bus_locations:
            first_bus_lat = bus_locations[0]['Latitude']
            first_bus_lon = bus_locations[0]['Longitude']
        else:
        # Default to a generic location (Singapore) if no data is available
            first_bus_lat, first_bus_lon = 1.3521, 103.8198

        # Create map centered on the first bus's location
        m = folium.Map(location=[first_bus_lat, first_bus_lon], zoom_start=13)

    # Add bus location markers
        for bus in bus_locations:
            bus_info_popup = f"Bus {bus['ServiceNo']} - Sequence: {bus['BusSequence']}"

            # Create a custom emoji icon using HTML
            folium.Marker(
                location=[bus['Latitude'], bus['Longitude']],
                popup=folium.Popup(bus_info_popup, parse_html=True),
                icon=folium.DivIcon(
                    html=f"""
                        <div style="
                            font-size: 28px;
                            color: blue;
                            text-align: center;
                            line-height: 0.8;
                            background-color: yellow;  /* White background for visibility */
                            padding: 10px; 
                            display: inline-block;
                            border-radius: 100px;  /* Optional rounded corners */
                            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);  /* Optional shadow for effect */
                        ">🚌</div>
                    """
                )
            ).add_to(m)

        

        # Adding bus location data
            
        def load_traffic_data():
            return pd.read_excel("C:/Users/xhhhh/AAAAAAAA schoool/A NP DDP/data/Traffic_Incidents.xlsx")

        # Load the data
        TIncident = load_traffic_data()

        # Convert DataFrame to a dictionary list
        incident_locations = TIncident.apply(lambda row: {
            "lat": row['Latitude'],
            "lon": row['Longitude'],
            "type": row ['Type'],
            "desc": f"{row['Type']} on {row['DateTime']}"
        }, axis=1).tolist()

        # Define icons for each incident type
        incident_icon_map = {
            "Accident": "🚑",
            "Roadwork": "🚧",
            "Vehicle Breakdown": "🚗",
            "Weather": "🌧️",
            "Obstacle": "🛑",
            "Road Block": "🛑",
            "Heavy Traffic": "🚦",
            "Misc.": "⚠️",
            "Diversion": "⚠️",
            "Unattended Vehicle": "🚗"
        }

    # Add traffic incident markers with customized icons and red border
        for incident in incident_locations:
            incident_type = incident['type']
            incident_icon = incident_icon_map.get(incident_type, "⚠️")  # Default warning icon if type is not found

            folium.Marker(
                location=[incident['lat'], incident['lon']],
                popup=incident['desc'],
                icon=folium.DivIcon(
                    html=f"""
                        <div style="
                        font-size: 28px;
                        color: black;
                        text-align: center;
                        line-height: 1;
                        background-color: white;  /* White background for visibility */
                        padding: 10px; 
                        display: inline-block;
                        border-radius: 100px;  /* Optional rounded corners */
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);  /* Optional shadow for effect */
                    ">{incident_icon}</div>
                    """
                )
            ).add_to(m)

        # Render the map in Streamlit
        folium_static(m)


else:
    st.warning("No data available for the selected bus service.")

# Show the entire data table (optional)
if st.checkbox("Show full bus schedule data"):
    st.dataframe(BusService)