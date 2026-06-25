import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# -----------------------------
# Config
# -----------------------------
FALLBACK_TEXT = "LLM generation unavailable. Using collected research data."

# Cerebras model: fast + good enough for research synthesis
CEREBRAS_MODEL = os.getenv("CEREBRAS_MODEL", "gpt-oss-120b")

# OpenRouter model: choose a cheap/free model for backup
# You can change this later if needed
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct")

# -----------------------------
# Clients
# -----------------------------
cerebras_client = None
if CEREBRAS_API_KEY:
    try:
        cerebras_client = OpenAI(
            api_key=CEREBRAS_API_KEY,
            base_url="https://api.cerebras.ai/v1",
        )
    except Exception as e:
        print("Cerebras init error:", e)

openrouter_client = None
if OPENROUTER_API_KEY:
    try:
        openrouter_client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
    except Exception as e:
        print("OpenRouter init error:", e)


# -----------------------------
# Helpers
# -----------------------------
def _extract_text(response) -> str:
    """
    Extract assistant text safely from OpenAI-compatible response.
    """
    try:
        if response and response.choices and response.choices[0].message:
            content = response.choices[0].message.content
            if isinstance(content, str):
                return content.strip()

            # sometimes content may come as list-like blocks
            if isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, dict):
                        text = item.get("text")
                        if text:
                            parts.append(text)
                joined = "\n".join(parts).strip()
                if joined:
                    return joined
    except Exception:
        pass

    raise ValueError("Empty or invalid LLM response")


def _should_retry(error_text: str) -> bool:
    lowered = error_text.lower()
    retry_terms = [
        "429",
        "rate limit",
        "quota",
        "temporarily unavailable",
        "timeout",
        "connection reset",
        "server error",
        "502",
        "503",
        "504",
    ]
    return any(term in lowered for term in retry_terms)


# -----------------------------
# Provider 1: Cerebras
# -----------------------------
def cerebras_generate(prompt: str, max_retries: int = 2) -> str:
    if cerebras_client is None:
        raise ValueError("Cerebras client not configured")

    last_error = None

    for attempt in range(max_retries):
        try:
            response = cerebras_client.chat.completions.create(
                model=CEREBRAS_MODEL,
                messages=[
                    {"role": "system", "content": "You are a precise research analyst."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            return _extract_text(response)

        except Exception as e:
            last_error = e
            err_text = str(e)

            if _should_retry(err_text) and attempt < max_retries - 1:
                wait_time = 3 * (attempt + 1)
                print(f"Cerebras retry {attempt+1}/{max_retries} in {wait_time}s...")
                time.sleep(wait_time)
                continue

            raise e

    raise last_error


# -----------------------------
# Provider 2: OpenRouter
# -----------------------------
def openrouter_generate(prompt: str, max_retries: int = 2) -> str:
    if openrouter_client is None:
        raise ValueError("OpenRouter client not configured")

    last_error = None

    for attempt in range(max_retries):
        try:
            response = openrouter_client.chat.completions.create(
                model=OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": "You are a precise research analyst."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                extra_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "ResearchOS",
                },
            )
            return _extract_text(response)

        except Exception as e:
            last_error = e
            err_text = str(e)

            if _should_retry(err_text) and attempt < max_retries - 1:
                wait_time = 3 * (attempt + 1)
                print(f"OpenRouter retry {attempt+1}/{max_retries} in {wait_time}s...")
                time.sleep(wait_time)
                continue

            raise e

    raise last_error


# -----------------------------
# Safe generation entrypoint
# -----------------------------
def safe_generate(prompt: str) -> str:
    """
    Order:
    1) Cerebras
    2) OpenRouter
    3) Deterministic fallback text
    """

    # 1) Cerebras first
    if cerebras_client is not None:
        try:
            return cerebras_generate(prompt)
        except Exception as e:
            print(f"Cerebras Error: {e}")

    # 2) OpenRouter fallback
    if openrouter_client is not None:
        try:
            return openrouter_generate(prompt)
        except Exception as e:
            print(f"OpenRouter Error: {e}")

    # 3) Final fallback
    return FALLBACK_TEXT