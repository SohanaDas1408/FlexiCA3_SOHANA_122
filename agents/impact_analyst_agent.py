import logging
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

logger = logging.getLogger("ImpactAnalystAgent")


class ImpactAnalystAgent(BaseAgent):
    """
    Climate Impact & Sentiment Agent: Computes severity scores, geographical exposure,
    socioeconomic implications, and climate sentiment dimensions.
    """

    def __init__(self):
        super().__init__(
            name="ImpactAnalystAgent",
            role="Climate Risk & Impact Assessment Specialist",
            system_prompt=(
                "You are an environmental risk analyst. Evaluate the severity, "
                "geographic exposure, and socioeconomic disruption of reported climate events. "
                "Provide risk categorization and severity scoring."
            )
        )

    def _heuristic_analysis(self, title: str, content: str) -> Dict[str, Any]:
        combined = f"{title} {content}".lower()

        # Severity indicators
        critical_keywords = ["catastrophic", "record high", "unprecedented", "bleaching", "drought", "emergency", "fatalities", "disaster"]
        high_keywords = ["surge", "threaten", "deficit", "depleted", "loss", "warning", "accelerating"]
        solution_keywords = ["renewable", "solar", "wind", "deployment", "agreement", "investment", "innovation", "clean energy"]

        crit_count = sum(1 for kw in critical_keywords if kw in combined)
        high_count = sum(1 for kw in high_keywords if kw in combined)
        sol_count = sum(1 for kw in solution_keywords if kw in combined)

        if sol_count >= 2 and crit_count == 0:
            severity = "LOW"
            severity_score = 0.25
            sentiment = "Positive / Progressive Solution"
            impact_desc = "Advancement in clean energy infrastructure and decarbonization pathways."
            action_rec = "Accelerate capital allocation into grid modernization and renewable scaling."
        elif crit_count >= 2 or ("record" in combined and "high" in combined):
            severity = "CRITICAL"
            severity_score = 0.88
            sentiment = "High Alarm / Urgent Concern"
            impact_desc = "Extreme environmental stress with immediate systemic risk to ecosystems and communities."
            action_rec = "Trigger rapid response protocols, emergency adaptation funding, and continuous sensor monitoring."
        elif crit_count >= 1 or high_count >= 2:
            severity = "HIGH"
            severity_score = 0.68
            sentiment = "Substantial Concern"
            impact_desc = "Significant climate-induced disruption requiring strategic adaptation interventions."
            action_rec = "Enforce regional resource management protocols and initiate contingency planning."
        else:
            severity = "MODERATE"
            severity_score = 0.45
            sentiment = "Analytical / Moderate Caution"
            impact_desc = "Ongoing climate dynamic requiring structured oversight and baseline tracking."
            action_rec = "Maintain periodic observation and integrate findings into annual policy reviews."

        # Geographic detection
        regions = []
        region_map = {
            "Global": ["global", "world", "international", "earth"],
            "Mediterranean / Southern Europe": ["mediterranean", "europe", "greece", "spain", "italy"],
            "Atlantic / Coastal": ["atlantic", "ocean", "coastal", "marine", "reef"],
            "North America": ["us", "united states", "canada", "north america"],
            "Asia-Pacific": ["asia", "china", "india", "pacific", "australia"],
            "Africa": ["africa", "sahel", "north africa"]
        }
        for reg_name, kws in region_map.items():
            if any(kw in combined for kw in kws):
                regions.append(reg_name)
        if not regions:
            regions = ["Global Scope"]

        return {
            "severity": severity,
            "severity_score": severity_score,
            "sentiment": sentiment,
            "key_impact": impact_desc,
            "recommended_action": action_rec,
            "regions_affected": regions[:2]
        }

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        verified_articles = state.get("verified_articles", [])
        analyzed_articles: List[Dict[str, Any]] = []

        self.log_step(
            stage="Impact Analysis Init",
            thought=f"Executing multi-dimensional risk analysis on {len(verified_articles)} verified climate items.",
            action="Calculate Severity Index, Sentiment, Regional Exposure, and Intervention Urgency",
            observation="Applying environmental risk modeling rules"
        )

        for art in verified_articles:
            title = art.get("title", "")
            content = art.get("content", "") or art.get("summary", "")
            heuristic = self._heuristic_analysis(title, content)

            llm_prompt = f"""
            Perform climate risk analysis for this article:
            Title: {title}
            Content: {content[:1000]}

            Return JSON with keys:
            - 'severity' ('CRITICAL', 'HIGH', 'MODERATE', or 'LOW')
            - 'severity_score' (float 0.0 to 1.0)
            - 'sentiment' (string)
            - 'key_impact' (concise description)
            - 'recommended_action' (actionable policy or mitigation step)
            - 'regions_affected' (list of strings)
            """

            analysis_result = self.call_llm(llm_prompt, default_fallback=heuristic)

            art["agent_analysis"] = {
                "severity": analysis_result.get("severity", heuristic["severity"]),
                "severity_score": analysis_result.get("severity_score", heuristic["severity_score"]),
                "sentiment": analysis_result.get("sentiment", heuristic["sentiment"]),
                "key_impact": analysis_result.get("key_impact", heuristic["key_impact"]),
                "recommended_action": analysis_result.get("recommended_action", heuristic["recommended_action"]),
                "regions_affected": analysis_result.get("regions_affected", heuristic["regions_affected"]),
                "credibility_score": art.get("verification", {}).get("credibility_score", 0.85)
            }
            analyzed_articles.append(art)

        self.log_step(
            stage="Impact Analysis Complete",
            thought=f"Risk assessments generated for all {len(analyzed_articles)} articles.",
            action="Store structured assessments in workflow state for executive synthesis",
            observation={
                "critical_count": sum(1 for a in analyzed_articles if a["agent_analysis"]["severity"] == "CRITICAL"),
                "high_count": sum(1 for a in analyzed_articles if a["agent_analysis"]["severity"] == "HIGH")
            }
        )

        state["analyzed_articles"] = analyzed_articles
        state["trace_logs"] = state.get("trace_logs", []) + self.reasoning_trace
        return state
