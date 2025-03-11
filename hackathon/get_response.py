import os 
import requests
import re
from dotenv import load_dotenv



def get_response(prompt):
    """
    Get response from OpenRouter API using the specified model.
    
    Parameters:
    prompt (str): The prompt to generate response.
    
    Returns:
    str: The generated response.
    """
    load_dotenv()
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }
    
    data = {
        "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        content = response_data["choices"][0]["message"]["content"]
        print(f"content", content)
        return content
    else:
        return f"Error at OpenRouter API: {response.status_code}, {response.text}"
    
if __name__ == "__main__":
    message = """Extract the following text and return in one single JSON format, no need for new line
    Dear Ms. DIANE, You have a First Visit Consultation at ENT-Head & Neck Surg Ctr - 15C, NUH Medical Centre, Zone B, Level 15, 15c, Lift Lobby B2 on 19 Mar 2025 at 3:45 pm
    Example JSON Format:
    {
    "appointment":
    "location": 
    "date": DD MMM YYYY (example: 5 FEB 2024)
    "time": HH:MM AM/PM (example: 10:30 AM)
    "description": 
    }
    """
    text = get_response(message)
    print(text)