from PIL import Image
import streamlit as st
from unified_agent import process_message
from ocr_tool import ocr_tool_function
import os

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "preview_message" not in st.session_state:
    st.session_state.preview_message = None

with open('css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# Load the logo and face images
logo = Image.open("imgs/logo.jpg")
assist_face = "imgs/face.png"
user_face = "imgs/face2.png"

def page1():
    st.title('Monthly Calendar')
    st.markdown('<iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=Asia%2FSingapore&showPrint=0&showTitle=0&showTabs=0&showTz=0&title=Healthhacks&src=ODAzZGZjYjljNWUwZmYyNzU4OGUxNTlmMTFhOTU4MDNhZDNhZDQzZWYzNDU5ZjRiNDQyN2VlMzgxYjA3NmI1ZEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t&color=%23A79B8E" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)

def page2():
    st.title('Weekly Calendar')
    st.markdown('<iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=Asia%2FSingapore&showPrint=0&showTitle=0&showTabs=0&showTz=0&title=Healthhacks&mode=WEEK&src=ODAzZGZjYjljNWUwZmYyNzU4OGUxNTlmMTFhOTU4MDNhZDNhZDQzZWYzNDU5ZjRiNDQyN2VlMzgxYjA3NmI1ZEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t&color=%23A79B8E" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)

def page3():
    st.title('Appointment Overview')
    st.markdown('<iframe src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=Asia%2FSingapore&showPrint=0&showTitle=0&showTabs=0&showTz=0&title=Healthhacks&mode=AGENDA&src=ODAzZGZjYjljNWUwZmYyNzU4OGUxNTlmMTFhOTU4MDNhZDNhZDQzZWYzNDU5ZjRiNDQyN2VlMzgxYjA3NmI1ZEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t&color=%23A79B8E" style="border-width:0" width="800" height="600" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)


def chatbot():
    st.logo(logo)
    st.title("AI-Powered Healthcare Assistant")
    
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        response = process_message(prompt)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar=user_face):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar=assist_face):
                st.write(message["content"])
    
    st.sidebar.markdown("### Demo Instructions")
    
    if st.sidebar.button("❓ What is the hotline for rescheduling appointments?"):
        prompt = "What is the hotline for rescheduling appointments?"
        st.session_state.preview_message = prompt
        st.rerun()
        
    if st.sidebar.button("💡 Help me schedule an appointment"):
        prompt = ("Dear Ms. DIANE, You have a First Visit Consultation at ENT-Head & Neck Surg Ctr - \
                    15C, NUH Medical Centre, Zone B, Level 15, 15c, Lift Lobby B2 on 17 Mar 2025 at 3:45 pm.")
        st.session_state.preview_message = prompt
        st.rerun()
    
    if st.sidebar.button("📷 Insert sample screenshot"):
        uploaded_file = "imgs/message.jpg"
        extracted_text = ocr_tool_function(uploaded_file)        
        st.image(uploaded_file, caption='Uploaded Image', use_container_width=True)
        st.write("Extracted Text: ", extracted_text)
        st.session_state.preview_message = extracted_text
        st.rerun()


    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        extracted_text = ocr_tool_function(uploaded_file)        
        st.image(uploaded_file, caption='Uploaded Image', use_container_width=True)
        st.write("Extracted Text: ", extracted_text)
        st.session_state.preview_message = extracted_text
        st.rerun()
        
    # # Initialize chat history
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    # # Display chat history
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"], avatar=user_face):
    #         st.markdown(message["content"])

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

def main():
    # Initialize the page state if it doesn't exist
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Chatbot"
    
    # Create a top navigation bar with buttons instead of links
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Chatbot", use_container_width=True):
            st.session_state.current_page = "Chatbot"
            
    with col2:
        if st.button("Monthly Calendar", use_container_width=True):
            st.session_state.current_page = "Monthly"
            
    with col3:
        if st.button("Weekly Calendar", use_container_width=True):
            st.session_state.current_page = "Weekly"
            
    with col4:
        if st.button("Appointment Overview", use_container_width=True):
            st.session_state.current_page = "Overview"
    
    # Route to the appropriate page based on session state
    if st.session_state.current_page == "Monthly":
        page1()
    elif st.session_state.current_page == "Weekly":
        page2()
    elif st.session_state.current_page == "Overview":
        page3()
    else:  # Default to Chatbot
        chatbot()


if __name__ == "__main__":
    main()
