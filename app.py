import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ১. পেজ এবং ওয়াইড লেআউট সেটিংস
st.set_page_config(page_title="IBZ Live Analytics & Processing Tracker", layout="wide", initial_sidebar_state="expanded")

# 🎬 কাস্টম সিএসএস (CSS) - স্মুথ স্লাইডিং ও ফেইড-ইন অ্যানিমেশন যুক্ত করা
st.markdown("""
    <style>
    /* ১. স্লাইডিং অ্যানিমেশন তৈরি */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* ২. পুরো মেইন পেজ ও কম্পোনেন্টে অ্যানিমেশন ক্লাস অ্যাপ্লাই */
    .stApp, .update-banner, .kpi-box, .animated-card {
        animation: fadeInUp 0.6s ease-out both;
    }
    
    /* ড্যাশবোর্ড থিম স্টাইলিং */
    .main { background-color: #f8f9fa; }
    
    .update-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    
    .kpi-box {
        background-color: white; padding: 22px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); text-align: center;
        border-bottom: 5px solid #007bff; margin-bottom: 20px;
        transition: transform 0.3s ease; /* মাউস নিলে হালকা নড়ার জন্য */
    }
    .kpi-box:hover {
        transform: translateY(-5px);
    }
    .kpi-box h4 { color: #888; font-size: 13px; text-transform: uppercase; margin-bottom: 5px; }
    .kpi-box h2 { color: #222; font-size: 32px; font-weight: bold; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# ২. অ্যাডভান্সড মক ডেটা জেনারেটর (১৭০০০০ - ১৮০৬০০)
# ==========================================
@st.cache_data
def generate_advanced_data():
    np.random.seed(101)
    file_numbers = list(range(170000, 180601))
    total_files = len(file_numbers)
    
    countries = ['Bangladesh', 'India', 'Morocco', 'Cameroon', 'Turkey', 'Unknown']
    statuses = ['Applied', 'Registered', 'Accord', 'Refus']
    
    # অপেক্ষার দিন গণনা
    reg_wait_days = np.random.randint(10, 30, size=total_files)      
    decision_wait_days = np.random.randint(20, 60, size=total_files) 
    total_processing_days = reg_wait_days + decision_wait_days      
    
    base_date = datetime(2026, 5, 1)
    dates = [(base_date + timedelta(days=int(i%120))).strftime('%Y-%m-%d') for i in range(total_files)]
    
    data = {
        'File Number': file_numbers,
        'VFS Number': [f"VFSDAC{random.randint(10000,99999)}" if random.random() > 0.4 else f"VFSDEL{random.randint(10000,99999)}" for _ in range(total_files)],
        'Country': np.random.choice(countries, total_files, p=[0.4, 0.2, 0.1, 0.1, 0.1, 0.1]),
        'Status': np.random.choice(statuses, total_files, p=[0.15, 0.25, 0.40, 0.20]),
        'Submission Month': np.random.choice(['May', 'June', 'July', 'August'], total_files),
        'Registration Wait (Days)': reg_wait_days,
        'Decision Wait (Days)': decision_wait_days,
        'Total Wait (Days)': total_processing_days,
        'Last Update Date': dates
    }
    return pd.DataFrame(data)

df = generate_advanced_data()

# ==========================================
# ৩. সাইডবার ফিল্টার ও প্রোফাইল ভিউ (শর্ত ৯, ১০)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #007bff; margin:0;'>🤖 IBZ Live Matrix</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:12px; color:#6c757d;'>Predictive Automation Engine</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    view_profile = st.radio("📊 Navigation View Profiler:", ["Overall Dashboard", "Country-Specific View"])
    
    if view_profile == "Country-Specific View":
        selected_country = st.selectbox("🌍 Filter by Country", df['Country'].unique())
        filtered_df = df[df['Country'] == selected_country]
    else:
        filtered_df = df
    st.markdown("---")

# ==========================================
# 📢 ৪. আজকের দৈনিক লাইভ আপডেট ব্যানার (অ্যানিমেটেড)
# ==========================================
latest_date = df['Last Update Date'].max()
today_data = filtered_df[filtered_df['Last Update Date'] == latest_date]
today_accords = len(today_data[today_data['Status'] == 'Accord'])
today_refus = len(today_data[today_data['Status'] == 'Refus'])

st.markdown(f"""
    <div class='update-banner'>
        <h3 style='margin:0; font-size:20px;'>📢 Daily Live Sync Update Box</h3>
        <p style='margin:5px 0 12px 0; opacity:0.8; font-size:13px;'>Latest Server Sync Date: {latest_date}</p>
        <div style='display:flex; gap:30px; font-size:16px;'>
            <div>🔍 Files Checked Today: <b>{len(today_data)}</b></div>
            <div>🟢 New Approvals (Accord): <b style='color:#2ecc71;'>{today_accords}</b></div>
            <div>🔴 New Rejections (Refus): <b style='color:#e74c3c;'>{today_refus}</b></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 🔍 ৫. সার্চ ইন্টারফেস (Timeline + VFS Number)
# ==========================================
st.markdown("### 🔍 Live File Registry Search")
search_input = st.text_input("", max_chars=6, placeholder="Type a 6-digit file code (e.g., 170450)...", label_visibility="collapsed")

if search_input:
    if search_input.isdigit() and 170000 <= int(search_input) <= 180600:
        match = df[df['File Number'] == int(search_input)]
        if not match.empty:
            res = match.iloc
            # সার্চ রেজাল্ট বক্সেও স্লাইডিং ক্লাস যুক্ত করা হয়েছে
            st.markdown(f"""
            <div class='animated-card' style="background-color: #ffffff; padding: 22px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-left: 6px solid #007bff; margin-bottom:20px;">
                <h4 style='margin:0; color:#007bff;'>🎯 File Number: {res['File Number']} | Connected VFS: {res['VFS Number']}</h4>
                <p style='margin:8px 0;'><b>Country Origin:</b> {res['Country']} | <b>Current Phase:</b> <span style='color:#28a745; font-weight:bold;'>{res['Status']}</span></p>
                <hr style='border:0.5px solid #eee;'>
                <div style='display:flex; gap:40px; font-size:14px; color:#555;'>
                    <div>⏳ <b>Submission to Register:</b> {res['Registration Wait (Days)']} Days</div>
                    <div>⏳ <b>Register to Decision:</b> {res['Decision Wait (Days)']} Days</div>
                    <div>📅 <b>Total Timeline Journey:</b> {res['Total Wait (Days)']} Days</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Invalid range. Enter between 170000 and 180600.")

# ==========================================
# ⏱️ ৬. প্রসেসিং ও অপেক্ষার দিন অ্যানালিটিক্স প্যানেল
# ==========================================
st.markdown("### ⏱️ Processing Waiting Time Analytics")
avg_reg = int(filtered_df['Registration Wait (Days)'].mean())
avg_dec = int(filtered_df['Decision Wait (Days)'].mean())
avg_total = int(filtered_df['Total Wait (Days)'].mean())

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown(f"<div class='kpi-box'><h4>Avg. Registration Wait</h4><h2>{avg_reg} Days</h2><p style='font-size:11px; color:#999; margin:0;'>From Submission to Register</p></div>", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"<div class='kpi-box' style='border-bottom-color:#28a745;'><h4>Avg. Decision Wait</h4><h2>{avg_dec} Days</h2><p style='font-size:11px; color:#999; margin:0;'>From Register to Decision</p></div>", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"<div class='kpi-box' style='border-bottom-color:#ffc107;'><h4>Avg. Total Processing Time</h4><h2>{avg_total} Days</h2><p style='font-size:11px; color:#999; margin:0;'>Entire Visa Lifecycle</p></div>", unsafe_allow_html=True)

# ==========================================
# 📈 𝟕. চার্ট ম্যাট্রিক্স (Pie, Bar, & Wave Charts)
# ==========================================
st.markdown("### 📊 Advanced Charts and Wave Paneling")
c_col1, c_col2 = st.columns(2)

with c_col1:
    st.markdown("#### 🍩 Decision Proportion (Donut Chart)")
    status_counts = filtered_df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    st.vega_lite_chart(status_counts, {
        'mark': {'type': 'arc', 'innerRadius': 60, 'stroke': '#fff'},
        'encoding': {
            'theta': {'field': 'Count', 'type': 'quantitative'},
            'color': {'field': 'Status', 'type': 'nominal', 'scale': {'range': ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f']}}
        }, 'height': 280
    }, use_container_width=True)

with c_col2:
    st.markdown("#### 🌊 Processing Load Timeline (Wave / Area Chart)")
    wave_data = filtered_df.groupby('Last Update Date').size().reset_index(name='Processed Files')
    st.area_chart(wave_data.set_index('Last Update Date'), height=280)

st.markdown("---")
st.markdown("#### 📊 Volume Distribution by Month (Stacked Bar)")
monthly_data = filtered_df.groupby(['Submission Month', 'Status']).size().unstack(fill_value=0)
st.bar_chart(monthly_data, height=300)

# ==========================================
# 📋 𝟖. লাইভ মাস্টার ডাটা ইনভেন্টরি
# ==========================================
st.markdown("---")
st.markdown("### 📋 Master Inventory Database View")
st.dataframe(
    filtered_df[['File Number', 'VFS Number', 'Country', 'Status', 'Registration Wait (Days)', 'Decision Wait (Days)', 'Total Wait (Days)']],
    column_config={
        "File Number": st.column_config.NumberColumn("IBZ ID", format="%d"),
        "VFS Number": "VFS Code",
        "Country": "Country",
        "Status": "Current Phase",
        "Registration Wait (Days)": "Sub ➔ Reg (Days)",
        "Decision Wait (Days)": "Reg ➔ Dec (Days)",
        "Total Wait (Days)": "Total Journey (Days)"
    }
)  # <--- এই ব্র্যাকেটটি দিয়ে ফাংশনটি শেষ করা হয়েছে
