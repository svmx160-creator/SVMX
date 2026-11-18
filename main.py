import streamlit as st
from openai import OpenAI, OpenAIError

st.set_page_config(
    page_title="GIVENOV.",
    page_icon="🌍",
)

st.title("GIVENOV")
st.caption("Environmental & Geographical Research Assistant")

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are GIVENOV AI, an intelligent research assistant.

Your specialisations are:
1. Environmental Science
2. Geographical Research
3. Climate and Weather Analysis
4. Environmental Data Interpretation
5. Scientific Research

Always provide accurate and well-structured explanations.
Never invent scientific measurements or research findings.
Use verified information and differentiate between assumptions and facts.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask GIVENOV a question…"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages,
                ],
            )

            answer = response.choices[0].message.content
            if not answer:
                st.error("The API returned an empty response. Please try again.")
            else:
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
        except OpenAIError as exc:
            status_code = getattr(exc, "status_code", None)
            status_text = f" (HTTP {status_code})" if status_code else ""
            st.error(f"OpenAI request failed{status_text}: {exc}")
