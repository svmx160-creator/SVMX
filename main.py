import streamlit as st
from google import genai

# ==================================
# APPLICATION CONFIGURATION
# ==================================

st.set_page_config(
    page_title="GIVENOV | Research Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================
# CUSTOM DESIGN
# ==================================

st.markdown("""
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
""", unsafe_allow_html=True)


# ==================================
# APPLICATION IDENTITY
# ==================================

with st.sidebar:

    st.markdown("# 🌍 GIVENOV")

    st.caption("ENVIRONMENTAL INTELLIGENCE")

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Workspace",
        [
            "Research Assistant",
            "Environmental Analysis",
            "Geographical Intelligence",
            "Research History"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### System Status")

    st.success("Application Online")

    st.info("AI Engine: Gemini")

    st.caption("GIVENOV Development Build 0.1")


# ==================================
# AI CONNECTION
# ==================================

@st.cache_resource
def connect_ai(api_key):
    return genai.Client(api_key=api_key)


# ==================================
# SESSION MEMORY
# ==================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []


# ==================================
# AI INSTRUCTIONS
# ==================================

SYSTEM_PROMPT = """
You are GIVENOV, an advanced environmental and
geographical research assistant.

Your specialisations include:

1. Environmental science
2. Geography
3. Climate science
4. Environmental monitoring
5. Geographical information systems
6. Scientific data interpretation

YOUR RESPONSIBILITIES:

- Answer scientific questions.
- Explain environmental phenomena.
- Analyse information provided by users.
- Interpret environmental measurements.
- Explain geographical processes.
- Identify patterns in supplied datasets.
- Produce structured research summaries.

SCIENTIFIC INTEGRITY:

- Never invent measurements.
- Never fabricate research sources.
- Distinguish established facts from assumptions.
- Explain uncertainty.
- Request additional information when necessary.

Your responses should be clear, scientific,
structured and informative.

Your identity is GIVENOV.
"""


# ==================================
# RESEARCH ASSISTANT
# ==================================

if page == "Research Assistant":

    st.title("GIVENOV Research Intelligence")

    st.markdown(
        "### Investigate. Analyse. Understand."
    )

    st.caption(
        "Your AI-powered environmental and geographical "
        "research assistant."
    )

    st.divider()

    # Research suggestions

    st.markdown("#### Suggested research topics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🌡️ Climate Science")

    with col2:
        st.info("🌱 Environmental Systems")

    with col3:
        st.info("🗺️ Geographical Research")

    st.divider()

    # Display conversation

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # User input

    prompt = st.chat_input(
        "Ask GIVENOV a research question..."
    )

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

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
                            if m["role"] == "user"
                            else "model"
                        ),
                        "parts": [{"text": m["content"]}]
                    }
                    for m in st.session_state.messages
                ]

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=conversation,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "max_output_tokens": 1200
                    }
                )

                answer = response.text

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error(
                    "Unable to connect to the AI engine. "
                    "Please check your API configuration."
                )

                st.caption(str(error))


# ==================================
# ENVIRONMENTAL ANALYSIS
# ==================================

elif page == "Environmental Analysis":

    st.title("Environmental Analysis")

    st.write(
        "Environmental data analysis workspace."
    )

    st.info(
        "Dataset processing and environmental "
        "measurements will be introduced in a "
        "future development build."
    )


# ==================================
# GEOGRAPHICAL INTELLIGENCE
# ==================================

elif page == "Geographical Intelligence":

    st.title("Geographical Intelligence")

    st.write(
        "Geographical research and mapping workspace."
    )

    st.info(
        "Interactive geographical mapping and "
        "coordinate analysis are planned."
    )


# ==================================
# RESEARCH HISTORY
# ==================================

elif page == "Research History":

    st.title("Research History")

    st.write(
        "Your current research session."
    )

    if st.session_state.messages:

        for message in st.session_state.messages:

            with st.expander(message["role"].title()):

                st.write(message["content"])

    else:

        st.info("No research conversations yet.")

