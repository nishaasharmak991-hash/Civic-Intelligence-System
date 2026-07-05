import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
st.set_page_config(
    page_title="Civic Intelligence Admin",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container{
    padding-top:1rem;
}
</style>
"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)
st.title(" Civic Intelligence Admin Dashboard")

st.markdown("---")

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "community.db"
)

DB_PATH = os.path.abspath(DB_PATH)

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query(
    "SELECT * FROM complaints ORDER BY created_at DESC",
    conn
)

# ==========================================
# Statistics
# ==========================================

total = len(df)

pending = len(df[df["status"] == "Pending"])

resolved = len(df[df["status"] == "Resolved"])

high = len(df[df["severity"] == "High"])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📋 Total", total)

with col2:
    st.metric("⏳ Pending", pending)

with col3:
    st.metric("✅ Resolved", resolved)

with col4:
    st.metric("🚨 High Severity", high)

st.markdown("---")
search = st.text_input(
    "🔍 Search Complaint ID"
)

if search:

    df = df[
        df["complaint_id"]
        .str.contains(search, case=False)
    ]

st.markdown("---")

st.subheader("✏ Update Complaint Status")

complaint_ids = df["complaint_id"].tolist()

if complaint_ids:

    selected_id = st.selectbox(
        "Select Complaint",
        complaint_ids
    )

    new_status = st.selectbox(
        "New Status",
        [
            "Pending",
            "In Progress",
            "Resolved"
        ]
    )

    if st.button("💾 Update Status"):

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE complaints
            SET status=?
            WHERE complaint_id=?
            """,
            (new_status, selected_id)
        )

        conn.commit()

        st.success("Status Updated Successfully")

        st.rerun()
st.dataframe(
    df,
    use_container_width=True
)

# ==========================================
# Charts
# ==========================================

st.markdown("---")

st.subheader("📊 Complaints by Category")

category_count = df["category"].value_counts()

fig, ax = plt.subplots()

ax.bar(category_count.index, category_count.values)

plt.xticks(rotation=30)

st.pyplot(fig)

st.subheader("📈 Complaint Status Distribution")

status_count = df["status"].value_counts()

fig2, ax2 = plt.subplots()

ax2.pie(
    status_count.values,
    labels=status_count.index,
    autopct="%1.1f%%"
)

st.pyplot(fig2)

conn.close()
st.markdown("---")

#st.caption(
#    "2026 Civic Intelligence System | Decision Intelligence Platform"
#)
