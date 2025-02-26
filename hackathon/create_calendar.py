import json
import requests
import os
import re
import json
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from get_response import get_response

def extract_appointment_details(message):
    """
    Extracts appointment details from the given message and returns them in a JSON format.
    The function ensures the date is in the correct format and retries if there are any errors.
    Parameters:
    message (str): The message containing the appointment details.
    Returns:
    dict: The extracted appointment details in a JSON format.
    """
    json_format = """
    {
    "appointment": "",
    "location": "",
    "date": "DD MMM YYYY (example: 5 FEB 2024)",
    "time": "HH:MM AM/PM (example: 10:30 AM)",
    "description": ""
    }
    """
    prompt = f"""Extract the following text and return in a JSON format, no need for new line
    {message}
    Example JSON format:
    {json_format}
    """
    max_retries = 5
    retries = 0

    while retries < max_retries:
        try:
            response = get_response(prompt)
            appointment_details = json.loads(response)

            # Check if the date is in "DD MMM YYYY" format
            date_str = appointment_details.get("date", "")
            if not re.fullmatch(r"\d{1,2} [A-Za-z]{3} \d{4}", date_str):
                print("Date format does not match expected 'DD MMM YYYY' format, retrying...")
                print(date_str)
                retries += 1
                continue

            # Check for any error in the JSON response
            if "Error" in appointment_details:
                print("Error detected, retrying...")
                retries += 1
                continue

            return appointment_details

        except json.JSONDecodeError:
            print("JSONDecodeError detected, retrying...")
            retries += 1
        except Exception as e:
            print(f"An unexpected error occurred: {e}, retrying...")
            retries += 1

    print("Failed to extract appointment details after multiple attempts.")
    return None

def json_checker(json_data):
    """
    Checks if the JSON data contains the required keys and sets default values if needed.
    Parameters:
        json_data (dict): The JSON data to be checked.
    Returns:
        dict: The JSON data with default values set if needed
    """
    if json_data.get("appointment") is None:
        print("Using Default Appointment Name")
        json_data["appointment"] = "Health Appointment"
    return json_data

def get_google_calendar_service():
    """Authenticate and return a Google Calendar service instance."""
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None

    # Check if token.pickle exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    
    # If no valid credentials available, let the user log in
    if not creds or not creds.valid:
        # Use the downloaded OAuth credentials file
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )
        # Use port 8080 which matches the configured redirect URI
        creds = flow.run_local_server(port=8080)
        
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service

def build_event_body(event_details: dict, duration: int) -> dict:
    """Construct the event body required by the Google Calendar API.
    Parameters:
        event_details (dict): The details of the event to be created.
        duration (int): The duration of the event in hours.
    Returns:
        dict: The event body for the Google Calendar API.
    """
    # Use json_checker to set defaults as needed.
    event_details = json_checker(event_details)
    
    # Combine date and time, then convert to datetime objects.
    start_time_str = f"{event_details['date']} {event_details['time']}"
    start_time = datetime.strptime(start_time_str, "%d %b %Y %I:%M %p")
    end_time = start_time + timedelta(hours=duration)
    
    event_body = {
        "summary": event_details.get("appointment"),
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": event_details.get("timeZone", "Asia/Singapore"),
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": event_details.get("timeZone", "Asia/Singapore"),
        },
        "description": event_details.get("description") or "",
        "location": event_details.get("location") or "",
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 1440},
                {"method": "popup", "minutes": 10},
            ],
        },
    }
    return event_body

def create_calendar_event(event_details: dict, duration: int) -> None:
    """Creates an event on Google Calendar using provided details.
    Parameters:
        event_details (dict): The details of the event to be created.
        duration (int): The duration of the event in hours.
    Returns:
        None
    """
    service = get_google_calendar_service()
    event_body = build_event_body(event_details, duration)

    try:
        created_event = service.events().insert(calendarId="primary", body=event_body).execute()
        print("Event successfully created on Google Calendar!")
        print(f"View event online: {created_event.get('htmlLink')}\n")
    except Exception as e:
        print(f"Error creating event: {e}")
        
def main(message):
    appointment_details = extract_appointment_details(message)
    duration = 1
    create_calendar_event(appointment_details, duration)
    return appointment_details