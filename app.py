import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# পেজ সেটআপ (ওয়াইড স্ক্রিন থিম)
st.set_page_config(page_title="IBZ VFS Live Tracker Matrix", layout="wide")

# ==========================================
# ১. মক ডেটাবেজ জেনারেশন (বাস্তবে এটি SQLite বা PostgreSQL হবে)
# ==========================================
@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    file_numbers = list(range(170000, 180601))
    total_files = len(file_numbers)
    
    countries = ['Bangladesh', 'India', 'Morocco', 'Cameroon', 'Turkey', 'Unknown']
    statuses = ['Applied', 'Registered', 'Accord', 'Refus']
    
    # রিকোয়ারমেন্ট অনুযায়ী ডাটাবেজ টেবিল স্ট্রাকচার তৈরি
    data = {
        'File Number': file_numbers,
        'VFS Number': [f"VFSDAC{random.randint(10000,99999)}" if random.random() > 0.3 else f"VFSDEL{random.randint(10000,99999)}" for _ in range(total_files)],
        'Country': np.random.choice(countries, total_files, p=[0.3, 0.2, 0.15, 0.1, 0.1, 0.15]),
        'Status': np.random.choice(statuses, total_files, p=[0.2, 0.3, 0.3, 0.2]),
        'Submission Month': np.random.choice(['May', 'June', 'July', 'August'], total_files),
        'Decision Day': np.random.choice(['Monday', 'Wednesday', 'Friday'], total_files)
    }
    return pd.DataFrame(data)

df = generate_mock_data()

# ==========================================
# ২. ড্যাশবোর্ড ইন্টারফেস ও ফিল্টারিং
# ==========================================
st.title("📊 IBZ VFS Advanced File Analytics Matrix")
st.markdown("---")

# শর্ত ১০: সামগ্রিক (Overall) এবং দেশভিত্তিক (Country-wise) দেখার অপশন
view_type = st.radio("Select View Profile:", ["Overall Statistics", "Country-wise Analysis"], horizontal=True)

if view_type == "Country-wise Analysis":
    # শর্ত ৯: দেশভিত্তিক চার্ট ফিল্টার করার ড্রপডাউন
    selected_country = st.selectbox("Select Target Country:", df['Country'].unique())
    filtered_df = df[df['Country'] == selected_country]
else:
    filtered_df = df

# টোটাল কাউন্টার বা কেপিআই ব্লক
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Monitored Files (170000-180600)", len(filtered_df))
col2.metric("Total Decisions (Accord/Refus)", len(filtered_df[filtered_df['Status'].isin(['Accord', 'Refus'])]))
col3.metric("Approved (Accord)", len(filtered_df[filtered_df['Status'] == 'Accord']))
col4.metric("Rejected (Refus)", len(filtered_df[filtered_df['Status'] == 'Refus']))

st.markdown("---")

# ==========================================
# ৩. চার্ট ও গ্রাফ এরিয়া (শর্ত ৮, ৯)
# ==========================================
st.subheader("📈 Visualization Panels (Pie & Bar Charts)")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("### Overall Status Breakdown (Pie Chart)")
    status_counts = filtered_df['Status'].value_counts()
    # স্ট্রিমলিটে পাই চার্টের জন্য ডাটাফ্রেম রেডি করা
    st.dataframe(status_counts) 

with chart_col2:
    st.write("### Monthly Volume (Bar Chart)")
    monthly_counts = filtered_df.groupby(['Submission Month', 'Status']).size().unstack(fill_value=0)
    st.bar_chart(monthly_counts)

# ==========================================
# ৪. বটের কাজের মেকানিজম এবং ব্যাকএন্ড সিমুলেশন লজিক
# ==========================================
st.markdown("---")
st.subheader("🤖 Live Anti-Block Bot Controller (Background Process Simulation)")

# ইউজার ইন্টারফেসে লাইভ প্রসেস দেখানোর জন্য এক্সপ্যান্ডার
with st.expander("View Bot Execution Log (Rules 1, 3, 4, 5, 6, 11)"):
    st.info("Bot is initialized. Monitoring Range: 170000 to 180600.")
    
    # টেস্ট করার জন্য ৩টি ফাইলের লুপ চালিয়ে ডেমো দেখানো হচ্ছে
    sample_range = [170001, 170002, 170003]
    
    for current_file in sample_range:
        st.write(f"**[Target File: {current_file}]** checking system queue...")
        
        # শর্ত ৪: ডিসিশন হয়ে গেলে (Accord/Reject) চেক করবে না
        mock_db_status = df[df['File Number'] == current_file]['Status'].values[0]
        if mock_db_status in ['Accord', 'Refus']:
            st.warning(f"⏩ File {current_file} skipped! Reason: Decision is already made ({mock_db_status}).")
            continue
            
        # শর্ত ৩: VFSDAC এ পাওয়া গেলে অন্য VFS দিয়ে চেক দেবে না
        vfs_num = df[df['File Number'] == current_file]['VFS Number'].values[0]
        if "VFSDAC" in vfs_num:
            st.success(f"🎯 File located in Dhaka Port ({vfs_num}). Secondary VFS checks aborted to save bandwidth.")
        
        # শর্ত ৬ এবং ১১: আইপি চেঞ্জার এবং হিউম্যান বিহেভিয়ার নকল
        fake_ips = ["192.168.45.12", "185.220.101.5", "45.132.22.109"]
        st.code(f"🔄 Rotating Proxy: IP Changed to -> {random.choice(fake_ips)} | User-Agent: Chrome/v126.0.0 (Windows NT 10.0)")
        
        # শর্ত ৫: ১৫ সেকেন্ড পর পর ডাটা নেওয়া (এখানে ডেমোর জন্য ১ সেকেন্ড দেওয়া হলো)
        st.write("⏳ Bot sleeping for 15 seconds to remain completely risk-free...")
        # time.sleep(15) # প্রোডাকশনে এটি আন-কমেন্ট করতে হবে

# ==========================================
# ৫. ডাটা টেবিল ভিউ (শর্ত ৭)
# ==========================================
st.markdown("---")
st.subheader("📋 Master Data Inventory View")
# ফাইল ইন্টারফেসে সাবমিশন, রেজিস্ট্রেশন, ডিসিশনের পাশাপাশি VFS নম্বর দেখানো
st.dataframe(filtered_df[['File Number', 'VFS Number', 'Country', 'Status', 'Submission Month']], use_container_width=True)
