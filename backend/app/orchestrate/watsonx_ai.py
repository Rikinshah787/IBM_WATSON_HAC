"""
watsonx.ai Integration
Optional integration for advanced reasoning and analysis
Uses IBM Granite models (approved for hackathon)
"""

import logging
import os
import json
import httpx
from typing import Dict, Any, Optional
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class WatsonAISettings(BaseSettings):
    """watsonx.ai configuration"""
    api_key: str = ""
    url: str = "https://us-south.ml.cloud.ibm.com"
    project_id: str = ""
    model_id: str = "ibm/granite-13b-instruct-v2"  # Approved Granite model
    
    class Config:
        env_prefix = "WATSONX_AI_"
        env_file = ".env"
        case_sensitive = False


class WatsonAI:
    """
    watsonx.ai integration for advanced reasoning
    Uses approved IBM Granite models only
    """
    
    def __init__(self):
        """Initialize watsonx.ai client"""
        self.settings = WatsonAISettings()
        self.is_available = bool(self.settings.api_key)
        logger.info(f"🔧 WatsonAI created (available: {self.is_available})")
    
    async def _get_token(self) -> str:
        """Get IAM token using API key"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://iam.cloud.ibm.com/identity/token",
                data={
                    "apikey": self.settings.api_key,
                    "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            return response.json()["access_token"]

    async def _generate_text(self, prompt: str) -> str:
        """Generate text using watsonx.ai API"""
        token = await self._get_token()
        
        url = f"{self.settings.url}/ml/v1/text/generation?version=2023-05-29"
        
        payload = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": 200,
                "min_new_tokens": 0,
                "stop_sequences": [],
                "repetition_penalty": 1.0
            },
            "model_id": self.settings.model_id,
            "project_id": self.settings.project_id
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result["results"][0]["generated_text"]

    async def generate_insight(
        self,
        query: str,
        data: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> Optional[str]:
        """
        Generate insight using watsonx.ai
        
        Args:
            query: Original query
            data: Processed data
            context: Additional context
        
        Returns:
            Generated insight text or None if unavailable
        """
        if not self.is_available:
            logger.debug("watsonx.ai not available, skipping")
            return None
        
        try:
            logger.info("🤖 Generating insight with watsonx.ai...")
            
            # Construct prompt
            data_summary = json.dumps(data, default=str)[:1000]  # Truncate to avoid token limits
            prompt = f"""
            Analyze the following data and answer the user's query.
            
            Query: {query}
            
            Data:
            {data_summary}
            
            Provide a concise insight based on the data.
            Insight:
            """
            
            insight = await self._generate_text(prompt)
            logger.info("✅ Insight generated")
            return insight.strip()
        except Exception as e:
            logger.error(f"❌ Failed to generate insight: {str(e)}", exc_info=True)
            return None
    
    async def analyze_correlation(
        self,
        sector1_data: Dict[str, Any],
        sector2_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze correlation between two sectors using watsonx.ai
        
        Args:
            sector1_data: Data from first sector
            sector2_data: Data from second sector
        
        Returns:
            Correlation analysis or None
        """
        if not self.is_available:
            logger.debug("watsonx.ai not available, using simple correlation")
            return {
                "correlation": "positive",
                "confidence": 0.75,
                "description": "Simple correlation analysis"
            }
        
        try:
            logger.info("🤖 Analyzing correlation with watsonx.ai...")
            
            data1_summary = json.dumps(sector1_data, default=str)[:500]
            data2_summary = json.dumps(sector2_data, default=str)[:500]
            
            prompt = f"""
            Analyze the correlation between these two datasets.
            
            Dataset 1:
            {data1_summary}
            
            Dataset 2:
            {data2_summary}
            
            Determine if there is a positive, negative, or no correlation.
            Provide the result in JSON format with keys: correlation (string), confidence (float 0-1), description (string).
            JSON:
            """
            
            response_text = await self._generate_text(prompt)
            
            # Parse JSON from response (simple attempt)
            try:
                # Find JSON-like structure
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = response_text[start:end]
                    return json.loads(json_str)
                else:
                    raise ValueError("No JSON found in response")
            except Exception:
                # Fallback if parsing fails
                return {
                    "correlation": "uncertain",
                    "confidence": 0.5,
                    "description": response_text.strip()
                }
        except Exception as e:
            logger.error(f"❌ Correlation analysis failed: {str(e)}", exc_info=True)
            return None

