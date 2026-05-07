import os

import requests
import streamlit as st

st.set_page_config(
    page_title="Decryptogen",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000/predict")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: black;
        }

        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(14, 165, 233, 0.18), transparent 22%),
                radial-gradient(circle at 90% 8%, rgba(249, 115, 22, 0.18), transparent 18%),
                radial-gradient(circle at 84% 82%, rgba(34, 197, 94, 0.14), transparent 20%),
                linear-gradient(180deg, #f8fafc 0%, #eef2ff 52%, #e2e8f0 100%);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image: linear-gradient(rgba(15, 23, 42, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(15, 23, 42, 0.03) 1px, transparent 1px);
            background-size: 42px 42px;
            mask-image: radial-gradient(circle at center, black 46%, transparent 100%);
            opacity: 0.7;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.96), rgba(15, 23, 42, 0.88));
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        [data-testid="stSidebar"] .stButton button {
            background: linear-gradient(135deg, #38bdf8 0%, #14b8a6 100%);
            color: white;
            border: none;
        }

        .eyebrow {
            display: inline-flex;
            gap: 0.5rem;
            align-items: center;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.08);
            color: #0f172a;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 2.2rem 2rem 1.7rem 2rem;
            border-radius: 30px;
            background: linear-gradient(135deg, rgba(8, 15, 30, 0.98), rgba(15, 23, 42, 0.88) 58%, rgba(30, 41, 59, 0.94));
            color: white;
            box-shadow: 0 28px 70px rgba(15, 23, 42, 0.28);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: auto -12% -40% auto;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.22), transparent 62%);
            filter: blur(10px);
        }

        .hero-grid {
            display: grid;
            grid-template-columns: 1.35fr 0.85fr;
            gap: 1rem;
            align-items: end;
        }

        .hero h1 {
            margin: 0;
            font-family: 'Fraunces', serif;
            font-size: clamp(2.8rem, 6vw, 5rem);
            line-height: 1.05;
            letter-spacing: -0.06em;
        }

        .hero p {
            margin-top: 0.85rem;
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.03rem;
            max-width: 56ch;
        }

        .hero-copy {
            position: relative;
            z-index: 1;
        }

        .hero-side {
            position: relative;
            z-index: 1;
            display: grid;
            gap: 0.7rem;
        }

        .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
        }

        .chip {
            display: inline-block;
            padding: 0.5rem 0.8rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.11);
            color: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.12);
            font-size: 0.82rem;
        }

        .panel {
            background: rgba(255, 255, 255, 0.82);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(148, 163, 184, 0.24);
            border-radius: 26px;
            padding: 1.2rem 1.2rem 1rem 1.2rem;
            box-shadow: 0 18px 42px rgba(15, 23, 42, 0.09);
        }

        .panel-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.75rem;
        }

        .panel h2, .panel h3 {
            margin-bottom: 0.2rem;
        }

        .section-label {
            color: #475569;
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
        }

        .subtle-card {
            border-radius: 20px;
            border: 1px solid rgba(148, 163, 184, 0.25);
            background: linear-gradient(180deg, rgba(255,255,255,0.92), rgba(248,250,252,0.9));
            padding: 0.9rem 1rem;
            margin-top: 0.8rem;
        }

        .subtle-card p {
            margin: 0;
            color: #334155;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.8rem;
            margin-top: 0.9rem;
        }

        .metric-box {
            border-radius: 18px;
            padding: 0.95rem 1rem;
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(37, 99, 235, 0.92));
            color: white;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
        }

        .metric-box.alt {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(20, 184, 166, 0.92));
        }

        .metric-label {
            display: block;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: rgba(255,255,255,0.75);
            margin-bottom: 0.35rem;
        }

        .metric-value {
            font-size: 1.35rem;
            font-weight: 800;
            line-height: 1.1;
        }

        .result-card {
            position: relative;
            overflow: hidden;
            border-radius: 26px;
            padding: 1.3rem 1.2rem 1.1rem 1.2rem;
            background: linear-gradient(135deg, #020617 0%, #111827 55%, #0f172a 100%);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 22px 54px rgba(15, 23, 42, 0.26);
        }

        .result-card::after {
            content: "";
            position: absolute;
            inset: auto -20% -45% auto;
            width: 340px;
            height: 340px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.22), transparent 60%);
        }

        .result-card * {
            position: relative;
            z-index: 1;
        }

        .result-title {
            margin: 0;
            font-family: 'Fraunces', serif;
            font-size: 2rem;
            letter-spacing: -0.04em;
        }

        .result-score {
            margin: 0.3rem 0 0.8rem 0;
            color: rgba(255,255,255,0.78);
        }

        .prob-row {
            display: grid;
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .prob-item {
            display: grid;
            gap: 0.35rem;
        }

        .prob-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            color: rgba(255,255,255,0.9);
            font-size: 0.92rem;
            font-weight: 600;
        }

        .progress-track {
            width: 100%;
            height: 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.1);
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, #38bdf8 0%, #14b8a6 100%);
        }

        .footer-note {
            margin-top: 0.85rem;
            color: #64748b;
            font-size: 0.92rem;
        }

        .stButton > button {
            width: 100%;
            border: none;
            border-radius: 16px;
            padding: 0.9rem 1rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            color: white;
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #06b6d4 100%);
            box-shadow: 0 12px 26px rgba(15, 23, 42, 0.2);
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 32px rgba(15, 23, 42, 0.24);
        }

        .stSlider > div[data-baseweb="slider"] > div {
            padding-top: 0.2rem;
        }

        div[data-baseweb="select"] > div {
            border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="hero-grid">
            <div class="hero-copy">
                <span class="eyebrow">FastAPI + Streamlit + Docker</span>
                <h1>Decryptogen</h1>
                <p>
                    A polished personality predictor that turns a few lifestyle signals into an instant
                    introvert or extrovert estimate. The Streamlit app handles the interface and the FastAPI
                    service returns the model prediction.
                </p>
            </div>
            <div class="hero-side">
                <div class="chip-row">
                    <span class="chip">Beautiful UI</span>
                    <span class="chip">FastAPI backend</span>
                    <span class="chip">Docker ready</span>
                    <span class="chip">Hugging Face Space</span>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

left, right = st.columns([1.08, 0.92], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title"><div><div class="section-label">Input profile</div><h2>Tell the model who you are</h2></div></div>', unsafe_allow_html=True)
    st.caption("These controls match the exact feature order expected by the FastAPI model.")

    top_left, top_right = st.columns(2)
    with top_left:
        time_spent_alone = st.slider("Time spent alone", 0.0, 10.0, 5.0, 0.5)
        social_event_attendance = st.slider("Social event attendance", 0.0, 10.0, 5.0, 0.5)
        friends_circle_size = st.slider("Friends circle size", 0.0, 25.0, 8.0, 1.0)
    with top_right:
        stage_fear = st.selectbox("Stage fear", ["No", "Yes"], index=0)
        going_outside = st.slider("Going outside", 0.0, 10.0, 5.0, 0.5)
        drained_after_socializing = st.selectbox("Drained after socializing", ["No", "Yes"], index=0)

    post_frequency = st.slider("Post frequency", 0.0, 20.0, 5.0, 1.0)

    st.markdown(
        """
        <div class="subtle-card">
            <p><strong>Tip:</strong> Higher values for time alone and drained-after-socializing usually push toward introvert.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    submit = st.button("Generate prediction", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title"><div><div class="section-label">Outcome</div><h2>Model response</h2></div></div>', unsafe_allow_html=True)
    st.caption(f"Frontend is calling: {API_URL}")

    if submit:
        payload = {
            "Time_spent_Alone": time_spent_alone,
            "Stage_fear": stage_fear,
            "Social_event_attendance": social_event_attendance,
            "Going_outside": going_outside,
            "Drained_after_socializing": drained_after_socializing,
            "Friends_circle_size": friends_circle_size,
            "Post_frequency": post_frequency,
        }

        with st.spinner("Calling FastAPI backend..."):
            try:
                response = requests.post(API_URL, json=payload, timeout=20)
                response.raise_for_status()
                result = response.json()

                personality = result.get("personality", "Unknown")
                confidence = result.get("confidence", "0%")
                probabilities = result.get("probabilities", {})
                extrovert_value = float(probabilities.get("Extrovert", 0))
                introvert_value = float(probabilities.get("Introvert", 0))

                st.markdown(
                    f"""
                    <div class="result-card">
                        <p class="section-label" style="color: rgba(255,255,255,0.7); margin-bottom: 0.4rem;">Prediction</p>
                        <h2 class="result-title">{personality}</h2>
                        <p class="result-score">Confidence: {confidence}</p>

                        <div class="metric-grid">
                            <div class="metric-box">
                                <span class="metric-label">Extrovert</span>
                                <div class="metric-value">{extrovert_value:.2f}%</div>
                            </div>
                            <div class="metric-box alt">
                                <span class="metric-label">Introvert</span>
                                <div class="metric-value">{introvert_value:.2f}%</div>
                            </div>
                        </div>

                        <div class="prob-row">
                            <div class="prob-item">
                                <div class="prob-head"><span>Extrovert likelihood</span><span>{extrovert_value:.2f}%</span></div>
                                <div class="progress-track"><div class="progress-fill" style="width: {extrovert_value}%"></div></div>
                            </div>
                            <div class="prob-item">
                                <div class="prob-head"><span>Introvert likelihood</span><span>{introvert_value:.2f}%</span></div>
                                <div class="progress-track"><div class="progress-fill" style="width: {introvert_value}%"></div></div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.success("Prediction received from FastAPI.")
            except requests.RequestException as exc:
                st.error(f"Could not reach the FastAPI server: {exc}")
            except ValueError:
                st.error("The FastAPI server returned an invalid response.")
    else:
        st.markdown(
            """
            <div class="result-card">
                <p class="section-label" style="color: rgba(255,255,255,0.7); margin-bottom: 0.4rem;">Preview</p>
                <h2 class="result-title">Ready when you are</h2>
                <p class="result-score">Adjust the inputs and generate a personality estimate.</p>
                <div class="subtle-card" style="background: rgba(255,255,255,0.06); border-color: rgba(255,255,255,0.1); color: white;">
                    <p style="color: rgba(255,255,255,0.84);">Your prediction will appear here with confidence and probability bars.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='footer-note'>If you are running inside Docker on Hugging Face Spaces, the API URL can stay as localhost.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.caption("Tip: In Docker on Hugging Face Spaces, Streamlit listens on port 7860 and FastAPI stays internal on port 8000.")
