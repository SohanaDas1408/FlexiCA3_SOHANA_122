import os
import sqlite3
import pytest
from gradio_app import (
    init_db, save_article, rank_priority, verify_corroboration,
    local_analyze, run_agent_cycle, get_agent_memory, DB
)


def test_sqlite_db_initialization():
    init_db()
    conn = sqlite3.connect(DB)
    tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    conn.close()
    assert "articles" in tables
    assert "logs" in tables


def test_local_analyze_categorization():
    sample_item = {
        "title": "Severe Flood and Heatwave strikes Mediterranean",
        "description": "Rising temperatures cause unprecedented flood and wildfire emergency across southern Europe."
    }
    analysis = local_analyze(sample_item)
    assert analysis["category"] == "Extreme Weather"
    assert analysis["relevance"] > 0.3
    assert len(analysis["keywords"]) > 0


def test_corroboration_and_priority():
    article = {
        "title": "Deadly Wildfire Evacuations Declared",
        "summary": "Severe disaster wildfire spreads due to extreme heat",
        "category": "Extreme Weather",
        "source": "Source A",
        "keywords": ["wildfire", "extreme heat"],
        "relevance": 0.8
    }
    other_items = [
        {"source": "Source B", "keywords": ["wildfire", "smoke"]},
        {"source": "Source C", "keywords": ["extreme heat", "evacuation"]}
    ]
    status, count = verify_corroboration(article, other_items)
    assert "Corroborated" in status
    assert count == 2

    priority = rank_priority(article, count)
    assert priority == "CRITICAL"


def test_save_and_memory():
    import time
    unique_id = f"{time.time()}"
    article = {
        "title": f"Test Unique Headline for Agent Memory {unique_id}",
        "url": f"https://example.com/test-article-{unique_id}",
        "source": "Test Authority",
        "published": "2026-03-20T12:00:00Z",
        "summary": "This is a test summary for persistence verification.",
        "category": "Climate Science",
        "location": "Global Scope",
        "relevance": 0.75,
        "priority": "HIGH",
        "verification": "Corroborated",
        "corroboration": 2
    }
    saved = save_article(article)
    assert saved is True

    result = get_agent_memory()
    md = result[0]
    df_articles = result[1]
    df_logs = result[2]
    assert not df_articles.empty
    assert any(unique_id in str(x) for x in df_articles["Headline"].values)

