import os
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set constants for LangChain from environment variables
class Constants:
    LLM_MODEL_TEMPERATURE = float(os.getenv("LLM_MODEL_TEMPERATURE"))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

