import logging
from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent
from tools.news_fetcher import NewsFetcherTool
from tools.climate_telemetry import ClimateTelemetryTool

logger = logging.getLogger("NewsScoutAgent")


class NewsScoutAgent(BaseAgent):
    """
    Perception & Ingestion Agent: Continuously crawls, filters, and structures
    climate news and events from NewsAPI.org, global RSS feeds, and web resources.
    """

    def __init__(self, fetcher_tool: Optional[NewsFetcherTool] = None, custom_groq_key: Optional[str] = None):
        super().__init__(
            name="NewsScoutAgent",
            role="Climate News Ingestion & Discovery Specialist",
            system_prompt=(
                "You are an autonomous intelligence agent scanning real-time climate signals. "
                "Your objective is to identify emerging environmental, policy, and scientific events."
            ),
            custom_groq_key=custom_groq_key
        )
        self.fetcher = fetcher_tool or NewsFetcherTool()
        self.telemetry_tool = ClimateTelemetryTool()

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        news_api_key = state.get("news_api_key", "")
        custom_topic = state.get("custom_topic", "").strip() or state.get("query", "").strip()
        use_live_rss = state.get("use_live_rss", True)
        feed_limit = state.get("feed_limit", 3)
        sample_limit = state.get("sample_limit", 15)

        articles = []
        # 1. Try authenticated NewsAPI if key provided
        if news_api_key:
            self.log_step(
                stage="Perception",
                thought=f"Initiating authenticated NewsAPI live query for: '{custom_topic or 'climate change'}'.",
                action="Invoke NewsFetcherTool.fetch_from_newsapi()",
                observation=f"Querying NewsAPI with limit={sample_limit}"
            )
            articles = self.fetcher.fetch_from_newsapi(
                query=custom_topic or "climate change OR global warming",
                api_key=news_api_key,
                limit=sample_limit
            )

        # 2. Dynamic topic query or Live RSS feeds
        if not articles and use_live_rss:
            if custom_topic:
                self.log_step(
                    stage="Perception",
                    thought=f"Initiating live dynamic climate query for topic: '{custom_topic}'.",
                    action="Invoke NewsFetcherTool.fetch_by_custom_topic()",
                    observation=f"Querying live Google News RSS for '{custom_topic}' with limit={sample_limit}"
                )
                articles = self.fetcher.fetch_by_custom_topic(custom_topic, limit=sample_limit)
            else:
                self.log_step(
                    stage="Perception",
                    thought="Initiating live multi-feed RSS news discovery (UN News, Phys.org, ScienceDaily, NASA).",
                    action="Invoke NewsFetcherTool.fetch_from_rss()",
                    observation=f"Querying configured feeds with limit_per_feed={feed_limit}"
                )
                articles = self.fetcher.fetch_from_rss(limit_per_feed=feed_limit)

        # 3. Fallback to offline verified dataset if disabled or empty
        if not articles:
            self.log_step(
                stage="Perception",
                thought="Ingesting verified scientific baseline climate dataset.",
                action="Invoke NewsFetcherTool.load_sample_articles()",
                observation=f"Loading verified benchmark items with limit={sample_limit}"
            )
            articles = self.fetcher.load_sample_articles(limit=sample_limit)

        # Deduplicate articles based on title
        seen_titles = set()
        deduped = []
        for art in articles:
            clean_title = art.get("title", "").strip().lower()
            if clean_title and clean_title not in seen_titles:
                seen_titles.add(clean_title)
                deduped.append(art)

        # Enrich state with live planetary vital signs
        planetary_vitals = self.telemetry_tool.get_planetary_indicators()

        self.log_step(
            stage="Ingestion Complete",
            thought=f"Perception phase completed. Successfully discovered and deduplicated {len(deduped)} articles. Acquired planetary baseline telemetry.",
            action="Populate shared state with candidate climate articles and planetary vitals",
            observation={
                "ingested_count": len(deduped),
                "sources": list(set(a.get('source', 'Unknown') for a in deduped)),
                "co2_ppm": planetary_vitals["atmospheric_co2"]["value"]
            }
        )

        state["raw_articles"] = deduped
        state["planetary_vitals"] = planetary_vitals
        state["trace_logs"] = state.get("trace_logs", []) + self.reasoning_trace
        return state

