import streamlit as st

from predict import analyze_text

st.set_page_config(
    page_title="Mirra",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Mirra")
st.caption(
    "AI Trust Analysis Assistant"
)

st.write(
    "Analyze claims, evidence, and context before sharing information."
)

st.divider()

text = st.text_area(
    "Paste a post, article, or claim",
    height=200,
    placeholder="Enter text here..."
)

if st.button("Analyze", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text.")
        st.stop()

    with st.spinner("Analyzing..."):

        report = analyze_text(text)

    local_analysis = report["local_analysis"]
    ai_analysis = report["ai_analysis"]

    # -------------------------
    # Summary
    # -------------------------

    st.subheader("📝 Mirra Summary")

    st.info(ai_analysis["summary"])

    # -------------------------
    # Detailed Analysis
    # -------------------------

    with st.expander("🔍 Detailed Analysis"):

        sections = ai_analysis["sections"]

        st.markdown("### Claim Detection")
        st.write(sections["claim_detection"])

        st.markdown("### Evidence Analysis")
        st.write(sections["evidence_analysis"])

        st.markdown("### Clickbait Analysis")
        st.write(sections["clickbait_analysis"])

        st.markdown("### Cherry Picking Analysis")
        st.write(sections["cherry_picking_analysis"])

        st.markdown("### Verification Recommendation")
        st.write(sections["verification_recommendation"])

    # -------------------------
    # Technical Analysis
    # -------------------------

    with st.expander("📊 Technical Analysis"):

        st.metric(
            "Credibility Confidence",
            f"{local_analysis['confidence']}%"
        )

        st.metric(
            "Emotion Score",
            local_analysis["emotion_score"]
        )

        st.metric(
            "Clickbait Score",
            local_analysis["clickbait_score"]
        )

        st.metric(
            "Evidence Score",
            local_analysis["evidence_score"]
        )

        st.metric(
            "Cherry Picking Risk",
            f"{ai_analysis['cherry_picking_risk']}%"
        )

        st.markdown("---")

        st.write(
            f"Assessment: **{local_analysis['assessment']}**"
        )