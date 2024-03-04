import os
import dotenv

f = dotenv.find_dotenv()
if not f:
    f = dotenv.find_dotenv('template.env')
dotenv.load_dotenv(f)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

MEMGRAPH_HOST = os.environ.get("MEMGRAPH_HOST", "127.0.0.1")
MEMGRAPH_PORT = os.environ.get("MEMGRAPH_PORT", "7687")
MEMGRAPH_PORT = int(MEMGRAPH_PORT)

CHROMA_DATA_DIR = os.environ.get("CHROMA_DATA_DIR")
CHROMA_VECTOR_SPACE = os.environ.get("CHROMA_VECTOR_SPACE")

EMBEDDING_MODEL_NAME = os.environ.get(
    "EMBEDDING_MODEL_NAME", "text-embedding-ada-002")
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "gpt-4")
LLM_MODEL_TEMPERATURE = os.environ.get("LLM_MODEL_TEMPERATURE", "0.2")
LLM_MODEL_TEMPERATURE = float(LLM_MODEL_TEMPERATURE)

MOCK = (os.environ.get("MOCK", 'False') == 'True')
