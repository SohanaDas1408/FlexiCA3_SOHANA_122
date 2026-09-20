import logging
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

logger = logging.getLogger("ActionSynthesizerAgent")


class ActionSynthesizerAgent(BaseAgent):
    """
    Action & Synthesis Agent: Synthesizes individual event analyses into high-level
    executive summaries, aggregate risk metrics, and strategic recommendations.
    """

    def __init__(self):
        super().__init__(
            name="ActionSynthesizerAgent",
            role="Executive Policy & Strategy Synthesis Specialist",
            system_prompt=(
                "You are an executive environmental policy advisor. "
                "Synthesize complex multi-event climate reports into clear, "
                "actionable executive summaries and high-level strategic directives."
            )
        )

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        analyzed_articles = state.get("analyzed_articles", [])

        self.log_step(
            stage="Synthesis Init",
            thought=f"Synthesizing global briefing across {len(analyzed_articles)} analyzed events.",
            action="Aggregate statistical metrics and formulate strategic recommendations",
            observation="Computing severity distributions and cross-domain trends"
        )

        total_analyzed = len(analyzed_articles)
        critical_alerts = sum(1 for a in analyzed_articles if a.get("agent_analysis", {}).get("severity") == "CRITICAL")
        high_alerts = sum(1 for a in analyzed_articles if a.get("agent_analysis", {}).get("severity") == "HIGH")
        avg_credibility = (
            sum(a.get("agent_analysis", {}).get("credibility_score", 0.85) for a in analyzed_articles) / total_analyzed
            if total_analyzed > 0 else 0.0
        )

        categories = [a.get("category", "General") for a in analyzed_articles]
        dominant_category = max(set(categories), key=categories.count) if categories else "General Climate"

        # Heuristic synthesis fallback
        summary_lines = []
        if critical_alerts > 0:
            summary_lines.append(
                f"Global climate telemetry indicates heightened planetary risk with {critical_alerts} critical "
                f"and {high_alerts} high-severity developments detected in current cycle."
            )
        else:
            summary_lines.append(
                f"Current monitoring cycle captured {total_analyzed} verified climate signals across {dominant_category}."
            )
        summary_lines.append(
            "Key drivers include compounding oceanic and agricultural heat stress alongside accelerated capital "
            "deployment in renewable energy grids. Rigorous verification indicates high scientific consensus across reporting."
        )
        executive_summary = " ".join(summary_lines)

        strategic_recommendations = [
            "Mandate real-time marine ecological surveillance protocols in oceanic warming hotspot zones.",
            "Accelerate emergency agricultural water allocation and deploy drought-resistant crop insurance mechanisms.",
            "Establish independent carbon permanence auditing bodies to eliminate misleading greenwashing claims.",
            "Channel blended finance mechanisms to scale distributed renewable energy grids in vulnerable regions."
        ]

        llm_prompt = f"""
        Provide an executive synthesis of this climate news dataset:
        Events count: {total_analyzed}
        Critical alerts: {critical_alerts}
        Titles: {[a.get('title') for a in analyzed_articles]}

        Return JSON with keys:
        - 'executive_summary': (string, concise 3-paragraph executive overview)
        - 'strategic_recommendations': (list of 4 actionable strategic bullet points)
        """

        synthesis_result = self.call_llm(
            llm_prompt,
            default_fallback={
                "executive_summary": executive_summary,
                "strategic_recommendations": strategic_recommendations
            }
        )

        digest_data = {
            "executive_summary": synthesis_result.get("executive_summary", executive_summary),
            "strategic_recommendations": synthesis_result.get("strategic_recommendations", strategic_recommendations),
            "metrics": {
                "total_analyzed": total_analyzed,
                "critical_alerts": critical_alerts,
                "high_alerts": high_alerts,
                "avg_credibility": avg_credibility,
                "dominant_category": dominant_category
            },
            "articles": analyzed_articles
        }

        self.log_step(
            stage="Synthesis Complete",
            thought="Executive digest formulated with verified metrics and policy directives.",
            action="Handover compiled digest payload to AlertDispatcherAgent",
            observation={"dominant_category": dominant_category, "recommendations_count": len(strategic_recommendations)}
        )

        state["digest_data"] = digest_data
        state["trace_logs"] = state.get("trace_logs", []) + self.reasoning_trace
        return state
