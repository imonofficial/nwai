import requests
import logging
from config import HUGGINGFACE_API_KEY

logger = logging.getLogger(__name__)

# Hugging Face Inference API details
# Using a fast instruction-following model
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

def generate_huggingface_response(prompt: str) -> str:
    """
    Sends the prompt to Hugging Face Inference API and returns the generated text.
    """
    if not HUGGINGFACE_API_KEY:
        return "Error: Hugging Face API key is missing from configuration."

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    
    # Format prompt for instruction model
    formatted_prompt = f"[INST] {prompt} [/INST]"
    
    payload = {
        "inputs": formatted_prompt,
        "parameters": {
            "max_new_tokens": 500,
            "return_full_text": False,
            "temperature": 0.7,
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"].strip()
            return "Received unexpected response format from Hugging Face."
        else:
            logger.error(f"Hugging Face API returned status {response.status_code}: {response.text}")
            return f"Error from Hugging Face API (Status {response.status_code})."
            
    except requests.exceptions.Timeout:
        logger.error("Hugging Face API request timed out.")
        return "I'm sorry, the Hugging Face API request timed out."
    except Exception as e:
        logger.error(f"Hugging Face API error: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request via Hugging Face API."
