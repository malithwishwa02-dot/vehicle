"""
AUTONOMOUS CORTEX: Intelligence Core
Real-time AI decision-making via OpenAI (or compatible APIs).
Analyzes raw data and provides strategic recommendations.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
import asyncio

class IntelligenceCore:
    """
    AI-powered decision engine for autonomous operations.
    Interfaces with OpenAI API to analyze targets and generate strategies.
    """
    
    # Configuration constants
    MAX_CONTENT_SAMPLE_LENGTH = 2000  # Maximum content length to send to AI
    
    def __init__(self, logger: logging.Logger = None):
        """
        Initialize Intelligence Core with OpenAI client.
        """
        self.logger = logger or logging.getLogger("IntelligenceCore")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.client = None
        
        if self.api_key:
            try:
                # Lazy import to avoid dependency if not needed
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
                self.logger.info(f"[INTELLIGENCE] Core online - Model: {self.model}")
            except ImportError:
                self.logger.warning("[INTELLIGENCE] openai package not installed - running in fallback mode")
            except Exception as e:
                self.logger.warning(f"[INTELLIGENCE] Failed to initialize OpenAI client: {e}")
        else:
            self.logger.warning("[INTELLIGENCE] OPENAI_API_KEY not set - running in fallback mode")
    
    async def analyze_target(self, url: str, raw_data: str) -> Dict[str, Any]:
        """
        Analyze target URL and raw data to generate strategic recommendations.
        
        Args:
            url: Target URL being analyzed
            raw_data: Raw HTML/content from the target
            
        Returns:
            Strategy dictionary with recommendations
        """
        if not self.client:
            return self._fallback_strategy(url, raw_data)
        
        try:
            # Truncate raw_data to avoid token limits
            data_sample = raw_data[:self.MAX_CONTENT_SAMPLE_LENGTH] if raw_data else "No data available"
            
            # Construct analysis prompt
            prompt = f"""You are an autonomous browser fingerprinting strategist analyzing a target website.

Target URL: {url}
Sample Content: {data_sample}

Based on this target, provide strategic recommendations in JSON format:
{{
    "recommended_age_days": <integer 30-180>,
    "trust_level": <string "high"|"medium"|"low">,
    "strategy_notes": <string brief explanation>,
    "risk_assessment": <string "minimal"|"moderate"|"elevated">
}}

Consider:
- E-commerce sites typically require older profiles (90-180 days)
- Financial sites require maximum trust (150-180 days)
- General content sites can use moderate aging (60-90 days)
- New/unknown sites should use conservative approach (120+ days)

Respond ONLY with valid JSON, no additional text."""

            # Call OpenAI API
            self.logger.info(f"[INTELLIGENCE] Analyzing target: {url}")
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a security-focused web analysis expert. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=500
                ),
                timeout=30.0
            )
            
            # Parse AI response
            content = response.choices[0].message.content.strip()
            
            # Handle potential markdown code blocks
            if content.startswith("```"):
                # Extract JSON from markdown code block (more robust parsing)
                lines = content.split("\n")
                if len(lines) > 2:
                    # Remove first and last lines (markdown delimiters)
                    content = "\n".join(lines[1:-1])
                # If only 2 lines or less, try to extract content
                elif len(lines) == 2:
                    content = lines[1] if lines[1] else "{}"
                else:
                    content = "{}"
            
            strategy = json.loads(content)
            
            # Validate required fields
            if "recommended_age_days" not in strategy:
                self.logger.warning("[INTELLIGENCE] Missing recommended_age_days, using fallback")
                return self._fallback_strategy(url, raw_data)
            
            self.logger.info(f"[INTELLIGENCE] Analysis complete - Recommended age: {strategy.get('recommended_age_days')} days")
            return strategy
            
        except asyncio.TimeoutError:
            self.logger.error("[INTELLIGENCE] API timeout - using fallback strategy")
            return self._fallback_strategy(url, raw_data)
        except json.JSONDecodeError as e:
            self.logger.error(f"[INTELLIGENCE] Failed to parse AI response: {e}")
            return self._fallback_strategy(url, raw_data)
        except Exception as e:
            self.logger.error(f"[INTELLIGENCE] Analysis failed: {e}")
            return self._fallback_strategy(url, raw_data)
    
    def _fallback_strategy(self, url: str, raw_data: str) -> Dict[str, Any]:
        """
        Fallback strategy when AI is unavailable.
        Uses heuristic-based analysis.
        
        Args:
            url: Target URL
            raw_data: Raw content
            
        Returns:
            Default strategy dictionary
        """
        # Simple heuristic: Check URL for known patterns
        url_lower = url.lower()
        
        if any(domain in url_lower for domain in ["bank", "paypal", "stripe", "financial"]):
            age_days = 180
            trust_level = "high"
            risk = "minimal"
        elif any(domain in url_lower for domain in ["amazon", "ebay", "shopify", "store", "shop"]):
            age_days = 120
            trust_level = "high"
            risk = "minimal"
        elif any(domain in url_lower for domain in ["google", "microsoft", "apple", "facebook"]):
            age_days = 90
            trust_level = "medium"
            risk = "moderate"
        else:
            age_days = 120
            trust_level = "medium"
            risk = "moderate"
        
        self.logger.info(f"[INTELLIGENCE] Using fallback strategy - Age: {age_days} days")
        
        return {
            "recommended_age_days": age_days,
            "trust_level": trust_level,
            "strategy_notes": "Fallback heuristic analysis (AI unavailable)",
            "risk_assessment": risk,
            "fallback_mode": True
        }
    
    async def health_check(self) -> bool:
        """
        Verify Intelligence Core is operational.
        
        Returns:
            True if AI is available, False if in fallback mode
        """
        if not self.client:
            self.logger.warning("[INTELLIGENCE] Running in fallback mode")
            return False
        
        try:
            # Simple API test
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5
                ),
                timeout=10.0
            )
            self.logger.info("[INTELLIGENCE] Health check passed")
            return True
        except Exception as e:
            self.logger.warning(f"[INTELLIGENCE] Health check failed: {e}")
            return False
