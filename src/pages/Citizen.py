# ==========================================
# ==========================================

# ---------- Imports ----------
import json
import os
from datetime import datetime
from dashboard import show_dashboard
from complaint_form import show_complaint_form
import streamlit as st
from dotenv import load_dotenv
from google import genai
from report_view import show_report
from streamlit_mic_recorder import mic_recorder

import database
from complaint_id import generate_complaint_id
from speech_to_text import transcribe_audio
from ai_analysis import analyze_text_complaint
from image_analysis import analyze_image
from pdf_generator import create_pdf

if st.button("🏠 Home"):
    st.switch_page("app.py")
# ---------- Database creation----------

database.create_database()


# ---------- Gemini Key ----------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ---------- Page Configuration Part----------

st.set_page_config(
    page_title="Civic Intelligence System",
    page_icon="🏙️",
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


# ==========================================
# Dashboard Statistics
# ==========================================
show_dashboard(database)

# ---------- Session State ----------

if "problem" not in st.session_state:
    st.session_state.problem = ""

if "report" not in st.session_state:
    st.session_state.report = None
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

if "complaint_id" not in st.session_state:
    st.session_state.complaint_id = None


# ---------- Main Title ----------

st.title("Civic Intelligence System")

st.subheader(
    "Citizen Complaint Management Platform"
)

st.markdown("---")
# ==========================================
# Sidebar
# ==========================================

# st.sidebar.title("🏙 Civic Intelligence")

# st.sidebar.success("Version 1.0")

# st.sidebar.markdown("---")

# st.sidebar.write("### Available Services")

# st.sidebar.write("✅ Text Complaint")

# st.sidebar.write("✅ Voice Complaint")

# st.sidebar.write("✅ Image Complaint")

# st.sidebar.write("✅ AI Decision Intelligence")

# st.sidebar.write("✅ PDF Report")

st.sidebar.markdown("---")

st.sidebar.info(
    """
Civic Intelligence System

Designed for Citizens and Government
to intelligently manage
community complaints.
"""
)

# ==========================================
# Language Selection
# ==========================================

language = st.selectbox(

    "🌐 Select Language",

    [

        "English",

        "Hindi",

        "Punjabi"

    ]

)

# =================================================
# Current Date & Time of complaint registration
# =================================================

st.write(

    "📅",

    datetime.now().strftime("%d-%m-%Y %H:%M")

)

st.markdown("---")

# ==========================================
# Complaint Details
# ==========================================

category = st.selectbox(

    "📂 Complaint Category",

    [

        "Traffic",

        "Waste Management",

        "Water",

        "Healthcare",

        "Energy",

        "Environment",

        "Public Safety",

        "Not Sure"

    ]

)

location = st.text_input(

    "Complaint Location"

)

st.markdown("---")


# # st.subheader("📝 Register a New Complaint")

# #st.caption(
#     #"Choose one of the following methods to submit your complaint."
# )
# # ==========================================
# # Complaint Input Tabs
# # ==========================================

# #tab1, tab2, tab3 = st.tabs(

#    # [

#        # "📝 Text Complaint",

#         "🎤 Voice Complaint",

#         "📷 Image Complaint"

#     ]

# )

# # ==========================================
# # Text Complaint
# # ==========================================

# with tab1:

#     problem = st.text_area(

#         "Describe your complaint",

#         value=st.session_state.problem,

#         height=180

#     )

#     if problem:

#         st.session_state.problem = problem


# # ==========================================
# # Voice Complaint
# # ==========================================

# with tab2:

#     st.write(

#         "Click the microphone and speak your complaint."

#     )

#     audio = mic_recorder(

#         start_prompt="🎙 Start Recording",

#         stop_prompt="⏹ Stop Recording",

#         just_once=True,

#         use_container_width=True

#     )

#     if audio:

#         with st.spinner(

#             "Converting speech to text..."

#         ):

#             complaint = transcribe_audio(

#                 client,

#                 audio["bytes"]

#             )

#         st.session_state.problem = complaint

#         st.success(

#             "Speech converted successfully."

#         )

#         st.text_area(

#             "Recognized Complaint",

#             complaint,

#             height=180,

#             disabled=True

#         )


# # ==========================================
# # Image Complaint
# # ==========================================

# with tab3:

#     uploaded_image = st.file_uploader(

#         "Upload Complaint Image",

#         type=[

#             "jpg",

#             "jpeg",

#             "png"

#         ]

#     )

#     if uploaded_image:

#         st.image(

#             uploaded_image,

#             use_container_width=True

#         )

#         st.success(

#             "Image uploaded successfully."

#         )

# # Keep uploaded image after Streamlit reruns

# if "uploaded_image" not in st.session_state:
#     st.session_state.uploaded_image = None

# if uploaded_image is not None:
#     st.session_state.uploaded_image = uploaded_image

# uploaded_image = st.session_state.uploaded_image
# problem = st.session_state.problem

# st.markdown("---")

# ==========================================
# Analysis Button
# ==========================================
problem, uploaded_image = show_complaint_form(client)
if st.button(

    " Analyze Complaint",

    use_container_width=True

):

    # --------------------------------------
    # Validation
    # --------------------------------------

    if location.strip() == "":

        st.warning(

            "Please enter complaint location."

        )

    elif problem.strip() == "" and uploaded_image is None:

        st.warning(

            "Please enter a complaint or upload an image."

        )

    else:

        with st.spinner(

            "AI is analyzing your complaint..."

        ):

            # ------------------------------
            # Image Complaint
            # ------------------------------

            if uploaded_image is not None:

                report = analyze_image(

                    client,

                    uploaded_image,

                    language

                )

            # ------------------------------
            # Text / Voice Complaint
            # ------------------------------

            else:

                report = analyze_text_complaint(

                    client,

                    category,

                    location,

                    problem,

                    language

                )

            
            # ==========================================
# Generate Complaint ID
# ==========================================

            complaint_id = generate_complaint_id()


# ==========================================
# Save Complaint
# ==========================================

            database.save_complaint(

            complaint_id=complaint_id,

            created_at=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            category=category,

            issue_type=category,

            location=location,

            complaint=problem if problem.strip() != "" else "Image Complaint",

            language=language,

            source="Image" if uploaded_image is not None else "Text/Voice",

            severity=report["severity"],

            priority_score=report["priority_score"],

            department=", ".join(report["department"]),

            status="Pending",

            image_name=uploaded_image.name if uploaded_image is not None else "",

            assigned_officer="",

            latitude=None,

            longitude=None,

            ai_report=json.dumps(report)

        )   
        # ==========================================
# Generate PDF
# ==========================================

        pdf_path = create_pdf(

            complaint_id,

            category,

            location,

            language,

            problem if problem.strip() != "" else "Image Complaint",

            report

        )
        # if st.session_state.report is None:
        #     st.stop()
        st.session_state.report = report
        st.session_state.complaint_id = complaint_id
        st.session_state.pdf_path = pdf_path

        st.success("✅ Complaint Registered Successfully")

        st.info(f"Complaint ID : {complaint_id}")

        st.markdown("---")

        # ==========================================
# AI Decision Intelligence Report
# ==========================================

#     report = st.session_state.report
#     complaint_id = st.session_state.complaint_id
#     pdf_path = st.session_state.pdf_path

#     st.subheader("📋 AI Decision Intelligence Report")

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.metric("Issue Type", report["issue_type"])

#     with col2:

#         severity = report["severity"].lower()

#         if severity == "high":
#          st.error("🔴 HIGH")
#         elif severity == "medium":
#             st.warning("🟠 MEDIUM")
#         elif severity == "low":
#             st.success("🟢 LOW")
#         else:
#             st.info(report["severity"])

#     with col3:

#         score = int(report["priority_score"])

#         st.metric("Priority Score", f"{score}%")

#         st.progress(score / 100)

#     st.markdown("---")

#     st.subheader("📄 Problem Summary")
#     st.write(report["problem_summary"])

#     st.subheader("🏢 Responsible Departments")
#     for dept in report["department"]:
#         st.markdown(f"- {dept}")

#     st.subheader("🔍 Root Causes")
#     for cause in report["root_causes"]:
#         st.markdown(f"- {cause}")

#     st.subheader("⚡ Immediate Actions")
#     for action in report["immediate_actions"]:
#         st.markdown(f"- {action}")

#     st.subheader("📅 Short-term Actions")
#     for action in report["short_term_actions"]:
#         st.markdown(f"- {action}")

#     st.subheader("🚀 Long-term Actions")
#     for action in report["long_term_actions"]:
#         st.markdown(f"- {action}")

#     st.subheader("🌱 Community Benefits")
#     for benefit in report["community_benefits"]:
#         st.markdown(f"- {benefit}")
#         # ==========================================
# # Download PDF
# # ==========================================
# if pdf_path is not None:
#     with open(pdf_path, "rb") as pdf:

#             st.download_button(

#             "📄 Download Complaint Report",

#             pdf,

#             file_name=f"{complaint_id}.pdf",

#             mime="application/pdf",

#             use_container_width=True

#          )
show_report()
st.markdown("---")

# st.caption(
#     "© 2026 Civic Intelligence System | AI Powered Decision Intelligence Platform"
# )