# AI-Powered Healthcare Assistant

An intelligent healthcare assistant that combines appointment scheduling capabilities with general healthcare queries using Large Language Models (LLM) and Google Calendar integration.

## Core Features

### 1. Unified Agent System
- Uses LangChain's agent framework to route queries between two main functions:
  - Appointment scheduling
  - General healthcare queries
- Powered by Ollama's Mistral 7B model for natural language understanding

### 2. Appointment Scheduling
The system can:
- Parse natural language appointment requests
- Extract key appointment details (date, time, location, type)
- Create Google Calendar events automatically
- Provide formatted confirmation messages

### 3. General Healthcare Queries
- Handles general questions about mental health services
- Provides contextual responses using conversation memory
- Maintains chat history for better context understanding

## Technical Architecture

### LLM Integration
- **Model**: Mistral 7B via Ollama
- **Purpose**: 
  - Natural language understanding
  - Query classification
  - Response generation
  - Appointment detail extraction

### Agent System
Uses two main tools:
1. **Schedule_Appointment Tool**
   - Triggers when messages start with "Dear"
   - Extracts appointment details using LLM
   - Creates Google Calendar events
   - Returns formatted confirmation

2. **General_Chat Tool**
   - Handles all non-appointment queries
   - Maintains conversation context
   - Provides healthcare-related information

### Calendar Integration
- Uses Google Calendar API for event creation
- OAuth 2.0 authentication
- Automatic token refresh handling
- Local credential storage using pickle

### User Interface
- Built with Streamlit
- Features:
  - Chat interface
  - Message preview before sending
  - Example prompts in sidebar
  - Formatted appointment confirmations

## How It Works

1. **User Input Processing**
   ```
   User Message → Unified Agent → Tool Selection → Response Generation
   ```

2. **Appointment Flow**
   ```
   Appointment Request → LLM Extraction → Calendar Creation → Confirmation
   ```

3. **Query Flow**
   ```
   Healthcare Query → LLM Processing → Context Integration → Response
   ```



## Setup Guide

### 1. Install Ollama
1. Download and install Ollama from [https://ollama.com/](https://ollama.com/)
2. After installation, open command prompt and run:
```bash
ollama pull iodose/nuextract-v1.5
ollama pull mistral:7b
```
This will download the nuextract-v1.5 and mistral:7b model for Ollama for the extraction task.
3. Keep Ollama running in the background while using the application

### 2. Google Calendar Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials (API & Services > Crendentials)
5. Create Credentials, Create OAuth client ID, and select Web application
6. Add `http://localhost:8080/` to the Authorized redirect URIs
7. Download the credentials JSON file
8. Store this JSON credentials file in the root directory of this project
9. Rename the JSON file to `credentials.json`

## Requirements Installation

1. Clone this repository
2. Install the required packages using:
```bash
pip install -r requirements.txt
```
This should download all the dependencies for the running of this application.

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