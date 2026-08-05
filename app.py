
import sys
from pathlib import Path

import streamlit as st

# Add the OrbitDesk source directory to Python's import path
BASE_DIR = Path(__file__).resolve().parent
ORBITDESK_DIR = BASE_DIR / "src" / "orbitdesk"

sys.path.insert(0, str(ORBITDESK_DIR))

from pipeline import answer_question


st.set_page_config(
    page_title="OrbitDesk Support Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 OrbitDesk Support Agent")
st.write(
    "Ask a question about OrbitDesk and get a knowledge-grounded support response."
)

question = st.text_area(
    "Enter your question:",
    placeholder="Example: Why did my scheduled export fail?",
    height=100
)

if st.button("Ask OrbitDesk", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Processing your question..."):

            try:
                result = answer_question(question.strip())

                st.subheader("Classification")
                st.info(result["classification"])

                if result["classification"] == "ANSWERABLE":

                    st.subheader("Answer")
                    st.write(result["answer"])

                    st.subheader("Retrieved Evidence")

                    for evidence in result.get("evidence", []):
                        with st.expander(
                            f"{evidence.get('document_id', 'Unknown document')} "
                            f"— Score: {evidence.get('score', 0):.3f}"
                        ):
                            st.write(evidence.get("passage", ""))

                else:
                    st.subheader("Response")
                    st.write(result["message"])

            except Exception as e:
                st.error("An error occurred while processing the question.")
                st.exception(e)

