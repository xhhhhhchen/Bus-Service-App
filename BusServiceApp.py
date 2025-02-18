import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import folium_static

# **Set the page layout before any UI elements**
st.set_page_config(
    page_title="Bus Arrival Checker",  # Title for browser tab
    page_icon="🚌",  # Icon for the page
    layout="centered",  
    initial_sidebar_state="expanded"  # Sidebar starts open
)

# **Define dictionary for Translations in the web page**
translations = {
    "en": {
        "title": "Bus Arrival Checker ",
        "select_bus_stop": "Select a Bus Stop:",
        "available_services": "Available Bus Services:",
        "select_service": "Select a Bus Service:",
        "bus_arrival": "Bus Arrival ⏳",
        "mrt_crowd": "🚇 MRT Crowd Level",
        "bus_location": "Bus Locations & Traffic Condition 🗺️",
        "gps_based": "Based on Live GPS 🗺️",
        "schedule_based": "Based on Schedule 📅",
        "warning_no_data": "No data available for the selected bus service.",
        "show_full_schedule": "Show full bus schedule data",
        "single_deck": "Single Deck",
        "double_deck": "Double Deck",
        "bendy_bus": "Bendy",
        "coming_at": "Coming at",
        "mrt_crowd": "🚇 Bedok MRT Crowd Level:",
        "station": "Station",
        "updated": "Updated",
        "low": "Low",
        "moderate": "Moderate",
        "high": "High"
    },

    "zh": {
        "title": "实时公交查询 🚏",
        "select_bus_stop": "选择巴士站:",
        "available_services": "可用巴士服务:",
        "select_service": "选择巴士服务:",
        "bus_arrival": "巴士到达时间 ⏳",
        "mrt_crowd": "🚇 MRT 人流量",
        "bus_location": "巴士位置与交通情况 🗺️",
        "gps_based": "基于实时 GPS 🗺️",
        "schedule_based": "基于时刻表 📅",
        "warning_no_data": "所选巴士服务没有可用数据。",
        "show_full_schedule": "显示完整的巴士时间表",
        "single_deck": "单层巴士",
        "double_deck": "双层巴士",
        "bendy_bus": "铰接巴士",
        "coming_at": "预计到达时间:",
        "title": "实时公交查询",
        "mrt_crowd": "🚇 勿洛地铁人流量:",
        "station": "地铁站",
        "updated": "更新时间",
        "low": "低",
        "moderate": "中等",
        "high": "高"
    },
    "ta": {
        "title": "பஸ் வருகை சோதனை 🚏",
        "select_bus_stop": "பேருந்து நிறுத்தம் தேர்வு:",
        "available_services": "கிடைக்கக்கூடிய பேருந்து சேவைகள்:",
        "select_service": "பேருந்து சேவையைத் தேர்வுசெய்க:",
        "bus_arrival": "பேருந்து வருகை ⏳",
        "mrt_crowd": "🚇 MRT கூட்ட நெரிசல் நிலை",
        "bus_location": "பேருந்து இருப்பிடம் & போக்குவரத்து நிலை 🗺️",
        "gps_based": "நிகழ்நிலை GPS 🗺️",
        "schedule_based": "அட்டவணை 📅",
        "warning_no_data": "தேர்ந்தெடுக்கப்பட்ட பேருந்து சேவைக்கு தரவுகள் இல்லை.",
        "show_full_schedule": "முழு பேருந்து அட்டவணையை காட்டு",
        "single_deck": "ஒற்றை ",
        "double_deck": "இரட்டை ",
        "bendy_bus": "மடங்கு பேருந்து",
        "coming_at": "வருகை:",
        "title": "பஸ் வருகை சோதனை",
        "mrt_crowd": "🚇 MRT கூட்ட நெரிசல் நிலை:",
        "station": "நிலையம்",
        "updated": "புதுப்பிக்கப்பட்டது",
        "low": "குறைவு",
        "moderate": "மிதமான",
        "high": "உயர்"
    },
    "ms": {
        "title": "Pemeriksa Ketibaan Bas 🚏",
        "select_bus_stop": "Pilih Hentian Bas:",
        "available_services": "Perkhidmatan Bas Tersedia:",
        "select_service": "Pilih Perkhidmatan Bas:",
        "bus_arrival": "Ketibaan Bas ⏳",
        "mrt_crowd": "🚇 Tahap Kepadatan MRT",
        "bus_location": "Lokasi Bas & Keadaan Trafik 🗺️",
        "gps_based": "Berdasarkan GPS Langsung 🗺️",
        "schedule_based": "Berdasarkan Jadual 📅",
        "warning_no_data": "Tiada data tersedia untuk perkhidmatan bas yang dipilih.",
        "show_full_schedule": "Tunjukkan jadual bas penuh",
        "single_deck": "Bas Dek Tunggal",
        "double_deck": "Bas Dua Tingkat",
        "bendy_bus": "Bas Panjang",
        "coming_at": "Tiba:",
        "title": "Pemeriksa Ketibaan Bas",
        "mrt_crowd": "🚇 Tahap Kepadatan MRT:",
        "station": "Stesen",
        "updated": "Dikemas kini",
        "low": "Rendah",
        "moderate": "Sederhana",
        "high": "Tinggi"
    }
}

#----------------- Creating buttons for language selection -------------------#

# **Initialize session state for language selection**
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"  # Default language

# **Define language options**
languages = {
    "English": "en",
    "中文 (Chinese)": "zh",
    "தமிழ் (Tamil)": "ta",
    "Bahasa Melayu (Malay)": "ms"
}

# **Create equal-sized columns for evenly spaced buttons**
cols = st.columns(len(languages))  # Creates 4 equally spaced columns

# **Language selection buttons**
for idx, (lang, code) in enumerate(languages.items()):
    with cols[idx]:  # Assign each button to a separate column
        if st.button(lang):
            st.session_state.selected_language = lang

# **Retrieve selected language code**
selected_language = st.session_state.selected_language
lang_key = languages[selected_language]  # Get language code (en, zh, ta, ms)


#----------------- start of the page -------------------#

# **Header**
st.markdown(f"## {translations[lang_key]['title']}")

# Load the bus arrival data from bus service
def load_data():
     return pd.read_excel("C:/Users/xhhhh/AAAAAAAA schoool/A NP DDP/data/Bus_Services.xlsx")

# Load the data
BusService = load_data()


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

#----------------- for user to select bus stop and busses -------------------#
with col1:
    # Dropdown for selecting Bus Stop Code with Name
    bus_stop_options = BusService[['BusStopCode', 'BusStopDisplay']].drop_duplicates()

    st.markdown( f"""
    <h5 style='white-space: nowrap; margin-bottom: -100px;'>
        {translations[lang_key]['select_bus_stop']}
    </h5>
    """, unsafe_allow_html=True)

    selected_display = st.selectbox('', bus_stop_options['BusStopDisplay'])  

    # Extract the selected Bus Stop Code from the selected display
    selected_stop = bus_stop_options.loc[
        bus_stop_options['BusStopDisplay'] == selected_display, 'BusStopCode'
    ].values[0]

    # Filter data based on selected bus stop
    filtered_data = BusService[BusService['BusStopCode'] == selected_stop]

    # Show available bus services for the selected bus stop
    bus_services = filtered_data['ServiceNo'].unique()

    st.markdown( f"""
        <h5 style='white-space: nowrap; margin-bottom: -100px;'>
            {translations[lang_key]['available_services']}
        </h5>
        """, unsafe_allow_html=True)
    # Display the select box with the new font size
    selected_service = st.selectbox("", bus_services)  # the font size here cannot be adjusted....


    # Display bus arrival time and  details 
    bus_info = filtered_data[filtered_data['ServiceNo'] == selected_service]

#----------------- To display MRT condition -------------------#

with col2:
    def load_mrt_data():
            return pd.read_excel("C:/Users/xhhhh/AAAAAAAA schoool/A NP DDP/data/MRT crowd density.xlsx")

    # Load the data
    MRT_CrowdLevel = load_mrt_data()

    # Extract information 
    crowd_level = MRT_CrowdLevel.loc[0, 'CrowdLevel']
    station_code = MRT_CrowdLevel.loc[0, 'Station']
    last_updated = MRT_CrowdLevel.loc[0, 'Last Updated'].strftime('%d %B %Y, %I:%M %p')

    # Define crowd level color coding
    crowd_color_map = {
        "Low": "green",
        "Moderate": "orange",
        "High": "red"
    }

    # Get translated crowd level
    crowd_level_translated = translations[lang_key].get(crowd_level.lower(), crowd_level)

    # Get translated labels
    station_label = translations[lang_key]["station"]
    updated_label = translations[lang_key]["updated"]

    # Get appropriate color for crowd level
    color = crowd_color_map.get(crowd_level, "black")

    # Display the MRT crowd level box
    st.markdown(f"<h5 style='white-space: nowrap;'>{translations[lang_key]['mrt_crowd']}</h5>", unsafe_allow_html=True)

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
                {crowd_level_translated}
            </span>
            <br>
            <span style="font-size: 20px; color: gray;">{station_label}: {station_code}</span>
            <br>
            <span style="font-size: 18px; color: gray;">{updated_label}: {last_updated}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# Check if bus_info is not empty
if not bus_info.empty:

    # Create layout with two columns
    col3, col4 = st.columns([1, 1])  # 1:1 ratio to balance bus info and map


#----------------- To display Bus Arrival timings and relevant information about the busses -------------------#
    with col3:

        st.markdown(f"### {translations[lang_key]['bus_arrival']}")

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
        display_columns = ['TimeToArrive', 'BusSequence', 'EstArrival', 'Load', 'Type', 'Feature','Monitored'] 

        #Get the translations based on the selected laguage for bus types 
        translated_bus_type = {
            "Single Deck": translations[lang_key]["single_deck"],
            "Double Deck": translations[lang_key]["double_deck"],
            "Bendy": translations[lang_key]["bendy_bus"]
        }

        translated_coming_at = translations[lang_key]["coming_at"]


        
        # Iterate through bus_info and display formatted data
        for index, row in bus_info.iterrows():
            arrival_time = row['TimeToArrive']
            formatted_time = row['EstArrival'].strftime('%I:%M %p')
            crowd_level = row['Load']
            bus_type_code = row['Type']  
            wheelchair_access = row['Feature']

            # Translate bus type based on code
            bus_type_translated = translated_bus_type.get(bus_type_code, "Unknown Bus Type")

            # Determine if GPS or schedule-based estimation
            Message = translations[lang_key]["gps_based"] if row['Monitored'] else translations[lang_key]["schedule_based"]

            # Determine color based on crowd level
            color = crowd_color_map.get(crowd_level, 'black')
            wheelchair_symbol = wheelchair_symbol_map.get(wheelchair_access, '')

            # Display bus arrival time with color coding and additional info
            st.markdown(
                f"""
                <div style="border: 6px solid #ddd; 
                            padding: 13px; 
                            border-radius: 10px; 
                            margin-top: 1px;
                            margin-bottom: 10px;
                            width: 300px;  
                            height: 150px; ">
                        <span style="font-size: 36px; font-weight: bold; color: {color};">{arrival_time}{wheelchair_symbol}</span>
                        <span style="font-size: 18px; color: gray; margin-top: -5px; margin-bottom: 0px; display: block;">
                            {bus_type_translated}, {translated_coming_at} {formatted_time}
                        </span>
                        <span style="font-size: 18px; color: gray; margin-bottom: px;  display: block;">{Message}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

#----------------- To Display a map and show Bus Locations, bus stop location and location of incidents -------------------#
    with col4:
         # Display the translated bus location header with consistent formatting
        st.markdown(
            f"""
            <h3 style="white-space: nowrap;">{translations[lang_key]['bus_location']}</h3>
            """,
            unsafe_allow_html=True
        )

        
        # Extract bus location data from the dataframe
        bus_locations = bus_info[['Latitude', 'Longitude', 'ServiceNo', 'BusSequence','TimeToArrive','BusStop_Latitude', 'BusStop_Longitude']].dropna().to_dict(orient='records')


        # Check if there are bus locations available
        if bus_locations:
            first_bus_lat = bus_locations[0]['Latitude']
            first_bus_lon = bus_locations[0]['Longitude']
            first_bus_lat, first_bus_lon = bus_locations[0]['BusStop_Latitude'], bus_locations[0]['BusStop_Longitude']
                    # Create map centered on the first bus's location
            m = folium.Map(location=[first_bus_lat, first_bus_lon], zoom_start=13)

        else:
        # Default to a generic location (Singapore) if no data is available
            m = folium.Map(location=[1.3521, 103.8198], zoom_start=13)
            
    

    # Add bus location markers
        # Add bus location markers
        for bus in bus_locations:
            bus_info_popup = f"Bus {bus['ServiceNo']} - Arrival: {bus['TimeToArrive']}"

            # Get crowd level and corresponding color
            crowd_level = bus.get('Load', 'Seats Available')  # Default to 'Seats Available' if missing
            bus_color = crowd_color_map.get(crowd_level, 'yellow')  # Default to yellow if not found

            # Create a custom emoji icon using HTML with dynamic background color
            folium.Marker(
                location=[bus['Latitude'], bus['Longitude']],
                popup=folium.Popup(bus_info_popup, parse_html=True),
                icon=folium.DivIcon(
                    html=f"""
                        <div style="
                            font-size: 28px;
                            color: white;
                            text-align: center;
                            line-height: 0.8;
                            background-color: {bus_color};  /* Dynamically set background color */
                            padding: 10px; 
                            display: inline-block;
                            border-radius: 50px;  /* Optional rounded corners */
                            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);  /* Optional shadow for effect */
                        ">🚌</div>
                    """
                )
            ).add_to(m)
                
            
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

         # Extract bus stop location data
        bus_stops = bus_info[['BusStop_Latitude', 'BusStop_Longitude', 'BusStopCode']].dropna().to_dict(orient='records')


        # Add bus stop location markers
        for stop in bus_stops:
            bus_stop_popup = f"Bus Stop Code: {stop['BusStopCode']}"

            folium.Marker(
                location=[stop['BusStop_Latitude'], stop['BusStop_Longitude']],
                popup=folium.Popup(bus_stop_popup, parse_html=True),
                icon=folium.DivIcon(
                    html=f"""
                        <div style="
                            font-size: 20px;
                            color: white;
                            text-align: center;
                            line-height: 1;
                            background-color: lightblue;  
                            padding: 8px; 
                            display: inline-block;
                            border-radius: 50px;  
                            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);  
                        ">🚏</div>
                    """
                )
            ).add_to(m)


        # Render the map in Streamlit
        folium_static(m)


    # # --------------------- SECOND MAP: BUS STOP LOCATIONS --------------------- (this is not included in the interface as it took too long to load)

    # st.markdown("### Bus Stop Locations 🏁")

    # # Extract bus stop location data
    # bus_stops = BusService[['BusStop_Latitude', 'BusStop_Longitude', 'BusStopCode']].dropna().to_dict(orient='records')

    # # Check if there are bus stops available
  

    # # Create a separate map centered on the first bus stop
    # bus_stop_map = folium.Map(location=[1.3521, 103.8198])

    # # Add bus stop location markers
    # for stop in bus_stops:
    #     bus_stop_popup = f"Bus Stop Code: {stop['BusStopCode']}"

    #     folium.Marker(
    #         location=[stop['BusStop_Latitude'], stop['BusStop_Longitude']],
    #         popup=folium.Popup(bus_stop_popup, parse_html=True),
    #         icon=folium.DivIcon(
    #             html=f"""
    #                 <div style="
    #                     font-size: 20px;
    #                     color: white;
    #                     text-align: center;
    #                     line-height: 1;
                      
    #                 ">🚏</div>
    #             """
    #         )
    #     ).add_to(bus_stop_map)

    # # Render the second map in Streamlit
    # folium_static(bus_stop_map)

else:
    st.warning(translations[lang_key]["warning_no_data"])
    
if st.checkbox(translations[lang_key]["show_full_schedule"]):
    st.dataframe(BusService)
