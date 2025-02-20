#Healthhacks Chatbot

# Project Setup and Running Instructions

## Requirements Installation

1. Clone this repository
2. Install the required packages using:
```bash
pip install -r requirements.txt
```
This should download all the dependencies for the running of this application.

## Environment Setup
Obtain the information from the json file downloaded from Google OAuth
Create a `.env` file in the root directory with the following format:
```
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_AUTH_URI=
GOOGLE_TOKEN_URI=
GOOGLE_AUTH_PROVIDER_CERT_URL=
GOOGLE_PROJECT_ID=
```

## Running the Application

To run the Streamlit application:
```bash
streamlit run streamlit.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Note
Make sure you have Python 3.12+ installed on your system before running the application.
