import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import re

# Set page configuration
st.set_page_config(
    page_title="US Import and Tariff Visualization",
    page_icon="🌎",
    layout="wide"
)

# Title and description
st.title("The Impact of Liberation Day Tariff Rates on Geopolitical Swing States")

# Load the data
@st.cache_data
def load_data():
    # Load the US import data
    df = pd.read_csv('US_2024_Import_Data.csv')
    
    # Clean up the tariff rate column (remove % sign and convert to float)
    df['Tariff Rate'] = df['Tariff Rate'].apply(lambda x: float(re.sub(r'%', '', str(x))))
    
    # Convert import values to numeric if they're not already
    df['Imports ($B)'] = pd.to_numeric(df['Imports ($B)'], errors='coerce')

    
    return df

df = load_data()

# Expanded country coordinates (approximate centers)
country_coords = {
    'Afghanistan': (33.9391, 67.7100),
    'Albania': (41.1533, 20.1683),
    'Algeria': (28.0339, 1.6596),
    'Andorra': (42.5063, 1.5218),
    'Angola': (-11.2027, 17.8739),
    'Anguilla': (18.2206, -63.0686),
    'Antigua and Barbuda': (17.0608, -61.7964),
    'Argentina': (-38.4161, -63.6167),
    'Armenia': (40.0691, 45.0382),
    'Aruba': (12.5211, -69.9683),
    'Australia': (-25.2744, 133.7751),
    'Austria': (47.5162, 14.5501),
    'Azerbaijan': (40.1431, 47.5769),
    'Bahamas': (25.0343, -77.3963),
    'Bahrain': (26.0667, 50.5577),
    'Bangladesh': (23.6850, 90.3563),
    'Barbados': (13.1939, -59.5432),
    'Belarus': (53.7098, 27.9534),
    'Belgium': (50.5039, 4.4699),
    'Belize': (17.1899, -88.4976),
    'Benin': (9.3077, 2.3158),
    'Bermuda': (32.3078, -64.7505),
    'Bhutan': (27.5142, 90.4336),
    'Bolivia': (-16.2902, -63.5887),
    'Bosnia and Herzegovina': (43.9159, 17.6791),
    'Botswana': (-22.3285, 24.6849),
    'Brazil': (-14.2350, -51.9253),
    'British Indian Ocean Terr.': (-7.3346, 72.4242),
    'British Virgin Islands': (18.4207, -64.6400),
    'Brunei': (4.5353, 114.7277),
    'Bulgaria': (42.7339, 25.4858),
    'Burkina Faso': (12.2383, -1.5616),
    'Burundi': (-3.3731, 29.9189),
    'Cabo Verde': (16.5388, -23.0418),
    'Cambodia': (12.5657, 104.9910),
    'Cameroon': (7.3697, 12.3547),
    'Canada': (56.1304, -106.3468),
    'Cayman Islands': (19.5134, -80.5669),
    'Central African Republic': (6.6111, 20.9394),
    'Chad': (15.4542, 18.7322),
    'Chile': (-35.6751, -71.5430),
    'China': (35.8617, 104.1954),
    'Christmas Island': (-10.4475, 105.6904),
    'Cocos (Keeling) Islands': (-12.1642, 96.8710),
    'Colombia': (4.5709, -74.2973),
    'Comoros': (-11.6455, 43.3333),
    'Congo (Brazzaville)': (-0.2280, 15.8277),
    'Cook Islands': (-21.2367, -159.7777),
    'Costa Rica': (9.7489, -83.7534),
    'Cote d\'Ivoire': (7.5400, -5.5471),
    'Croatia': (45.1000, 15.2000),
    'Cuba': (21.5218, -77.7812),
    'Curacao': (12.1696, -68.9900),
    'Cyprus': (35.1264, 33.4299),
    'Czech Republic': (49.8175, 15.4730),
    'Democratic Republic of Congo': (-4.0383, 21.7587),
    'Denmark': (56.2639, 9.5018),
    'Djibouti': (11.8251, 42.5903),
    'Dominica': (15.4150, -61.3710),
    'Dominican Republic': (18.7357, -70.1627),
    'East Timor': (-8.8742, 125.7275),
    'Ecuador': (-1.8312, -78.1834),
    'Egypt': (26.8206, 30.8025),
    'El Salvador': (13.7942, -88.8965),
    'Equatorial Guinea': (1.6508, 10.2679),
    'Eritrea': (15.1794, 39.7823),
    'Estonia': (58.5953, 25.0136),
    'Eswatini': (-26.5225, 31.4659),
    'Ethiopia': (9.1450, 40.4897),
    'Falkland Islands': (-51.7963, -59.5236),
    'Faroe Islands': (61.8926, -6.9118),
    'Fiji': (-17.7134, 178.0650),
    'Finland': (61.9241, 25.7482),
    'France': (46.2276, 2.2137),
    'French Guiana': (3.9339, -53.1258),
    'French Polynesia': (-17.6797, -149.4068),
    'French Southern and Antarctic': (-49.2804, 69.3486),
    'Gabon': (-0.8037, 11.6094),
    'Gambia': (13.4432, -15.3101),
    'Gaza Strip admin. by Israel': (31.3547, 34.3088),
    'Georgia': (42.3154, 43.3569),
    'Germany': (51.1657, 10.4515),
    'Ghana': (7.9465, -1.0232),
    'Gibraltar': (36.1408, -5.3536),
    'Greece': (39.0742, 21.8243),
    'Greenland': (71.7069, -42.6043),
    'Grenada': (12.1165, -61.6790),
    'Guadeloupe': (16.2650, -61.5510),
    'Guatemala': (15.7835, -90.2308),
    'Guinea': (9.9456, -9.6966),
    'Guinea-Bissau': (11.8037, -15.1804),
    'Guyana': (4.8604, -58.9302),
    'Haiti': (18.9712, -72.2852),
    'Heard and McDonald Islands': (-53.0818, 73.5042),
    'Honduras': (15.2000, -86.2419),
    'Hong Kong': (22.3193, 114.1694),
    'Hungary': (47.1625, 19.5033),
    'Iceland': (64.9631, -19.0208),
    'India': (20.5937, 78.9629),
    'Indonesia': (-0.7893, 113.9213),
    'Iran': (32.4279, 53.6880),
    'Iraq': (33.2232, 43.6793),
    'Ireland': (53.1424, -7.6921),
    'Israel': (31.0461, 34.8516),
    'Italy': (41.8719, 12.5674),
    'Jamaica': (18.1096, -77.2975),
    'Japan': (36.2048, 138.2529),
    'Jordan': (30.5852, 36.2384),
    'Kazakhstan': (48.0196, 66.9237),
    'Kenya': (-0.0236, 37.9062),
    'Kiribati': (1.8708, -157.3630),
    'Kosovo': (42.5633, 20.9030),
    'Kuwait': (29.3117, 47.4818),
    'Kyrgyzstan': (41.2044, 74.7661),
    'Laos': (19.8563, 102.4955),
    'Latvia': (56.8796, 24.6032),
    'Lebanon': (33.8547, 35.8623),
    'Lesotho': (-29.6100, 28.2336),
    'Liberia': (6.4281, -9.4295),
    'Libya': (26.3351, 17.2283),
    'Liechtenstein': (47.1660, 9.5554),
    'Lithuania': (55.1694, 23.8813),
    'Luxembourg': (49.8153, 6.1296),
    'Macau': (22.1987, 113.5439),
    'Madagascar': (-18.7669, 46.8691),
    'Malawi': (-13.2543, 34.3015),
    'Malaysia': (4.2105, 101.9758),
    'Maldives': (3.2028, 73.2207),
    'Mali': (17.5707, -3.9962),
    'Malta': (35.9375, 14.3754),
    'Marshall Islands': (7.1315, 171.1845),
    'Martinique': (14.6415, -61.0242),
    'Mauritania': (21.0079, -10.9408),
    'Mauritius': (-20.3484, 57.5522),
    'Mayotte': (-12.8275, 45.1662),
    'Mexico': (23.6345, -102.5528),
    'Micronesia': (7.4256, 150.5508),
    'Moldova': (47.4116, 28.3699),
    'Monaco': (43.7384, 7.4246),
    'Mongolia': (46.8625, 103.8467),
    'Montenegro': (42.7087, 19.3744),
    'Montserrat': (16.7425, -62.1874),
    'Morocco': (31.7917, -7.0926),
    'Mozambique': (-18.6657, 35.5296),
    'Myanmar (Burma)': (21.9162, 95.9560),
    'Namibia': (-22.9576, 18.4904),
    'Nauru': (-0.5228, 166.9315),
    'Nepal': (28.3949, 84.1240),
    'Netherlands': (52.1326, 5.2913),
    'New Caledonia': (-20.9043, 165.6180),
    'New Zealand': (-40.9006, 174.8860),
    'Nicaragua': (12.8654, -85.2072),
    'Niger': (17.6078, 8.0817),
    'Nigeria': (9.0820, 8.6753),
    'Niue': (-19.0544, -169.8672),
    'Norfolk Island': (-29.0408, 167.9547),
    'North Korea': (40.3399, 127.5101),
    'North Macedonia': (41.6086, 21.7453),
    'Norway': (60.4720, 8.4689),
    'Oman': (21.4735, 55.9754),
    'Pakistan': (30.3753, 69.3451),
    'Palau': (7.5150, 134.5825),
    'Panama': (8.5380, -80.7821),
    'Papua New Guinea': (-6.3150, 143.9555),
    'Paraguay': (-23.4425, -58.4438),
    'Peru': (-9.1900, -75.0152),
    'Philippines': (12.8797, 121.7740),
    'Pitcairn Islands': (-24.3768, -128.3242),
    'Poland': (51.9194, 19.1451),
    'Portugal': (39.3999, -8.2245),
    'Qatar': (25.3548, 51.1839),
    'Republic of Yemen': (15.5527, 48.5164),
    'Reunion': (-21.1151, 55.5364),
    'Romania': (45.9432, 24.9668),
    'Russia': (61.5240, 105.3188),
    'Rwanda': (-1.9403, 29.8739),
    'Samoa': (-13.7590, -172.1046),
    'San Marino': (43.9424, 12.4578),
    'Sao Tome and Principe': (0.1864, 6.6131),
    'Saudi Arabia': (23.8859, 45.0792),
    'Senegal': (14.4974, -14.4524),
    'Serbia': (44.0165, 21.0059),
    'Seychelles': (-4.6796, 55.4920),
    'Sierra Leone': (8.4606, -11.7799),
    'Singapore': (1.3521, 103.8198),
    'Sint Maarten': (18.0425, -63.0548),
    'Slovakia': (48.6690, 19.6990),
    'Slovenia': (46.1512, 14.9955),
    'Solomon Islands': (-9.6457, 160.1562),
    'Somalia': (5.1521, 46.1996),
    'South Africa': (-30.5595, 22.9375),
    'South Korea': (35.9078, 127.7669),
    'South Sudan': (6.8770, 31.3070),
    'Spain': (40.4637, -3.7492),
    'Sri Lanka': (7.8731, 80.7718),
    'St Helena': (-15.9650, -5.7089),
    'St Kitts and Nevis': (17.3578, -62.7830),
    'St Lucia': (13.9094, -60.9789),
    'St Pierre and Miquelon': (46.8852, -56.3159),
    'St Vincent and the Grenadines': (13.2528, -61.1971),
    'Sudan': (12.8628, 30.2176),
    'Suriname': (3.9193, -56.0278),
    'Svalbard, Jan Mayen Island': (77.8750, 20.9752),
    'Sweden': (60.1282, 18.6435),
    'Switzerland': (46.8182, 8.2275),
    'Syria': (34.8021, 38.9968),
    'Taiwan': (23.6978, 120.9605),
    'Tajikistan': (38.8610, 71.2761),
    'Tanzania': (-6.3690, 34.8888),
    'Thailand': (15.8700, 100.9925),
    'Togo': (8.6195, 0.8248),
    'Tokelau': (-9.2002, -171.8484),
    'Tonga': (-21.1790, -175.1982),
    'Trinidad and Tobago': (10.6918, -61.2225),
    'Tunisia': (33.8869, 9.5375),
    'Turkey': (38.9637, 35.2433),
    'Turkmenistan': (38.9697, 59.5563),
    'Turks and Caicos Islands': (21.6940, -71.7979),
    'Tuvalu': (-7.1095, 177.6493),
    'UAE': (23.4241, 53.8478),
    'Uganda': (1.3733, 32.2903),
    'Ukraine': (48.3794, 31.1656),
    'United Arab Emirates': (23.4241, 53.8478),
    'United Kingdom': (55.3781, -3.4360),
    'United States': (37.0902, -95.7129),
    'Uruguay': (-32.5228, -55.7658),
    'Uzbekistan': (41.3775, 64.5853),
    'Vanuatu': (-15.3767, 166.9592),
    'Vatican City': (41.9029, 12.4534),
    'Venezuela': (6.4238, -66.5897),
    'Vietnam': (14.0583, 108.2772),
    'Wallis and Futuna': (-13.7687, -177.1561),
    'West Bank admin. by Israel': (31.9522, 35.2332),
    'Zambia': (-13.1339, 27.8493),
    'Zimbabwe': (-19.0154, 29.1549)
}

# Function to create the bubble map visualization
def create_bubble_map(data, min_imports, max_imports, min_tariff, max_tariff, selected_countries, highlight_swing_states=False):
    # Filter data based on selections
    filtered_df = data.copy()
    
    # Filter by import value range
    filtered_df = filtered_df[
        (filtered_df['Imports ($B)'] >= min_imports) &
        (filtered_df['Imports ($B)'] <= max_imports) &
        (filtered_df['Tariff Rate'] >= min_tariff) &
        (filtered_df['Tariff Rate'] <= max_tariff)
    ]
    
    # Filter by countries if any are selected
    if selected_countries:
        filtered_df = filtered_df[filtered_df['CTYNAME'].isin(selected_countries)]
    
    # Create figure
    fig = go.Figure()
    
    # Prepare data for regular bubbles and star-shaped bubbles (geopolitical swing states)
    regular_lons, regular_lats, regular_sizes, regular_tariff_rates = [], [], [], []
    regular_hover_texts, regular_country_names = [], []
    
    swing_lons, swing_lats, swing_sizes, swing_tariff_rates = [], [], [], []
    swing_hover_texts, swing_country_names = [], []
    
    # Process each country
    for _, row in filtered_df.iterrows():
        country_name = row['CTYNAME']
        imports = row['Imports ($B)']
        tariff_rate = row['Tariff Rate']
        # Handle the case where Geopolitical_swing_state could be a boolean or string
        swing_state_value = row['Geopolitical_swing_state']
        if isinstance(swing_state_value, bool):
            is_swing_state = swing_state_value
        else:
            # If it's a string, convert to lowercase and check if it's 'true'
            is_swing_state = str(swing_state_value).lower() == 'true'
        
        # Skip if we don't have coordinates for this country
        if country_name not in country_coords:
            # Try to find a close match
            for coord_country in country_coords.keys():
                if country_name in coord_country or coord_country in country_name:
                    country_name = coord_country
                    break
            else:
                continue  # Skip if no match found
        
        lat, lon = country_coords[country_name]
        
        # Calculate bubble size based on import value (logarithmic scale for better visualization)
        # Handle very small values
        if imports < 1:
            bubble_size = 5
        elif imports <10:
            bubble_size = 10
        elif imports < 100:
            bubble_size = 20
        else:
            # Use log scale for better visualization of wide range of values
            bubble_size = 5 + 8 * np.log2(imports)
        
        hover_text = (
            f"Country: {country_name}<br>" +
            f"Imports: ${imports:,.2f} Billion<br>" +
            f"Tariff Rate: {tariff_rate}%<br>" +
            f"Geopolitical Swing State: {'Yes' if is_swing_state else 'No'}"
        )
        
        # Add data to appropriate arrays based on swing state status
        if is_swing_state:
            swing_lons.append(lon)
            swing_lats.append(lat)
            swing_sizes.append(bubble_size)
            swing_tariff_rates.append(tariff_rate)
            swing_country_names.append(country_name)
            swing_hover_texts.append(hover_text)
        else:
            regular_lons.append(lon)
            regular_lats.append(lat)
            regular_sizes.append(bubble_size)
            regular_tariff_rates.append(tariff_rate)
            regular_country_names.append(country_name)
            regular_hover_texts.append(hover_text)
    
    # Prepare country codes for choropleth
    # Get ISO3 codes for swing states (excluding China and USA which have special colors)
    swing_country_iso3 = []
    for country in swing_country_names:
        if country == 'China' or country == 'United States':
            continue
        
        # Map country names to ISO3 codes (simplified mapping for demonstration)
        # In a real application, you would use a more comprehensive mapping
        iso3 = None
        if country == 'Vietnam': iso3 = 'VNM'
        elif country == 'Bangladesh': iso3 = 'BGD'
        elif country == 'India': iso3 = 'IND'
        elif country == 'Indonesia': iso3 = 'IDN'
        elif country == 'Singapore': iso3 = 'SGP'
        elif country == 'Sweden': iso3 = 'SWE'
        elif country == 'France': iso3 = 'FRA'
        elif country == 'Germany': iso3 = 'DEU'
        elif country == 'Netherlands': iso3 = 'NLD'
        elif country == 'Norway': iso3 = 'NOR'
        elif country == 'Kuwait': iso3 = 'KWT'
        elif country == 'Qatar': iso3 = 'QAT'
        elif country == 'Saudi Arabia': iso3 = 'SAU'
        elif country == 'United Arab Emirates': iso3 = 'ARE'
        elif country == 'Australia': iso3 = 'AUS'
        elif country == 'Japan': iso3 = 'JPN'
        elif country == 'South Korea': iso3 = 'KOR'
        elif country == 'Taiwan': iso3 = 'TWN'
        elif country == 'Mexico': iso3 = 'MEX'
        elif country == 'Brazil': iso3 = 'BRA'
        elif country == 'Chile': iso3 = 'CHL'
        elif country == 'Morocco': iso3 = 'MAR'
        
        if iso3:
            swing_country_iso3.append(iso3)
    
    # Add special choropleth for China (red), United States (blue), and swing states (purple)
    fig.add_trace(go.Choropleth(
        locations=['CHN', 'USA'] + swing_country_iso3,
        z=[1, 2] + [3] * len(swing_country_iso3),  # Different values for different colors
        text=['China', 'United States'] + swing_country_names,
        colorscale=[
            [0, 'rgb(220,20,60)'],    # Red for China (z=1)
            [0.5, 'rgb(30,144,255)'], # Blue for USA (z=2)
            [1, 'rgb(128,0,128)']     # Purple for swing states (z=3)
        ],
        showscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add regular bubbles (invisible if highlight_swing_states is enabled)
    if not highlight_swing_states or len(regular_lons) > 0:  # Only add if not highlighting or if there are regular countries
        fig.add_trace(go.Scattergeo(
            lon=regular_lons,
            lat=regular_lats,
            mode='markers',
            marker=dict(
                size=regular_sizes,
                color=regular_tariff_rates,  # Always use tariff rates for color
                colorscale='Hot_r',  # Always use the reversed "Hot" colorscale
                cmin=min_tariff,
                cmax=50,
                showscale=False,  # Don't show colorscale for regular bubbles
                opacity=0 if highlight_swing_states else 0.7,  # Make invisible if highlighting swing states
                line=dict(width=1, color='black')
            ),
            text=regular_country_names,
            hoverinfo='text' if not highlight_swing_states else 'none',  # Disable hover info when invisible
            hovertext=regular_hover_texts if not highlight_swing_states else None,
            name='Regular Countries',
            visible=True  # Keep trace in the figure even when invisible
        ))
    
    # Add markers for geopolitical swing states (using hot colorscale like regular bubbles)
    fig.add_trace(go.Scattergeo(
        lon=swing_lons,
        lat=swing_lats,
        mode='markers',
        marker=dict(
            size=swing_sizes,
            color=swing_tariff_rates,  # Use tariff rates for color mapping
            colorscale='Hot_r',  # Use the reversed "Hot" colorscale
            cmin=min_tariff,
            cmax=50,
            showscale=False,  # Don't show a second colorscale
            opacity=0.7,
            line=dict(width=1, color='black')
        ),
        text=swing_country_names,
        hoverinfo='text',
        hovertext=swing_hover_texts,
        name='Geopolitical Swing States'
    ))
    
    # Add a standalone colorscale that's always visible
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(
            colorscale='Hot_r',
            showscale=True,
            cmin=min_tariff,
            cmax=50,
            colorbar=dict(
                title="Tariff Rate (%)",
                thickness=15,
                len=0.5,
                y=0.5
            )
        ),
        hoverinfo='none',
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text="US Imports and Tariff Rates by Country",
            font=dict(size=24)
        ),
        showlegend=False,
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            showocean=True,
            oceancolor='rgb(158, 202, 225)',
            showlakes=True,
            lakecolor='rgb(158, 202, 225)',
            showrivers=True,
            rivercolor='rgb(158, 202, 225)',
            showcountries=True,
            showcoastlines=True,
            coastlinecolor='rgb(80, 80, 80)',
            coastlinewidth=0.5
        ),
        height=700,
        margin=dict(l=0, r=0, t=50, b=0),
        # Hide axes and gridlines
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(visible=False, showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
    )
    
    return fig


# Sidebar filters
st.sidebar.header("Filters")

# Country filter
all_countries = sorted(df['CTYNAME'].unique())
selected_countries = st.sidebar.multiselect(
    "Countries",
    options=all_countries,
    default=[]
)

# Geopolitical swing state filter
highlight_swing_states = st.sidebar.checkbox("Highlight Geopolitical Swing States", value=False)

# Import value range filter
min_imports = float(df['Imports ($B)'].min())
max_imports = float(df['Imports ($B)'].max())
import_range = st.sidebar.slider(
    "Import Value Range (Billion USD)",
    min_value=min_imports,
    max_value=max_imports,
    value=(min_imports, max_imports),
    format="$%.2f"
)

# Tariff rate range filter
min_tariff = float(df['Tariff Rate'].min())
max_tariff = float(df['Tariff Rate'].max())
tariff_range = st.sidebar.slider(
    "Tariff Rate Range (%)",
    min_value=min_tariff,
    max_value=max_tariff,
    value=(min_tariff, max_tariff),
    format="%.1f%%"
)

# Create and display the map
with st.spinner("Generating map... This may take a moment."):
    map_fig = create_bubble_map(df, import_range[0], import_range[1], tariff_range[0], tariff_range[1], selected_countries, highlight_swing_states)
    st.plotly_chart(map_fig, use_container_width=True)

st.markdown("""
This interactive map visualizes US import data (2024) and tariff rates from the Liberation Day announcement for countries around the world:
- **Bubble size**: Represents the total imports into the US from each country  (larger bubble = higher import value)
- **Bubble color**: Represents the proposed tariff rate
- **Country shading**: 
  - China is shaded red
  - United States is shaded blue
  - Geopolitical swing states are shaded purple
            
Use the filters in the sidebar to explore different aspects of the US import data:
- Filter by specific countries
- Filter by import value range
- Filter by tariff rate range
- **Highlight Geopolitical Swing States**: When checked, this makes geopolitical swing states stand out by hiding non-swing states

Hover over bubbles to see detailed information about each country, including the exact import value (in billions of USD), tariff rate, and geopolitical swing state status.
""")

# Display data table
st.subheader("US Import Data")
st.dataframe(df, use_container_width=True)
