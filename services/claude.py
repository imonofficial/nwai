import anthropic
import logging
from config import CLAUDE_API_KEY

logger = logging.getLogger(__name__)

# Initialize Anthropics client if API key is present
if CLAUDE_API_KEY:
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
else:
    client = None
    logger.warning("CLAUDE_API_KEY is not set. Claude AI integration will fail.")

def generate_claude_response(prompt: str) -> str:
    """
    Sends the prompt to Claude API and returns the generated text.
    """
    if not client:
        return "Error: Claude API key is missing from configuration."
    
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Fast and cost-effective model suitable for chat
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Claude API error: {str(e)}")
        return "I'm sorry, I encountered an error while processing your request via Claude API."
