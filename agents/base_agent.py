import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from config import GROQ_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_GROQ_MODEL

logger = logging.getLogger("BaseAgent")


class BaseAgent(ABC):
    """
    Abstract Base Agent implementing the Cognitive Thought-Action-Observation
    paradigm with Groq, Gemini, OpenAI, and heuristic execution engines.
    """

    def __init__(self, name: str, role: str, system_prompt: str, custom_groq_key: Optional[str] = None):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.reasoning_trace: List[Dict[str, Any]] = []
        self.groq_key = custom_groq_key or GROQ_API_KEY
        self._init_llm()

    def _init_llm(self):
        self.llm_provider = "none"

        # 1. Prioritize Ultra-Fast Groq Engine
        if self.groq_key and len(self.groq_key.strip()) > 8:
            try:
                import groq
                self.groq_client = groq.Groq(api_key=self.groq_key.strip())
                self.llm_provider = "groq"
                logger.info(f"[{self.name}] Initialized Groq LLM Engine successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq: {e}")

        # 2. Fallback to Gemini
        if self.llm_provider == "none" and GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                self.gemini_model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=self.system_prompt
                )
                self.llm_provider = "gemini"
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini: {e}")

        # 3. Fallback to OpenAI
        if self.llm_provider == "none" and OPENAI_API_KEY:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
                self.llm_provider = "openai"
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")

    def log_step(self, stage: str, thought: str, action: str, observation: Any):
        """
        Records the cognitive trace of the agent's internal deliberation.
        """
        trace_entry = {
            "agent": self.name,
            "role": self.role,
            "stage": stage,
            "thought": thought,
            "action": action,
            "observation": observation
        }
        self.reasoning_trace.append(trace_entry)
        logger.info(f"[{self.name}] [{stage}] Thought: {thought} | Action: {action}")

    def call_llm(
        self,
        prompt: str,
        default_fallback: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes an ultra-fast LLM call (Groq/Gemini/OpenAI) or reverts to
        the intelligent deterministic reasoning fallback engine.
        """
        if self.llm_provider == "groq":
            try:
                target_model = model or DEFAULT_GROQ_MODEL
                response = self.groq_client.chat.completions.create(
                    model=target_model,
                    messages=[
                        {"role": "system", "content": self.system_prompt + "\nYou MUST return strictly valid JSON. Do not include markdown wraps or conversational filler."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                raw_text = response.choices[0].message.content.strip()
                return json.loads(raw_text)
            except Exception as e:
                logger.warning(f"[{self.name}] Groq API call failed or non-JSON: {e}")

        elif self.llm_provider == "gemini":
            try:
                response = self.gemini_model.generate_content(prompt)
                text = response.text.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                return json.loads(text)
            except Exception as e:
                logger.warning(f"Gemini LLM call failed: {e}")

        elif self.llm_provider == "openai":
            try:
                response = self.openai_client.chat.completions.create(
                    model=model or "gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": self.system_prompt + " Reply strictly with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                logger.warning(f"OpenAI LLM call failed: {e}")

        return default_fallback or {}

    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Core task execution logic for the agent.
        """
        pass

