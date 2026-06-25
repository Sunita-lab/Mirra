import streamlit as st
from predict import analyze_text

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Mirra",
    page_icon="🔍",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3.2em;
    font-weight: 600;
    font-size: 16px;
}

.feature-card {
    padding: 18px;
    border-radius: 12px;
    background-color: rgba(120,120,120,0.08);
    margin-bottom: 20px;
}

.summary-card {
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🔍 Mirra")

st.markdown("""
### AI-Powered Trust Analysis Assistant

Analyze credibility, evidence quality, context completeness,
and verification needs before sharing information.
""")

st.info(
    "Mirra evaluates trust signals in content. "
    "It does not determine absolute truth or falsehood."
)

# --------------------------------------------------
# Feature Card
# --------------------------------------------------

st.markdown("""
<div class="feature-card">

### What Mirra Analyzes

✅ Credibility Signals

✅ Evidence Quality

✅ Clickbait & Emotional Language

✅ Cherry-Picking Risk

✅ Verification Needs

</div>
""", unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# Input Area
# --------------------------------------------------

text = st.text_area(
    "Paste a post, article, or claim",
    height=220,
    placeholder="Enter text here..."
)

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

if st.button("🔍 Analyze Content", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text.")
        st.stop()

    with st.spinner("Analyzing content..."):

        report = analyze_text(text)

    local_analysis = report["local_analysis"]
    ai_analysis = report["ai_analysis"]

    assessment = local_analysis["assessment"]

    # --------------------------------------------------
    # Assessment Banner
    # --------------------------------------------------

    if assessment == "Likely Reliable":
        st.success(f"✅ Assessment: {assessment}")
    else:
        st.error(f"⚠️ Assessment: {assessment}")

    # --------------------------------------------------
    # Trust Meter
    # --------------------------------------------------

    st.markdown("### Trust Confidence")

    confidence_value = min(
        int(local_analysis["confidence"]),
        100
    )

    st.progress(confidence_value)

    st.caption(
        f"Model Confidence: {local_analysis['confidence']}%"
    )

    st.divider()

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    with st.container(border=True):

        st.subheader("📝 Mirra Summary")

        st.write(
            ai_analysis["summary"]
        )

    st.write("")

    # --------------------------------------------------
    # Detailed Analysis
    # --------------------------------------------------

    with st.expander(
        "🔍 Detailed Analysis",
        expanded=False
    ):

        sections = ai_analysis["sections"]

        st.markdown("### Claim Detection")
        st.write(
            sections["claim_detection"]
        )

        st.markdown("### Evidence Analysis")
        st.write(
            sections["evidence_analysis"]
        )

        st.markdown("### Clickbait Analysis")
        st.write(
            sections["clickbait_analysis"]
        )

        st.markdown("### Cherry Picking Analysis")
        st.write(
            sections["cherry_picking_analysis"]
        )

        st.markdown("### Verification Recommendation")
        st.write(
            sections["verification_recommendation"]
        )

    # --------------------------------------------------
    # Technical Analysis
    # --------------------------------------------------

    with st.expander(
        "📊 Technical Analysis",
        expanded=False
    ):

        st.markdown("### Mirra Signal Scores")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Confidence",
                f"{local_analysis['confidence']}%"
            )

        with col2:
            st.metric(
                "Emotion",
                local_analysis["emotion_score"]
            )

        with col3:
            st.metric(
                "Evidence",
                local_analysis["evidence_score"]
            )

        col4, col5 = st.columns(2)

        with col4:
            st.metric(
                "Clickbait",
                local_analysis["clickbait_score"]
            )

        with col5:
            st.metric(
                "Cherry Picking",
                f"{ai_analysis.get('cherry_picking_risk', 0)}%"
            )

        st.markdown("---")

        st.markdown("### Assessment")

        st.write(
            f"**{local_analysis['assessment']}**"
        )

        st.markdown("---")

        st.markdown("### ℹ️ What These Metrics Mean")

        with st.expander("Confidence"):
            st.write(
                "Represents how confident the ML model is in its prediction. "
                "Higher confidence means the model is more certain, not necessarily more correct."
            )

        with st.expander("Emotion"):
            st.write(
                "Measures emotional intensity in the language. "
                "Higher values indicate stronger emotional wording."
            )

        with st.expander("Clickbait"):
            st.write(
                "Detects sensational or attention-grabbing language patterns."
            )

        with st.expander("Evidence"):
            st.write(
                "Measures the presence of evidence indicators such as studies, reports, surveys, research, and data references."
            )

        with st.expander("Cherry Picking"):
            st.write(
                "Estimates the risk that information may be presented without enough context or supporting details."
            )