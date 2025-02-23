import streamlit as st
from create_calendar import main
from get_response import get_response  # Import the LLM response function

def chatbot():
    st.title("AI-Powered Chatbot")

    # User selects mode before interacting
    mode = st.radio("Choose a mode:", ["Chat", "Schedule an Appointment"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if mode == "Schedule an Appointment":
            appointment_details = main(prompt)  # Calls appointment creation
            response = f"✅ Appointment created: {appointment_details}"
        else:
            response = get_response(prompt)  # Calls the LLM for general queries

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    chatbot()
