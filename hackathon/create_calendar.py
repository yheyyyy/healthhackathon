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
    json_format = """
    {
    "appointment":
    "location": 
    "date": DD MMM YYYY (example: 5 FEB 2024)
    "time": 
    "description": 
    }
    """
    prompt = f"""Extract the following text and return in a JSON format, no need for new line
    {message}

    Example JSON format:
    {json_format}
    """
    while True:
        try:
            response = get_response(prompt)
            appointment_details = json.loads(response)
            
            # Check if the date is in "DD MMM YYYY" format
            date_str = appointment_details.get("date", "")
            if not re.fullmatch(r"\d{1,2} [A-Za-z]{3} \d{4}", date_str):
                print("Date format does not match expected 'DD MMM YYYY' format, retrying...")
                continue

            # Check for any error in the JSON response
            if "Error" in appointment_details:
                print("Error detected, retrying...")
                continue
            else:
                break
        except json.JSONDecodeError:
            print("JSONDecodeError detected, retrying...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}, retrying...")
    return appointment_details

def json_checker(json_data):
    if json_data.get("appointment") is None:
        print("Using Default Appointment Name")
        json_data["appointment"] = "Health Appointment"
    return json_data

def get_google_calendar_service():
    """Authenticate and return a Google Calendar service instance."""
    load_dotenv()
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
                "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
                "redirect_uris": ["http://localhost"],
            }
        },
        SCOPES,
    )

    if os.path.exists("token.pickle"):
        credentials = pickle.load(open("token.pickle", "rb"))
    else:
        credentials = flow.run_local_server(port=8080)
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    service = build("calendar", "v3", credentials=credentials)
    return service

def build_event_body(event_details: dict, duration: int) -> dict:
    """Construct the event body required by the Google Calendar API."""
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
    """Creates an event on Google Calendar using provided details."""
    service = get_google_calendar_service()
    event_body = build_event_body(event_details, duration)

    try:
        created_event = service.events().insert(calendarId="primary", body=event_body).execute()
        print("\n\033[92mEvent successfully created on Google Calendar!\033[0m")
        print(f"View event online: {created_event.get('htmlLink')}\n")
    except Exception as e:
        print(f"Error creating event: {e}")
        
def main(message):
    appointment_details = extract_appointment_details(message)
    duration =1
    create_calendar_event(appointment_details, duration)
    return appointment_details


