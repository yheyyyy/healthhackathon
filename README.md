# Healthhacks Chatbot

## Prerequisites

### 1. Install Ollama
1. Download and install Ollama from [https://ollama.com/](https://ollama.com/)
2. After installation, open command prompt and run:
```bash
ollama pull iodose/nuextract-v1.5
```
This will download the nuextract-v1.5 model for Ollama for the extraction task.
3. Keep Ollama running in the background while using the application

### 2. Google Calendar Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials (API & Services > Crendentials)
5. Create Credentials, Create OAuth client ID, and select Web application
6. Add `http://localhost:8080/` to the Authorized redirect URIs
7. Download the credentials JSON file

## Requirements Installation

1. Clone this repository
2. Install the required packages using:
```bash
pip install -r requirements.txt
```
This should download all the dependencies for the running of this application.

## Environment Setup
1. Create a `.env` file in the root directory
2. Copy these values from your Google OAuth credentials JSON:
```
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
GOOGLE_PROJECT_ID=your_project_id
```

## Running the Application

1. Ensure Ollama is running in the background
2. Start the Streamlit application:
```bash
streamlit run streamlit.py
```
3. The application will open at `http://localhost:8501`
4. First-time users will be prompted to authenticate with Google Calendar

## Troubleshooting
- If you get Ollama connection errors, ensure Ollama is running
- If calendar events aren't creating, check your Google Calendar permissions
- For authentication issues, delete `token.pickle` and restart the application

## System Requirements
- Python 3.12+
- Windows/Mac/Linux OS
- Internet connection for Google Calendar API
- Minimum 8GB RAM recommended for Ollama

Project References:
https://khayrul-rules.medium.com/youll-never-create-calendar-events-manually-again-after-today-here-s-why-52427c6e06cb