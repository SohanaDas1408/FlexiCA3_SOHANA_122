import time
import logging
from typing import Dict, Any, Callable, Optional, List
from agents.scout_agent import NewsScoutAgent
from agents.fact_checker_agent import FactCheckerAgent
from agents.impact_analyst_agent import ImpactAnalystAgent
from agents.synthesizer_agent import ActionSynthesizerAgent
from agents.dispatcher_agent import AlertDispatcherAgent

logger = logging.getLogger("ClimateAgentOrchestrator")


class ClimateAgentOrchestrator:
    """
    Multi-Agent Workflow Coordinator: Orchestrates sequential and state-driven
    agent execution, capturing end-to-end cognitive telemetry and state transitions.
    """

    def __init__(self):
        self.scout = NewsScoutAgent()
        self.fact_checker = FactCheckerAgent()
        self.impact_analyst = ImpactAnalystAgent()
        self.synthesizer = ActionSynthesizerAgent()
        self.dispatcher = AlertDispatcherAgent()

    def run_pipeline(
        self,
        use_live_rss: bool = True,
        custom_topic: str = "",
        feed_limit: int = 2,
        sample_limit: int = 4,
        progress_callback: Optional[Callable[[str, int, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Executes the autonomous multi-agent monitoring pipeline.
        
        Args:
            use_live_rss: Whether to fetch live RSS or use offline curated dataset.
            custom_topic: Optional specific real-time topic/keyword to search dynamically.
            feed_limit: Limit of articles fetched per RSS feed.
            sample_limit: Limit of articles loaded in sample mode.
            progress_callback: Callback function(agent_name, step_pct, status_msg).
        """
        start_time = time.time()
        state: Dict[str, Any] = {
            "use_live_rss": use_live_rss,
            "custom_topic": custom_topic,
            "feed_limit": feed_limit,
            "sample_limit": sample_limit,
            "trace_logs": [],
            "execution_metadata": {}
        }

        agents_pipeline = [
            ("NewsScoutAgent", 20, "Perception: Discovering and extracting climate signals...", self.scout),
            ("FactCheckerAgent", 40, "Verification: Auditing source credibility and IPCC consensus...", self.fact_checker),
            ("ImpactAnalystAgent", 60, "Cognition: Modeling severity index, sentiment, and regional risk...", self.impact_analyst),
            ("ActionSynthesizerAgent", 80, "Synthesis: Formulating executive digest and strategic policy directives...", self.synthesizer),
            ("AlertDispatcherAgent", 100, "Automation: Generating PDF digests and dispatching emergency alerts...", self.dispatcher),
        ]

        for agent_name, pct, msg, agent_instance in agents_pipeline:
            logger.info(f"===> Orchestrator starting phase: {agent_name} ({pct}%)")
            if progress_callback:
                progress_callback(agent_name, pct, msg)

            state = agent_instance.execute(state)
            time.sleep(0.3)  # Smooth transition for real-time visualization

        duration = round(time.time() - start_time, 2)
        state["execution_metadata"] = {
            "total_execution_seconds": duration,
            "agents_executed": len(agents_pipeline),
            "status": "COMPLETED_SUCCESSFULLY"
        }

        logger.info(f"Pipeline finished successfully in {duration}s")
        return state
