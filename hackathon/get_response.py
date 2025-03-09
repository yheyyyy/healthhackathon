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
    # Load environment variables
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
        print(content)
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content)
        if match:
            return match.group(0)
        return "Error: No JSON content found"
    else:
        return f"Error at OpenRouter API: {response.status_code}, {response.text}"