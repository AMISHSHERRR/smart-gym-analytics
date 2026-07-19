import csv
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Database path
CSV_FILE = r"C:\gym_project\gym_members.csv"

# Page layout configurations
st.set_page_config(page_title="Smart Gym Analytics", page_icon="🏋️‍♂️", layout="wide")

# Custom UI Styling
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #FF4B4B; text-align: center; margin-bottom: 20px; }
    .metric-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏋️‍♂️ SMART GYM MANAGEMENT & ANALYTICS</div>', unsafe_allow_html=True)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to section:", ["📊 Business Dashboard", "➕ Add New Member", "📋 View Registered Database"])

# Helper function to read data safely
def load_data():
    if not os.path.isfile(CSV_FILE):
        # Create empty file with headers if it doesn't exist
        df = pd.DataFrame(columns=["Member_ID", "Name", "Age", "Membership_Type", "Monthly_Spend"])
        df.to_csv(CSV_FILE, index=False)
        return df
    return pd.read_csv(CSV_FILE)

df = load_data()

# ==================== SECTION 1: DASHBOARD ====================
if page == "📊 Business Dashboard":
    st.subheader("🚀 Business Performance Analytics")
    
    if df.empty:
        st.info("The database is currently empty. Add members to see live charts!")
    else:
        # High-level summary metric cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Active Members", value=len(df))
        with col2:
            st.metric(label="Total Monthly Revenue", value=f"Rs. {df['Monthly_Spend'].sum()}")
        with col3:
            st.metric(label="Average Member Age", value=f"{int(df['Age'].mean())} years")
            
        st.markdown("---")
        
        # Interactive Layout Charts
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.write("#### Membership Distribution")
            fig1, ax1 = plt.subplots(figsize=(5, 4))
            type_counts = df['Membership_Type'].value_counts()
            ax1.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
            st.pyplot(fig1)
            
        with chart_col2:
            st.write("#### Revenue Generation Per Plan")
            fig2, ax2 = plt.subplots(figsize=(5, 4))
            revenue_data = df.groupby('Membership_Type')['Monthly_Spend'].sum()
            revenue_data.plot(kind='bar', color='#66b3ff', edgecolor='black', ax=ax2)
            ax2.set_ylabel("Revenue (in Rs.)")
            ax2.set_xlabel("Membership Type")
            plt.xticks(rotation=0)
            st.pyplot(fig2)

# ==================== SECTION 2: ADD MEMBER ====================
elif page == "➕ Add New Member":
    st.subheader("📝 Registration Form")
    
    with st.form("member_form", clear_on_submit=True):
        member_id = st.text_input("Member ID (e.g., 108)")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=12, max_value=100, value=25)
        m_type = st.selectbox("Select Membership Plan", ["Basic (Rs. 800)", "Standard (Rs. 1200)", "Premium (Rs. 1500)"])
        
        submit_btn = st.form_submit_button("Register Member ✨")
        
        if submit_btn:
            if not member_id or not name:
                st.error("Please fill out all input fields!")
            else:
                # Extract pricing details
                plan_name = m_type.split(" ")[0]
                spend = 800 if "Basic" in m_type else (1200 if "Standard" in m_type else 1500)
                
                # Append row cleanly to CSV
                with open(CSV_FILE, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([member_id, name, age, plan_name, spend])
                    
                st.success(f"Success! Added {name} into the database securely.")
                st.balloons() # Drop visual effects

# ==================== SECTION 3: VIEW DATABASE ====================
elif page == "📋 View Registered Database":
    st.subheader("🔍 Central Member Records")
    
    if df.empty:
        st.warning("No tracking history found inside gym_members.csv.")
    else:
        # Search utility feature
        search_query = st.text_input("🔍 Quick Search by Name:", "")
        if search_query:
            filtered_df = df[df['Name'].str.contains(search_query, case=False, na=False)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)