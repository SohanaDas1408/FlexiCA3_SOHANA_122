import logging
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from tools.fact_validator import FactValidatorTool

logger = logging.getLogger("FactCheckerAgent")


class FactCheckerAgent(BaseAgent):
    """
    Verification & Credibility Agent: Evaluates publisher authority, cross-references
    claims against IPCC consensus baselines, and flags greenwashing or misinformation.
    """

    def __init__(self, validator_tool: FactValidatorTool = None):
        super().__init__(
            name="FactCheckerAgent",
            role="Source Credibility & Scientific Consensus Verifier",
            system_prompt=(
                "You are an expert fact-checker specialized in climate science. "
                "Assess whether news claims align with IPCC AR6 scientific consensus "
                "and identify greenwashing tactics or sensationalized rhetoric."
            )
        )
        self.validator = validator_tool or FactValidatorTool()

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        raw_articles = state.get("raw_articles", [])
        verified_articles: List[Dict[str, Any]] = []

        self.log_step(
            stage="Verification Init",
            thought=f"Commencing factual verification and credibility auditing for {len(raw_articles)} candidate articles.",
            action="Invoke FactValidatorTool against IPCC consensus matrix and greenwashing filters",
            observation=f"Auditing publisher domains and claim consistency."
        )

        for art in raw_articles:
            title = art.get("title", "")
            source = art.get("source", "")
            url = art.get("url", "")
            full_content = art.get("content", "") or art.get("summary", "")

            # Tool evaluations
            credibility = self.validator.evaluate_credibility(source, url)
            scientific_check = self.validator.check_scientific_alignment(f"{title} {full_content}")
            gw_check = self.validator.detect_greenwashing_and_sensationalism(f"{title} {full_content}")

            # LLM Prompt for deeper validation if enabled
            llm_fallback = {
                "verified": gw_check["passed_quality_gate"],
                "credibility_score": credibility["credibility_score"],
                "scientific_alignment": "HIGH" if scientific_check["is_scientifically_aligned"] else "LOW",
                "notes": "Verified against scientific consensus and domain authority matrix."
            }

            llm_prompt = f"""
            Analyze the following climate news article for scientific accuracy and greenwashing:
            Title: {title}
            Source: {source}
            Content: {full_content[:1000]}

            Return JSON with keys: 'verified' (boolean), 'credibility_score' (float 0.0 to 1.0), 'scientific_alignment' (string), 'notes' (string).
            """
            
            validation_result = self.call_llm(llm_prompt, default_fallback=llm_fallback)

            art["verification"] = {
                "credibility_score": validation_result.get("credibility_score", credibility["credibility_score"]),
                "rating": credibility["rating"],
                "scientific_alignment": validation_result.get("scientific_alignment", "HIGH"),
                "matched_ipcc_topics": scientific_check["matched_ipcc_topics"],
                "greenwashing_flags": gw_check["greenwashing_flags"],
                "misinformation_risk": gw_check["misinformation_risk"],
                "passed_quality_gate": validation_result.get("verified", gw_check["passed_quality_gate"]),
                "notes": validation_result.get("notes", "Validated by FactCheckerAgent.")
            }

            if art["verification"]["passed_quality_gate"]:
                verified_articles.append(art)

        self.log_step(
            stage="Verification Complete",
            thought=f"Quality audit complete: {len(verified_articles)}/{len(raw_articles)} articles passed verification gates.",
            action="Annotate articles with credibility metrics and pass to Impact Analyst",
            observation={"verified_count": len(verified_articles), "rejected_count": len(raw_articles) - len(verified_articles)}
        )

        state["verified_articles"] = verified_articles
        state["trace_logs"] = state.get("trace_logs", []) + self.reasoning_trace
        return state
