import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- API Keys & Custom Endpoints ---
OPENAI_API_KEY = os.getenv("LAB_API_KEY") or os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("LAB_BASE_URL") or os.getenv("OPENAI_BASE_URL", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")  # Optional: for HuggingFace models

if OPENAI_BASE_URL:
    os.environ["OPENAI_BASE_URL"] = OPENAI_BASE_URL
if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# --- Qdrant (same as Day 18) ---
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "company_knowledge_base"

# --- Search (same as Day 18) ---
BM25_TOP_K = 20
DENSE_TOP_K = 20
HYBRID_TOP_K = 20
RERANK_TOP_K = 3

# --- Paths ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
FIXTURES_DIR = os.path.join(ROOT_DIR, "fixtures")
ARTIFACTS_DIR = os.path.join(ROOT_DIR, "artifacts")
REPORTS_DIR = os.path.join(ROOT_DIR, "doc", "reports")

TEST_SET_PATH = os.path.join(FIXTURES_DIR, "test_set_50q.json")
ANSWERS_PATH = os.path.join(ARTIFACTS_DIR, "answers_50q.json")
HUMAN_LABELS_PATH = os.path.join(FIXTURES_DIR, "human_labels_10q.json")
ADVERSARIAL_SET_PATH = os.path.join(FIXTURES_DIR, "adversarial_set_20.json")
CLEAN_SET_PATH = os.path.join(FIXTURES_DIR, "clean_set_8.json")
OUTPUT_SET_PATH = os.path.join(FIXTURES_DIR, "output_set_4.json")
GUARDRAILS_CONFIG_DIR = os.path.join(ROOT_DIR, "guardrails")
PAIR_QUESTION_IDS = (1, 5, 12, 21, 41)

# --- LLM Models ---
MODEL_NAME = os.getenv("LAB_MODEL", "deepseek-v4.1-flash")
GENERATION_MODEL = os.getenv("LAB_MODEL") or os.getenv("GENERATION_MODEL", MODEL_NAME)
JUDGE_MODEL = os.getenv("JUDGE_MODEL", GENERATION_MODEL)
EVALUATOR_MODEL = os.getenv("EVALUATOR_MODEL", JUDGE_MODEL)


def openai_client():
    """Create a client for OpenAI or an OpenAI-compatible provider."""
    from openai import OpenAI

    kwargs = {}
    if OPENAI_API_KEY:
        kwargs["api_key"] = OPENAI_API_KEY
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
    return OpenAI(**kwargs)

# --- Guardrail latency budget ---
LATENCY_BUDGET_P95_MS = 500  # Full guard target; Task 12 currently measures input guards only.
PRESIDIO_LANGUAGE = "en"
