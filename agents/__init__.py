"""
Agents package for Climate Change News Monitoring Multi-Agent System.
"""
from .base_agent import BaseAgent
from .scout_agent import NewsScoutAgent
from .fact_checker_agent import FactCheckerAgent
from .impact_analyst_agent import ImpactAnalystAgent
from .synthesizer_agent import ActionSynthesizerAgent
from .dispatcher_agent import AlertDispatcherAgent
from .orchestrator import ClimateAgentOrchestrator

__all__ = [
    "BaseAgent",
    "NewsScoutAgent",
    "FactCheckerAgent",
    "ImpactAnalystAgent",
    "ActionSynthesizerAgent",
    "AlertDispatcherAgent",
    "ClimateAgentOrchestrator"
]
