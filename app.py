import streamlit as st
import time
from main import get_llm
from langchain_core.messages import HumanMessage, AIMessage

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Gemma AI Assistant",
    page_icon="✨",
    layout="centered"
)

# Custom CSS for a more professional, modern look
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stChatMessage {
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stChatInputContainer {
            padding-bottom: 20px;
        }
        .sidebar-text {
            font-size: 0.9rem;
            color: #6c757d;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. AI LOGIC LAYER (Separated from UI)
# ==========================================
class AIChatEngine:
    """Handles the interaction with the LangChain LLM."""
    def __init__(self):
        self.llm = get_llm()

    def generate_response(self, messages):
        """Invokes the LLM and handles errors."""
        try:
            # Use invoke for the full response
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==========================================
# 3. SESSION STATE MANAGEMENT
# ==========================================
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = AIChatEngine()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# 4. SIDEBAR / SETTINGS
# ==========================================
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "This is a professional AI Assistant powered by **Gemma 3** via Ollama and LangChain."
    )

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<p class="sidebar-text">Built with Streamlit & LangChain</p>',
        unsafe_allow_html=True
    )

# ==========================================
# 5. CHAT UI/UX
# ==========================================
st.title("✨ Gemma AI Assistant")
st.caption("Experience the power of generative AI with a clean, modern interface.")

# Display existing chat history
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# User Input
if prompt := st.chat_input("Type your message here..."):
    # 1. Add and display user message
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate and display AI response
    with st.chat_message("assistant"):
        # Loading state
        with st.spinner("Thinking..."):
            response_text = st.session_state.chat_engine.generate_response(st.session_state.messages)

            # Simulate a slight delay for better UX (optional)
            # time.sleep(0.5)

            st.markdown(response_text)

    # 3. Add AI response to history
    st.session_state.messages.append(AIMessage(content=response_text))

# Footer
st.markdown(
    """
    <div style="position: fixed; bottom: 10px; right: 10px; font-size: 12px; color: gray;">
        Powered by Ollama & LangChain
    </div>
    """,
    unsafe_allow_html=True
)
