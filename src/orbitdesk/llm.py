import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

if not api_key:
    raise ValueError("GROQ_API_KEY is not configured.")

client = Groq(api_key=api_key)


def generate_answer(question, evidence, classification_hint):
    # Build context with source tags
    context_parts = []
    for item in evidence:
        tag = item.get("source_type", "kb").upper()
        if item.get("outdated"):
            tag += " | OUTDATED"
        context_parts.append(f"[{tag}] {item['source_id']}:\n{item['passage']}")
    
    context = "\n\n---\n\n".join(context_parts)

    system_prompt = """You are OrbitDesk's support assistant. Obey these rules:

1. Answer using ONLY the provided evidence. Do not invent facts.
2. Cite sources by their ID (e.g., "According to KB-003...").
3. NEVER ask for, reveal, or transform passwords, API secrets, OAuth tokens, or payment info.
4. You CANNOT: change accounts, create credentials, execute exports, issue refunds, contact recipients, or give legal/medical/financial advice.
5. If the user asks for an action you cannot do, explain which authorized role can do it (Owner, Admin, Analyst, Viewer).
6. If evidence conflicts, trust current KB documents over resolved cases. Flag outdated cases in warnings.
7. You must respond with valid JSON only. No markdown, no extra text.

Required JSON fields:
- classification: answerable | requires_clarification | requires_escalation | out_of_scope | safe_failure
- answer: your response text
- sources: array of {source_id, passage} for evidence actually used
- confidence: number 0.0 to 1.0
- requires_human: boolean (true for escalations)
- reason: brief routing explanation
- clarification_question: string or null
- warnings: array of strings (e.g., "CASE-0914 is superseded")"""

    user_prompt = f"""User question: {question}

Hinted classification: {classification_hint}

Evidence:
{context}

Return ONLY valid JSON. Do not wrap it in markdown code blocks."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    
    # Remove markdown code block if present
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    parsed = json.loads(content)

    # Safety: ensure all required fields exist
    required_defaults = {
        "classification": "safe_failure",
        "answer": "No answer provided.",
        "sources": [],
        "confidence": 0.0,
        "requires_human": False,
        "reason": "No reason provided.",
        "clarification_question": None,
        "warnings": []
    }
    
    for field, default in required_defaults.items():
        if field not in parsed:
            parsed[field] = default

    return parsed