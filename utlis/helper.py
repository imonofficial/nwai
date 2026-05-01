import logging

# Configure basic logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def dummy_ml_predict(input_text: str) -> dict:
    """
    A dummy machine learning prediction function.
    In a real scenario, this would load a model and perform inference.
    """
    logger.info(f"Processing input text: {input_text[:50]}...")
    
    # Simulate text processing/summarization logic
    word_count = len(input_text.split())
    summary = f"Summary of {word_count} words: " + input_text[:50] + ("..." if len(input_text) > 50 else "")
    
    # Mock confidence score
    confidence = 0.95 if word_count > 5 else 0.50
    
    return {
        "summary": summary,
        "word_count": word_count,
        "confidence": confidence,
        "model_version": "dummy-v1"
    }
