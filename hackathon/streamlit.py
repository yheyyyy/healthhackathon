import streamlit as st
from create_calendar import main
from get_response import get_response

def chatbot():
    st.title("AI-Powered Chatbot")

    # User selects mode before interacting
    mode = st.radio("Choose a mode:", ["Chat", "Schedule an Appointment"])

    # Add examples section at the top
    st.sidebar.markdown("### Example Prompts")
    if mode == "Chat":
        if st.sidebar.button("❓ What are the mental Health Services?"):
            prompt = "What are the mental Health Services??"
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = get_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
        if st.sidebar.button("💡 Help me reschedule my appointments"):
            prompt = "Help me reschedule my appointments"
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = get_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
    elif mode == "Schedule an Appointment":
        if st.sidebar.button("📅 Schedule Dummy Appointment 1"):
            prompt = ("Dear Ms. DIANE, You have a First Visit Consultation at ENT-Head & "
                     "Neck Surg Ctr - 15C, NUH Medical Centre, Zone B, Level 15, 15c, "
                     "Lift Lobby B2 on 19 Feb 2025 at 3:45 pm.")
            st.session_state.messages.append({"role": "user", "content": prompt})
            appointment_details = main(prompt)
            response = (f"✅ Appointment created:\n"
                       f"Appointment Name: {appointment_details['appointment']}\n"
                       f"Location: {appointment_details['location']}\n"
                       f"Date: {appointment_details['date']}\n"
                       f"Time: {appointment_details['time']}")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
        if st.sidebar.button("📅 Schedule Dummy Appointment 2"):
            prompt = ("Dear Ms. DIANE, You have a Second Visit Consultation at ENT-Head & "
                     "Neck Surg Ctr - 15C, NUH Medical Centre, Zone B, Level 15, 15c, "
                     "Lift Lobby B2 on 19 July 2025 at 3:45 pm.")
            st.session_state.messages.append({"role": "user", "content": prompt})
            appointment_details = main(prompt)
            response = (f"✅ Appointment created:\n"
                       f"Appointment Name: {appointment_details['appointment']}\n"
                       f"Location: {appointment_details['location']}\n"
                       f"Date: {appointment_details['date']}\n"
                       f"Time: {appointment_details['time']}")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

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
            response = (f"✅ Appointment created:\n"
                       f"Appointment Name: {appointment_details['appointment']}\n"
                       f"Location: {appointment_details['location']}\n"
                       f"Date: {appointment_details['date']}\n"
                       f"Time: {appointment_details['time']}")
        else:
            # Calls the LLM for general queries
            response = get_response(prompt)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    chatbot()
