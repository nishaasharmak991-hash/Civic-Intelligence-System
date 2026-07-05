import streamlit as st


def show_dashboard(database):

    # ==========================================
    # Dashboard Header
    # ==========================================

    st.title("🏙 Civic Intelligence System")

    st.caption(
        "AI-powered Decision Intelligence Platform for Smart Communities"
    )

    st.markdown("---")

    # ==========================================
    # Dashboard Statistics
    # ==========================================

    total = database.get_total_complaints()
    high = database.get_high_priority_count()
    pending = database.get_pending_count()
    resolved = database.get_resolved_count()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📋 Total Complaints",
            total
        )

    with col2:
        st.metric(
            "🚨 High Priority",
            high
        )

    with col3:
        st.metric(
            "⏳ Pending",
            pending
        )

    with col4:
        st.metric(
            "✅ Resolved",
            resolved
        )

    st.markdown("---")