import streamlit as st


def show_report():

    if (
        st.session_state.report is None
        or st.session_state.pdf_path is None
        or st.session_state.complaint_id is None
    ):
        return

    report = st.session_state.report
    complaint_id = st.session_state.complaint_id
    pdf_path = st.session_state.pdf_path

    st.success("✅ Complaint Registered Successfully")
    st.info(f"Complaint ID : {complaint_id}")

    st.markdown("---")
    st.subheader("📋 AI Decision Intelligence Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Issue Type", report["issue_type"])

    with col2:

        severity = report["severity"].lower()

        if severity == "high":
            st.error("🔴 HIGH")

        elif severity == "medium":
            st.warning("🟠 MEDIUM")

        elif severity == "low":
            st.success("🟢 LOW")

        else:
            st.info(report["severity"])

    with col3:

        score = int(report["priority_score"])

        st.metric("Priority Score", f"{score}%")

        st.progress(score / 100)

    st.markdown("---")

    st.subheader("📄 Problem Summary")
    st.write(report["problem_summary"])

    st.subheader("🏢 Responsible Departments")

    for dept in report["department"]:
        st.markdown(f"- {dept}")

    st.subheader("🔍 Root Causes")

    for cause in report["root_causes"]:
        st.markdown(f"- {cause}")

    st.subheader("⚡ Immediate Actions")

    for action in report["immediate_actions"]:
        st.markdown(f"- {action}")

    st.subheader("📅 Short-term Actions")

    for action in report["short_term_actions"]:
        st.markdown(f"- {action}")

    st.subheader("🚀 Long-term Actions")

    for action in report["long_term_actions"]:
        st.markdown(f"- {action}")

    st.subheader("🌱 Community Benefits")

    for benefit in report["community_benefits"]:
        st.markdown(f"- {benefit}")

    with open(pdf_path, "rb") as pdf:

        st.download_button(
            "📄 Download Complaint Report",
            pdf,
            file_name=f"{complaint_id}.pdf",
            mime="application/pdf",
            use_container_width=True
        )