import streamlit as st

st.set_page_config(
    page_title="Civic Intelligence System",
    page_icon=" ",
    layout="wide"
)
hide_streamlit_style = """
<style>

/* Hide Streamlit page navigation */
[data-testid="stSidebarNav"] {
    display: none;
}

/* Hide hamburger menu */
#MainMenu {
    visibility: hidden;
}

/* Hide footer */
footer {
    visibility: hidden;
}

/* Hide header */
header {
    visibility: hidden;
}

</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title(" Civic Intelligence System")
st.subheader(" Decision Intelligence Platform")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##  Citizen Portal")
    st.write("Register and track complaints.")

    if st.button("Open Citizen Portal", use_container_width=True):
        st.switch_page("pages/Citizen.py")

with col2:
    st.markdown("## Admin Portal")
    st.write("Authorized users only.")

    if st.button("Admin Login", use_container_width=True):
        st.switch_page("pages/Admin_Login.py")