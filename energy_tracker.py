import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configure page
st.set_page_config(
    page_title="🏡 Smart Energy Tracker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .appliance-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 3px solid #4CAF50;
    }
    
    .energy-tip {
        background: linear-gradient(45deg, #FFA726, #FF7043);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .consumption-high { color: #FF5722; font-weight: bold; }
    .consumption-medium { color: #FF9800; font-weight: bold; }
    .consumption-low { color: #4CAF50; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'daily_consumption' not in st.session_state:
    st.session_state.daily_consumption = []
if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False

# Data persistence functions
@st.cache_data
def load_data():
    """Load existing data from CSV"""
    try:
        if os.path.exists('energy_consumption_data.csv'):
            return pd.read_csv('energy_consumption_data.csv')
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

def save_data(data):
    """Save data to CSV"""
    try:
        df = pd.DataFrame(data)
        df.to_csv('energy_consumption_data.csv', index=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

# Helper functions
def calculate_base_consumption(home_type):
    """Calculate base consumption based on home type"""
    consumption_map = {
        "1BHK": 3,
        "2BHK": 4,
        "3BHK": 5,
        "4BHK": 6,
        "Villa": 8
    }
    return consumption_map.get(home_type, 4)

def get_appliance_consumption(appliance):
    """Get consumption units for different appliances"""
    appliance_map = {
        "AC": 3,
        "Fridge": 2,
        "Washing Machine": 4,
        "Dishwasher": 3,
        "Water Heater": 5,
        "Electric Stove": 4
    }
    return appliance_map.get(appliance, 1)

def get_consumption_category(units):
    """Categorize consumption levels"""
    if units <= 5:
        return "Low", "consumption-low"
    elif units <= 10:
        return "Medium", "consumption-medium"
    else:
        return "High", "consumption-high"

# Main App Header
st.markdown("""
<div class="main-header">
    <h1>🏡 Smart Home Energy Consumption Tracker</h1>
    <p>Monitor, Analyze & Optimize Your Energy Usage</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.markdown("## 🧭 Navigation")
page = st.sidebar.radio("Choose a section:", 
                       ["🏠 Home Setup", "📊 Daily Tracking", "📈 Analytics", "💡 Energy Tips"])

# HOME SETUP PAGE
if page == "🏠 Home Setup":
    st.markdown("## 🏠 Home & User Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Personal Details")
        name = st.text_input("📝 Full Name", placeholder="Enter your full name")
        city = st.text_input("🏙️ City", placeholder="Enter your city")
        area = st.text_input("📍 Area/Locality", placeholder="Enter your area")
        people = st.number_input("👥 Number of People", min_value=1, max_value=20, value=2)
    
    with col2:
        st.markdown("### 🏡 Home Details")
        home_type = st.selectbox("🏠 Property Type", 
                                ["Flat", "Tenement", "Independent House", "Villa"])
        home_facility = st.selectbox("🛏️ Home Size", 
                                   ["1BHK", "2BHK", "3BHK", "4BHK", "Villa"])
        
        st.markdown("### ⚡ Available Appliances")
        appliances = st.multiselect("Select your appliances:", 
                                  ["AC", "Fridge", "Washing Machine", "Dishwasher", 
                                   "Water Heater", "Electric Stove"])
    
    if st.button("💾 Save Setup", type="primary"):
        if name and city and area:
            st.session_state.user_data = {
                'name': name,
                'city': city,
                'area': area,
                'people': people,
                'home_type': home_type,
                'home_facility': home_facility,
                'appliances': appliances,
                'setup_date': datetime.now().strftime('%Y-%m-%d')
            }
            st.session_state.setup_complete = True
            st.success("✅ Setup completed successfully!")
            st.rerun()
        else:
            st.error("❌ Please fill in all required fields")
    
    if st.session_state.setup_complete:
        st.markdown("---")
        st.markdown("### ✅ Current Setup")
        data = st.session_state.user_data
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"👤 **{data.get('name', 'N/A')}**\n📍 {data.get('city', 'N/A')}, {data.get('area', 'N/A')}")
        with col2:
            st.info(f"🏠 **{data.get('home_facility', 'N/A')} {data.get('home_type', 'N/A')}**\n👥 {data.get('people', 'N/A')} people")
        with col3:
            appliances_text = ", ".join(data.get('appliances', [])) if data.get('appliances') else "None"
            st.info(f"⚡ **Appliances:**\n{appliances_text}")

# DAILY TRACKING PAGE
elif page == "📊 Daily Tracking":
    if not st.session_state.setup_complete:
        st.warning("⚠️ Please complete the home setup first!")
        st.stop()
    
    st.markdown("## 📊 Daily Energy Consumption Tracking")
    
    # Day selection
    today = datetime.now().date()
    selected_date = st.date_input("📅 Select Date", value=today, max_value=today)
    day_name = selected_date.strftime('%A')
    
    st.markdown(f"### ☀️ Tracking for {day_name}, {selected_date}")
    
    # Base consumption
    base_consumption = calculate_base_consumption(st.session_state.user_data.get('home_facility', '2BHK'))
    daily_consumption = base_consumption
    
    st.markdown(f"""
    <div class="metric-container">
        <h4>🏠 Base Home Consumption: {base_consumption} units</h4>
        <small>Based on your {st.session_state.user_data.get('home_facility', '2BHK')} home</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Appliance usage tracking
    st.markdown("### 🔌 Appliance Usage Today")
    appliance_usage = {}
    appliances = st.session_state.user_data.get('appliances', [])
    
    if appliances:
        cols = st.columns(min(3, len(appliances)))
        for i, appliance in enumerate(appliances):
            with cols[i % 3]:
                used = st.checkbox(f"Used {appliance} today?", key=f"appliance_{appliance}")
                if used:
                    hours = st.slider(f"Hours used", 1, 24, 8, key=f"hours_{appliance}")
                    consumption = get_appliance_consumption(appliance) * (hours / 8)  # Normalized to 8 hours
                    appliance_usage[appliance] = consumption
                    daily_consumption += consumption
                    
                    st.markdown(f"""
                    <div class="appliance-card">
                        <strong>{appliance}</strong><br>
                        🕐 {hours} hours<br>
                        ⚡ +{consumption:.1f} units
                    </div>
                    """, unsafe_allow_html=True)
    
    # Solar energy
    st.markdown("### ☀️ Renewable Energy")
    solar_used = st.checkbox("Used Solar Energy today?")
    solar_reduction = 0
    if solar_used:
        solar_hours = st.slider("Solar generation hours", 1, 12, 6)
        solar_reduction = solar_hours * 1.5  # 1.5 units per hour
        daily_consumption -= solar_reduction
        st.success(f"🌞 Solar energy reduced consumption by {solar_reduction:.1f} units!")
    
    # Final consumption calculation
    daily_consumption = max(0, daily_consumption)  # Ensure non-negative
    category, css_class = get_consumption_category(daily_consumption)
    
    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⚡ Total Consumption", f"{daily_consumption:.1f} units", 
                 delta=f"{daily_consumption - base_consumption:.1f}")
    with col2:
        st.metric("📊 Category", category)
    with col3:
        estimated_cost = daily_consumption * 5.5  # Assuming ₹5.5 per unit
        st.metric("💰 Estimated Cost", f"₹{estimated_cost:.0f}")
    
    # Save daily data
    if st.button("💾 Save Today's Data", type="primary"):
        daily_data = {
            'date': selected_date.strftime('%Y-%m-%d'),
            'day': day_name,
            'user_name': st.session_state.user_data.get('name'),
            'base_consumption': base_consumption,
            'appliance_consumption': sum(appliance_usage.values()),
            'solar_reduction': solar_reduction,
            'total_consumption': daily_consumption,
            'estimated_cost': daily_consumption * 5.5,
            'appliances_used': list(appliance_usage.keys())
        }
        
        # Load existing data and append
        existing_data = load_data()
        if existing_data.empty:
            df = pd.DataFrame([daily_data])
        else:
            df = pd.concat([existing_data, pd.DataFrame([daily_data])], ignore_index=True)
        
        # Remove duplicates for same date
        df = df.drop_duplicates(subset=['date', 'user_name'], keep='last')
        
        if save_data(df.to_dict('records')):
            st.success("✅ Data saved successfully!")
            st.session_state.daily_consumption.append(daily_data)
        else:
            st.error("❌ Failed to save data")

# ANALYTICS PAGE
elif page == "📈 Analytics":
    st.markdown("## 📈 Energy Consumption Analytics")
    
    # Load data
    data = load_data()
    
    if data.empty:
        st.info("📊 No data available yet. Start tracking your daily consumption!")
        st.stop()
    
    # Filter data for current user if available
    if st.session_state.get('user_data', {}).get('name'):
        user_data = data[data['user_name'] == st.session_state.user_data['name']]
        if not user_data.empty:
            data = user_data
    
    # Convert date column
    data['date'] = pd.to_datetime(data['date'])
    data = data.sort_values('date')
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_consumption = data['total_consumption'].mean()
        st.metric("📊 Avg Daily Consumption", f"{avg_consumption:.1f} units")
    with col2:
        total_cost = data['estimated_cost'].sum()
        st.metric("💰 Total Cost", f"₹{total_cost:.0f}")
    with col3:
        max_consumption = data['total_consumption'].max()
        st.metric("📈 Peak Consumption", f"{max_consumption:.1f} units")
    with col4:
        total_solar = data['solar_reduction'].sum()
        st.metric("🌞 Solar Savings", f"{total_solar:.1f} units")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily consumption trend
        fig1 = px.line(data, x='date', y='total_consumption', 
                      title='📈 Daily Energy Consumption Trend',
                      labels={'total_consumption': 'Consumption (units)', 'date': 'Date'})
        fig1.update_traces(line_color='#667eea', line_width=3)
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Consumption by day of week
        day_avg = data.groupby('day')['total_consumption'].mean().reset_index()
        fig2 = px.bar(day_avg, x='day', y='total_consumption',
                     title='📊 Average Consumption by Day',
                     labels={'total_consumption': 'Avg Consumption (units)', 'day': 'Day'})
        fig2.update_traces(marker_color='#764ba2')
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Recent data table
    st.markdown("### 📋 Recent Consumption Data")
    recent_data = data.tail(10)[['date', 'day', 'total_consumption', 'estimated_cost', 'solar_reduction']]
    recent_data['date'] = recent_data['date'].dt.strftime('%Y-%m-%d')
    st.dataframe(recent_data, use_container_width=True)

# ENERGY TIPS PAGE
elif page == "💡 Energy Tips":
    st.markdown("## 💡 Smart Energy Saving Tips")
    
    tips = [
        {
            "icon": "❄️",
            "title": "Air Conditioning Optimization",
            "tip": "Set AC temperature to 24°C or higher. Each degree lower increases consumption by 6%. Use ceiling fans to feel cooler at higher temperatures.",
            "savings": "Save up to 30% on AC bills"
        },
        {
            "icon": "🌞",
            "title": "Natural Lighting",
            "tip": "Use natural light during daytime. Replace traditional bulbs with LED lights which consume 75% less energy and last 25 times longer.",
            "savings": "Reduce lighting costs by 75%"
        },
        {
            "icon": "🔌",
            "title": "Unplug Devices",
            "tip": "Unplug electronics when not in use. Many devices consume 'phantom power' even when turned off, accounting for 5-10% of home energy use.",
            "savings": "Save 5-10% on electricity bills"
        },
        {
            "icon": "🌡️",
            "title": "Water Heater Settings",
            "tip": "Set water heater temperature to 60°C. Insulate your water heater and pipes. Take shorter showers to reduce hot water usage.",
            "savings": "Reduce water heating costs by 25%"
        },
        {
            "icon": "🏠",
            "title": "Home Insulation",
            "tip": "Seal air leaks around windows and doors. Use curtains and blinds to block heat during summer and retain warmth in winter.",
            "savings": "Save 15-20% on heating/cooling"
        },
        {
            "icon": "⚡",
            "title": "Energy-Efficient Appliances",
            "tip": "Choose appliances with 5-star energy ratings. They may cost more upfront but save significantly over their lifetime.",
            "savings": "Save 20-50% on appliance energy use"
        }
    ]
    
    for tip in tips:
        st.markdown(f"""
        <div class="energy-tip">
            <h3>{tip['icon']} {tip['title']}</h3>
            <p>{tip['tip']}</p>
            <strong>💰 {tip['savings']}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Carbon footprint information
    st.markdown("---")
    st.markdown("## 🌍 Environmental Impact")
    
    if st.session_state.daily_consumption:
        total_units = sum([day['total_consumption'] for day in st.session_state.daily_consumption])
        co2_saved = total_units * 0.85  # Approximate CO2 kg per unit
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🌱 CO2 Footprint", f"{co2_saved:.1f} kg CO2")
        with col2:
            trees_equivalent = co2_saved / 22  # 1 tree absorbs ~22kg CO2 per year
            st.metric("🌳 Trees Needed", f"{trees_equivalent:.1f} trees")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🏡 Smart Home Energy Tracker | Built with ❤️ using Streamlit</p>
    <p>💡 Track • Analyze • Optimize • Save</p>
</div>
""", unsafe_allow_html=True)