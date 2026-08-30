import sys
from pathlib import Path

import streamlit as st

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
st.write("Ask a question about OrbitDesk and get a knowledge-grounded support response.")

st.caption(
    "🛡️ Support boundaries: I can explain product behavior and troubleshoot, "
    "but I cannot make account changes, view secrets, create credentials, "
    "issue refunds, contact recipients, or guarantee recovery of deleted data."
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

                # Top metrics row
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Classification", result.get("classification", "unknown").upper())
                with col2:
                    conf = result.get("confidence", 0)
                    st.metric("Confidence", f"{conf:.2f}")
                with col3:
                    needs_human = result.get("requires_human", False)
                    st.metric("Needs Human", "YES" if needs_human else "NO")

                # Reason
                if result.get("reason"):
                    st.caption(f"**Reason:** {result['reason']}")

                # Warnings
                for warning in result.get("warnings", []):
                    st.warning(f"⚠️ {warning}")

                # Clarification question
                if result.get("clarification_question"):
                    st.info(f"**Clarification needed:** {result['clarification_question']}")

                # Answer
                st.subheader("Answer")
                st.write(result.get("answer", "No answer provided."))

                # Escalation banner
                if result.get("classification") == "requires_escalation":
                    st.error(
                        "This request requires human approval or elevated permissions. "
                        "The support assistant cannot complete this action."
                    )
                    # Try to extract role from answer
                    answer_text = result.get("answer", "")
                    if "Owner" in answer_text or "Admin" in answer_text:
                        st.write("Check the answer above for the required role/team.")

                # Sources
                sources = result.get("sources", [])
                if sources:
                    st.subheader("Sources")
                    for src in sources:
                        sid = src.get("source_id", "Unknown")
                        passage = src.get("passage", "")
                        st.write(f"**{sid}**")
                        st.write(passage[:600] + "..." if len(passage) > 600 else passage)
                        st.divider()

            except Exception as e:
                st.error("An error occurred while processing the question.")
                st.exception(e)