import streamlit as st
import time
from google import genai


st.set_page_config(
    page_title="GIVENOV | Research Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.stApp {
    background-color: #0b1120;
    color: #e2e8f0;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #263449;
}

h1, h2, h3 {
    color: #67e8f9 !important;
}

.stChatMessage {
    background-color: #172337;
    border-radius: 12px;
    border: 1px solid #263449;
}

.stChatInput {
    border: 1px solid #22d3ee;
}

div.stButton > button {
    background-color: #164e63;
    color: white;
    border-radius: 8px;
    border: 1px solid #22d3ee;
}

div.stButton > button:hover {
    background-color: #0e7490;
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("# 🌍 GIVENOV")
    st.caption("ENVIRONMENTAL INTELLIGENCE")
    st.divider()

    page = st.radio(
        "Workspace",
        [
            "Research Assistant",
            "Environmental Analysis",
            "Geographical Intelligence",
            "Research History",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### System Status")
    st.success("Application Online")
    st.info("AI Engine: Gemini")
    st.caption("GIVENOV Development Build 0.2")

if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM_PROMPT = """
You are GIVENOV, an advanced environmental and geographical
research assistant.

Specialisations:
1. Environmental science
2. Geography
3. Climate science
4. Environmental monitoring
5. Geographical information systems
6. Scientific data interpretation

Responsibilities:
- Answer scientific questions.
- Explain environmental phenomena.
- Analyse information provided by users.
- Interpret environmental measurements.
- Explain geographical processes.
- Identify patterns in supplied datasets.
- Produce structured research summaries.

Scientific integrity:
- Never invent measurements.
- Never fabricate research sources.
- Distinguish established facts from assumptions.
- Explain uncertainty.
- Request additional information when necessary.

Use clear, objective and evidence-oriented explanations.
"""


@st.cache_resource
def connect_ai(api_key):
    return genai.Client(api_key=api_key)


MODELS = [
    "gemini-2.5-flash",
]


def generate_response(client, conversation):
    errors = []

    for model in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=conversation,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "max_output_tokens": 1200,
                    },
                )

                if not getattr(response, "text", None):
                    raise ValueError("Empty AI response")

                return response.text, model

            except Exception as error:
                error_message = str(error)
                errors.append(f"{model}: {error_message}")

                if attempt == 0 and any(
                    code in error_message
                    for code in ("429", "500", "502", "503")
                ):
                    time.sleep(2)
                    continue

                break

    raise RuntimeError(
        "All configured AI models failed. " + " | ".join(errors)
    )


if page == "Research Assistant":
    st.title("GIVENOV Research Intelligence")
    st.markdown("### Investigate. Analyse. Understand.")
    st.caption(
        "Your AI-powered environmental and geographical "
        "research assistant."
    )
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.info("🌡️ Climate Science")
    col2.info("🌱 Environmental Systems")
    col3.info("🗺️ Geographical Research")

    st.divider()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask GIVENOV a research question...")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
                client = connect_ai(api_key)

                conversation = [
                    {
                        "role": (
                            "user"
                            if message["role"] == "user"
                            else "model"
                        ),
                        "parts": [{"text": message["content"]}],
                    }
                    for message in st.session_state.messages
                ]

                with st.spinner(
                    "GIVENOV is analysing your question..."
                ):
                    answer, selected_model = generate_response(
                        client,
                        conversation,
                    )

                st.markdown(answer)
                st.caption(f"AI Model: {selected_model}")

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except KeyError:
                st.error(
                    "GEMINI_API_KEY is missing from Streamlit Secrets."
                )

            except Exception as error:
                st.error(
                    "GIVENOV could not obtain an AI response."
                )
                st.info(
                    "Possible causes include temporary service "
                    "unavailability, API limits or configuration problems."
                )
                st.caption(str(error))

elif page == "Environmental Analysis":
    st.title("Environmental Analysis")
    st.write("Environmental data analysis workspace.")
    st.info(
        "Dataset processing and environmental measurements "
        "are planned for a future build."
    )

elif page == "Geographical Intelligence":
    st.title("Geographical Intelligence")
    st.write("Geographical research and mapping workspace.")
    st.info(
        "Interactive geographical mapping and coordinate "
        "analysis are planned."
    )

elif page == "Research History":
    st.title("Research History")
    st.write("Your current research session.")

    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.expander(message["role"].title()):
                st.write(message["content"])
    else:
        st.info("No research conversations yet.")
