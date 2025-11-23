# watsonx_client.py
import os
import json
import logging
from typing import Dict, Any, Optional
import httpx
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class WatsonXSettings(BaseSettings):
    WATSONX_AI_API_KEY: str = ""
    WATSONX_AI_URL: str = "https://us-south.ml.cloud.ibm.com"
    WATSONX_AI_PROJECT_ID: str = ""
    WATSONX_AI_MODEL_ID: str = "ibm/granite-13b-instruct-v2"
    WATSONX_API_VERSION: str = "2024-05-31"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

class WatsonXClient:
    def __init__(self, settings: Optional[WatsonXSettings] = None):
        self.settings = settings or WatsonXSettings()
        self.available = bool(self.settings.WATSONX_AI_API_KEY and self.settings.WATSONX_AI_PROJECT_ID)
        self._token: Optional[str] = None
        logger.info("WatsonXClient initialized (available=%s)", self.available)

    async def _get_iam_token(self) -> str:
        if self._token:
            return self._token
        url = "https://iam.cloud.ibm.com/identity/token"
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.settings.WATSONX_AI_API_KEY
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient(timeout=30.0) as client:
            r = await client.post(url, data=data, headers=headers)
            r.raise_for_status()
            body = r.json()
            token = body.get("access_token")
            if not token:
                raise RuntimeError("no access_token in IAM response")
            self._token = token
            return token

    async def generate_text(self, prompt: str, max_new_tokens: int = 200) -> str:
        if not self.available:
            raise RuntimeError("WatsonXClient not configured (missing API key or project id)")
        token = await self._get_iam_token()
        endpoint = f"{self.settings.WATSONX_AI_URL.rstrip('/')}/ml/v1/text/generation"
        params = {"version": self.settings.WATSONX_API_VERSION}
        payload = {
            "input": prompt,
            "model_id": self.settings.WATSONX_AI_MODEL_ID,
            "project_id": self.settings.WATSONX_AI_PROJECT_ID,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "decoding_method": "greedy"
            }
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            r = await client.post(endpoint, params=params, json=payload, headers=headers)
            r.raise_for_status()
            body = r.json()
            # typical response: {"results":[{"generated_text":"..."}], ...}
            if isinstance(body, dict):
                results = body.get("results") or []
                if results and isinstance(results, list) and "generated_text" in results[0]:
                    return results[0]["generated_text"]
            # fallback: attempt to join any text fields
            return json.dumps(body)

    async def generate_insight(self, query: str, data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        if not self.available:
            logger.debug("WatsonX not available, skipping")
            return None
        try:
            data_summary = json.dumps(data, default=str)[:2000]
            ctx = f"\nContext: {json.dumps(context, default=str)}\n" if context else ""
            prompt = (
                "Analyze the following data and answer the user's query concisely.\n\n"
                f"Query: {query}\n\n"
                f"Data: {data_summary}\n\n"
                f"{ctx}\nProvide a short, actionable insight:\n"
            )
            return (await self.generate_text(prompt)).strip()
        except Exception as exc:
            logger.exception("generate_insight failed: %s", exc)
            return None

    async def recognize_intent(self, query: str, sectors: list) -> Optional[Dict[str, Any]]:
        """
        Recognize intent using WatsonX AI
        """
        if not self.available:
            return None
            
        try:
            prompt = (
                "You are an AI assistant for a business dashboard. Analyze the query and identify the intent and relevant sectors.\n"
                "Available intents: analyze_attrition, correlate_satisfaction_sales, analyze_pipeline, identify_blocking_tickets, "
                "predict_escalations, analyze_complaint_impact, auto_approve_invoices, analyze_budget_hiring, general_query\n\n"
                f"Query: {query}\n\n"
                "Return ONLY a JSON object with keys: 'intent' (string) and 'sectors' (list of strings).\n"
                "Example: {\"intent\": \"analyze_attrition\", \"sectors\": [\"hr\"]}\n\n"
                "JSON:"
            )
            
            response_text = await self.generate_text(prompt, max_new_tokens=100)
            
            # Extract JSON
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(response_text[start:end])
            
            return None
        except Exception as e:
            logger.error(f"Watson intent recognition failed: {e}")
            return None

    async def analyze_correlation(self, a: Dict[str, Any], b: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.available:
            logger.debug("WatsonX not available, returning fallback")
            return {"correlation": "unknown", "confidence": 0.5, "description": "fallback analysis"}
        try:
            prompt = (
                "Given the two datasets below, determine whether correlation is positive, negative, or none. "
                "Return a JSON object with keys: correlation (string), confidence (0-1 float), description (string).\n\n"
                "Dataset A:\n" + json.dumps(a, default=str)[:1000] + "\n\n"
                "Dataset B:\n" + json.dumps(b, default=str)[:1000] + "\n\nJSON:"
            )
            resp = await self.generate_text(prompt, max_new_tokens=300)
            # try to extract JSON substring
            start = resp.find("{")
            end = resp.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(resp[start:end])
            # fallback: return text as description
            return {"correlation": "uncertain", "confidence": 0.5, "description": resp.strip()}
        except Exception:
            logger.exception("analyze_correlation failed")
            return None
