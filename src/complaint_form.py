import streamlit as st
from audio_recorder_streamlit import audio_recorder
from streamlit_mic_recorder import mic_recorder
from speech_to_text import transcribe_audio


def show_complaint_form(client):

    # -----------------------------
    # Session State
    # -----------------------------

    if "problem" not in st.session_state:
        st.session_state.problem = ""

    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None

    # -----------------------------
    # Heading
    # -----------------------------

    st.header("📝 Register a New Complaint")

    st.write(
        "Choose one of the methods below to submit your complaint."
    )

    # -----------------------------
    # Tabs
    # -----------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "📝 Text Complaint",
            "🎤 Voice Complaint",
            "📷 Image Complaint"
        ]
    )

    # ==========================================
    # TEXT TAB
    # ==========================================

    with tab1:

        problem = st.text_area(
            "Describe your complaint",
            value=st.session_state.problem,
            height=180
        )

        if problem:
            st.session_state.problem = problem
    # ==========================================
# VOICE TAB
# ==========================================

    with tab2:

        st.write("Click below to record your complaint.")

        audio_bytes = audio_recorder(
            text="🎤 Click to Record",
            recording_color="#e74c3c",
            neutral_color="#2ecc71",
            icon_name="microphone",
            icon_size="2x",
        )

        if audio_bytes:

            with st.spinner("Converting speech to text..."):

                complaint = transcribe_audio(
                    client,
                    audio_bytes
                )

            st.session_state.problem = complaint

            st.success("Speech converted successfully.")

            st.text_area(
                "Recognized Complaint",
                complaint,
                height=180,
                disabled=True
            )
    
    # ==========================================
# IMAGE TAB
# ==========================================

    with tab3:

        uploaded_image = st.file_uploader(

        "Upload Complaint Image",

        type=["jpg", "jpeg", "png"]

        )

        if uploaded_image is not None:

            st.session_state.uploaded_image = uploaded_image

            st.image(

            uploaded_image,

            use_container_width=True

            )

            st.success(

            "Image uploaded successfully."

            )
    # -----------------------------
    # Return Values
    # -----------------------------

    return (
        st.session_state.problem,
        st.session_state.uploaded_image
    )