import streamlit as st
import json

# Set up page config
st.set_page_config(page_title="Election Cell HQ", layout="wide", page_icon="🛡️")

# Custom CSS for Glassmorphism
st.markdown("""
<style>
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(0, 240, 255, 0.4);
        transform: translateY(-2px);
    }
    .name-text {
        font-size: 1.05rem;
        font-weight: 600;
        color: #ffffff;
    }
    .desig-badge {
        background-color: rgba(0, 240, 255, 0.15);
        border: 1px solid rgba(0, 240, 255, 0.3);
        color: #00F0FF;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
        margin-left: 8px;
        text-transform: uppercase;
    }
    .station-text {
        color: #94a3b8;
        font-size: 0.85rem;
        display: block;
        margin-top: 4px;
    }
    .phone-btn {
        background: rgba(0, 240, 255, 0.1);
        color: #00F0FF !important;
        border: 1px solid rgba(0, 240, 255, 0.3);
        text-decoration: none;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 12px;
        transition: all 0.3s ease;
    }
    .phone-btn:hover {
        background: #00F0FF;
        color: #050A30 !important;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

personnel_data = load_data()

# Header
col_logo, col_title = st.columns([1, 10])
with col_logo:
    st.markdown("<h1 style='text-align: center; color: #00F0FF;'>👮‍♂️</h1>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h2 style='margin-bottom: 0; padding-bottom: 0;'>Election Monitoring Cell</h2>", unsafe_allow_html=True)
    st.caption("Virudhunagar District Police Dashboard")

st.divider()

# Controls
if personnel_data:
    constituencies = sorted(list(set([p['ac_name'] for p in personnel_data])))
    
    col_filter1, col_filter2 = st.columns([1, 1])
    with col_filter1:
        selected_const = st.selectbox("📌 Select Constituency", constituencies)
    with col_filter2:
        search_q = st.text_input("🔍 Search Name, Designation or Station")

    team_type = st.radio("Team Type", ["FST (Flying Squad)", "SST (Static Surveillance)"], horizontal=True)
    selected_team_type = "FST" if "FST" in team_type else "SST"

    # Filter data
    filtered = [p for p in personnel_data if p['ac_name'] == selected_const and p['team_type'] == selected_team_type]
    
    if search_q:
        sq = search_q.lower()
        filtered = [
            p for p in filtered 
            if sq in p.get('name','').lower() 
            or sq in p.get('designation','').lower() 
            or sq in p.get('station','').lower() 
            or sq in p.get('phone','')
        ]

    st.markdown("<br/>", unsafe_allow_html=True)

    if not filtered:
        st.info("ℹ️ No personnel found matching the criteria.")
    else:
        # Group by team number
        team_nums = sorted(list(set([p['team_number'] for p in filtered])))
        
        for tnum in team_nums:
            st.markdown(f"<h3 style='color: #FFD700;'>🔷 Team {tnum}</h3>", unsafe_allow_html=True)
            t_data = [p for p in filtered if p['team_number'] == tnum]
            
            # Group by shift
            shifts = sorted(list(set([p['shift'] for p in t_data])))
            
            # Show shifts side-by-side using columns
            cols = st.columns(len(shifts) if len(shifts) > 0 else 1)
            
            for idx, snum in enumerate(shifts):
                s_data = [p for p in t_data if p['shift'] == snum]
                with cols[idx % len(cols)]:
                    st.markdown(f"**⏰ Shift {snum}**")
                    for person in s_data:
                        name = person.get('name', 'Unknown')
                        desig = person.get('designation', 'PC')
                        station = person.get('station', '')
                        phone = person.get('phone', '')
                        
                        styled_phone = f"{phone[:5]} {phone[5:]}" if len(phone) == 10 else phone
                        
                        st.markdown(f"""
                        <div class="glass-card">
                            <span class="name-text">{name}</span>
                            <span class="desig-badge">{desig}</span>
                            <span class="station-text">{station}</span>
                            <a href="tel:{phone}" class="phone-btn">📞 Call {styled_phone}</a>
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown("---")
else:
    st.error("Data could not be loaded. Please ensure data.json is present in the repository.")
