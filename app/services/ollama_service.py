import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()  

OLLAMA_URL = os.getenv("OLLAMA_URL")

logging.basicConfig(level=logging.INFO)

def generate_startup_idea(preferences, categories):
    logging.info("Selected categories: %s", categories)
    category_text = ", ".join(categories) if categories else "General"
    
    if not categories:
        logging.warning("No categories provided. Using default: General")
    else:
        extra_instruction = f" The startup idea must be strictly limited to the domain of {category_text}."
    
    prompt = (
        f"Generate a startup idea strictly in the field of {category_text}. "
        f"The idea should be exclusively related to {category_text} and must address the following preferences: {preferences}. "
        f"Ensure that the idea is focused only on {category_text} and does not include unrelated elements."
    )
    if categories:
        prompt += extra_instruction
    
    logging.info("Final Prompt Sent to Ollama: %s", prompt)
    
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
    logging.info("Sending request to Ollama with payload: %s", payload)
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        logging.info("Received response with status code: %d", response.status_code)
        response.raise_for_status()
        response_data = response.json()
        logging.info("Ollama Response: %s", response_data)
        
        idea = response_data.get("response", None)
        if idea:
            return idea
        else:
            logging.error("No 'response' field in Ollama API response: %s", response_data)
            return "Error: No valid response from Ollama API"
    except requests.exceptions.Timeout:
        logging.error("Request to Ollama API timed out")
        return "Error: Request to Ollama API timed out"
    except requests.exceptions.RequestException as e:
        logging.error("Error connecting to Ollama: %s", e)
        return f"Error: {e}"
