import re
import logging
from typing import Dict, Any, List
from config import IPCC_FACTUAL_BASE

logger = logging.getLogger("FactValidatorTool")


class FactValidatorTool:
    """
    Autonomous tool to verify climate claims, detect misinformation/greenwashing,
    and compute a Source Credibility Index.
    """

    TRUSTED_DOMAINS = [
        "un.org", "ipcc.ch", "nasa.gov", "noaa.gov", "copernicus.eu",
        "nature.com", "science.org", "sciencedaily.com", "phys.org",
        "reuters.com", "iea.org", "worldbank.org", "wmo.int"
    ]

    GREENWASHING_KEYWORDS = [
        "eco-friendly", "clean coal", "carbon neutral commitment without verification",
        "natural solution", "greenest ever", "guaranteed zero emission",
        "100% sustainable without audit", "unverified offset"
    ]

    SENSATIONALIST_TERMS = [
        "apocalypse now", "earth will end in 5 years", "all humans doomed by next month",
        "miracle technology solves everything", "climate hoax", "global cooling conspiracy"
    ]

    def __init__(self):
        self.consensus_db = IPCC_FACTUAL_BASE

    def evaluate_credibility(self, source_name: str, url: str) -> Dict[str, Any]:
        """
        Computes credibility score (0.0 to 1.0) based on domain authority,
        peer-reviewed references, and established scientific bodies.
        """
        score = 0.70  # Baseline score
        source_lower = source_name.lower()
        url_lower = url.lower()

        # Check for premier scientific / institutional sources
        for domain in self.TRUSTED_DOMAINS:
            if domain in url_lower or domain.replace(".org", "").replace(".gov", "") in source_lower:
                score += 0.25
                break

        if any(term in source_lower for term in ["un ", "copernicus", "iea", "nasa", "noaa", "reuters", "science"]):
            score = max(score, 0.95)

        score = min(1.0, round(score, 2))

        return {
            "credibility_score": score,
            "rating": "HIGH" if score >= 0.85 else ("MODERATE" if score >= 0.65 else "LOW"),
            "trusted_domain_matched": score >= 0.85
        }

    def check_scientific_alignment(self, text: str) -> Dict[str, Any]:
        """
        Cross-references text against IPCC scientific consensus claims.
        """
        matched_claims: List[Dict[str, Any]] = []
        text_lower = text.lower()

        for key, info in self.consensus_db.items():
            # Check for keyword patterns
            keywords = key.split("_")
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches >= len(keywords) * 0.5:
                matched_claims.append({
                    "topic": key,
                    "scientific_consensus": info["claim"],
                    "source_reference": info["source"],
                    "consensus_level": f"{int(info['consensus'] * 100)}%"
                })

        return {
            "matched_ipcc_topics": len(matched_claims),
            "alignment_details": matched_claims,
            "is_scientifically_aligned": len(matched_claims) > 0 or not self._contains_pseudoscience(text_lower)
        }

    def detect_greenwashing_and_sensationalism(self, text: str) -> Dict[str, Any]:
        """
        Detects potential greenwashing claims and sensationalist rhetoric.
        """
        text_lower = text.lower()
        found_gw = [kw for kw in self.GREENWASHING_KEYWORDS if kw in text_lower]
        found_sensational = [term for term in self.SENSATIONALIST_TERMS if term in text_lower]

        risk_level = "LOW"
        if found_sensational or len(found_gw) >= 2:
            risk_level = "HIGH"
        elif found_gw:
            risk_level = "MEDIUM"

        return {
            "greenwashing_flags": found_gw,
            "sensationalism_flags": found_sensational,
            "misinformation_risk": risk_level,
            "passed_quality_gate": risk_level != "HIGH"
        }

    def _contains_pseudoscience(self, text_lower: str) -> bool:
        pseudoscience_patterns = [
            r"climate change is a hoax",
            r"global cooling has started",
            r"carbon dioxide is not a greenhouse gas"
        ]
        return any(re.search(pat, text_lower) for pat in pseudoscience_patterns)
