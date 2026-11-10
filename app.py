import time
import streamlit as st
from utils import SAMPLE_RAW_TEXT, extract_pdf_text
from ai_client import analyze_with_gemini

st.set_page_config(page_title="ClauseGuard AI", page_icon="⚖️", layout="wide")

if "doc_content" not in st.session_state:
    st.session_state["doc_content"] = ""
if "last_uploaded_name" not in st.session_state:
    st.session_state["last_uploaded_name"] = None

def load_sample():
    st.session_state["doc_content"] = SAMPLE_RAW_TEXT
    st.session_state["contract_text_box"] = SAMPLE_RAW_TEXT

with st.sidebar:
    st.title("ClauseGuard AI")
    st.caption("Automated Legal Risk Intelligence")
    api_key_input = st.text_input("Gemini API Key (Optional)", type="password")
    st.button("Load Sample Contract", on_click=load_sample, use_container_width=True)

st.header("Contract & Agreement Risk Auditor")
st.write("Upload a PDF agreement or paste contract terms to evaluate legal risk exposure.")

uploaded_file = st.file_uploader("Upload Agreement (PDF)", type=["pdf"])
if uploaded_file is not None:
    if st.session_state["last_uploaded_name"] != uploaded_file.name:
        extracted_text = extract_pdf_text(uploaded_file)
        st.session_state["doc_content"] = extracted_text
        st.session_state["contract_text_box"] = extracted_text
        st.session_state["last_uploaded_name"] = uploaded_file.name

text_input = st.text_area(
    "Contract Text to Inspect",
    value=st.session_state["doc_content"],
    height=180,
    key="contract_text_box",
)

if st.button("Analyze Contract Risks", type="primary", use_container_width=True):
    if not text_input or not text_input.strip():
        st.warning("Please upload a PDF or paste contract text before running an audit.")
    else:
        start_ts = time.time()
        with st.spinner("Evaluating contract clauses and risk vectors..."):
            data = analyze_with_gemini(text_input, api_key_input)
            elapsed = round(time.time() - start_ts, 2)

            st.divider()
            col1, col2, col3 = st.columns([1, 1, 2])

            score = int(data.get("risk_score", 50))
            with col1:
                st.metric(
                    label="Overall Risk Percentage",
                    value=f"{score}%",
                    delta=f"{score}/100 Risk Index",
                    delta_color="inverse",
                )
            with col2:
                st.metric(label="Audit Verdict", value=data.get("verdict", "Review Needed"))
            with col3:
                st.write(f"**Executive Summary** *(Analyzed in {elapsed}s)*:")
                st.write(data.get("summary", "Analysis completed."))

            st.progress(
                min(max(score, 0), 100) / 100.0,
                text=f"Calculated Contract Risk Exposure: {score}%",
            )

            st.subheader("Detected Red Flags & Negotiation Recommendations")
            for clause in data.get("clauses", []):
                risk = clause.get("risk_level", "Medium")
                color = "red" if risk == "High" else "orange" if risk == "Medium" else "green"

                with st.expander(f":{color}[{risk.upper()} RISK] - {clause.get('title')}", expanded=True):
                    st.markdown(f"**Identified Risk:** {clause.get('issue')}")
                    st.markdown(f"**Counter-Proposal:** :green[{clause.get('recommendation')}]")
