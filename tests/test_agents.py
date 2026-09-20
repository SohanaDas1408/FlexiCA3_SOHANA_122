import pytest
from agents.scout_agent import NewsScoutAgent
from agents.fact_checker_agent import FactCheckerAgent
from agents.impact_analyst_agent import ImpactAnalystAgent
from agents.synthesizer_agent import ActionSynthesizerAgent
from agents.dispatcher_agent import AlertDispatcherAgent
from tools.news_fetcher import NewsFetcherTool
from tools.fact_validator import FactValidatorTool


def test_news_fetcher_sample_load():
    fetcher = NewsFetcherTool()
    articles = fetcher.load_sample_articles(limit=2)
    assert len(articles) == 2
    assert "title" in articles[0]
    assert "content" in articles[0]


def test_fact_validator_credibility():
    validator = FactValidatorTool()
    res = validator.evaluate_credibility("UN News", "https://news.un.org/feed")
    assert res["credibility_score"] >= 0.85
    assert res["rating"] == "HIGH"


def test_fact_validator_scientific_alignment():
    validator = FactValidatorTool()
    text = "Global sea level rise is accelerating due to ice sheet loss and thermal expansion."
    res = validator.check_scientific_alignment(text)
    assert res["matched_ipcc_topics"] > 0
    assert res["is_scientifically_aligned"] is True


def test_scout_agent_execution():
    scout = NewsScoutAgent()
    state = {"use_live_rss": False, "sample_limit": 2}
    result = scout.execute(state)
    assert "raw_articles" in result
    assert len(result["raw_articles"]) == 2
    assert len(result["trace_logs"]) > 0


def test_fact_checker_agent_execution():
    scout = NewsScoutAgent()
    checker = FactCheckerAgent()
    state = scout.execute({"use_live_rss": False, "sample_limit": 2})
    result = checker.execute(state)
    assert "verified_articles" in result
    assert len(result["verified_articles"]) > 0
    assert "verification" in result["verified_articles"][0]


def test_impact_analyst_agent_execution():
    scout = NewsScoutAgent()
    checker = FactCheckerAgent()
    analyst = ImpactAnalystAgent()
    
    state = scout.execute({"use_live_rss": False, "sample_limit": 2})
    state = checker.execute(state)
    result = analyst.execute(state)
    assert "analyzed_articles" in result
    assert "severity" in result["analyzed_articles"][0]["agent_analysis"]
    assert "sentiment" in result["analyzed_articles"][0]["agent_analysis"]
