import streamlit as st
from unified_agent import process_message

def chatbot():
    st.title("AI-Powered Healthcare Assistant")

    # Add examples section at the top
    st.sidebar.markdown("### Example Prompts")
    
    # Initialize session state for preview message
    if "preview_message" not in st.session_state:
        st.session_state.preview_message = None
    
    if st.sidebar.button("❓ What are the Mental Health Services?"):
        prompt = "What are the mental health services available?"
        st.session_state.preview_message = prompt
        
    if st.sidebar.button("💡 Help me schedule an appointment"):
        prompt = ("Dear Ms. DIANE, You have a First Visit Consultation at ENT-Head & Neck Surg Ctr - \
                    15C, NUH Medical Centre, Zone B, Level 15, 15c, Lift Lobby B2 on 27 Feb 2025 at 3:45 pm.")
        st.session_state.preview_message = prompt

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Display preview message if exists
    if st.session_state.preview_message:
        with st.chat_message("preview"):
            st.markdown(st.session_state.preview_message)
            if st.button("Send this message"):
                prompt = st.session_state.preview_message
                st.session_state.messages.append({"role": "user", "content": prompt})
                response = process_message(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.preview_message = None  # Clear preview
                st.rerun()
            if st.button("Cancel"):
                st.session_state.preview_message = None
                st.rerun()

    # Regular chat input
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.preview_message = prompt
        st.rerun()

if __name__ == "__main__":
    chatbot()
