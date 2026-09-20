import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
import feedparser
import requests
from bs4 import BeautifulSoup
from config import DEFAULT_RSS_FEEDS, DATA_DIR, NEWS_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NewsFetcherTool")


class NewsFetcherTool:
    """
    Autonomous tool to scrape, parse, and clean climate-related news
    from NewsAPI.org authenticated API, RSS feeds, direct URLs, or offline datasets.
    """

    def __init__(self, sample_data_path: Optional[Path] = None):
        self.sample_data_path = sample_data_path or (DATA_DIR / "sample_articles.json")
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36 ClimateAgentBot/1.0"
        })

    def fetch_from_newsapi(
        self,
        query: str = "climate change OR global warming",
        api_key: Optional[str] = None,
        limit: int = 15,
        sort_by: str = "publishedAt"
    ) -> List[Dict[str, Any]]:
        """
        Fetches live articles from official NewsAPI.org endpoint.
        """
        key = api_key or NEWS_API_KEY
        if not key or len(key.strip()) < 8:
            logger.info("NewsAPI key not supplied. Proceeding to live dynamic RSS stream.")
            return []

        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "language": "en",
                "sortBy": sort_by,
                "pageSize": min(limit, 50)
            }
            headers = {"X-Api-Key": key.strip()}
            resp = self.session.get(url, params=params, headers=headers, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "ok":
                    articles = []
                    for raw in data.get("articles", []):
                        title = (raw.get("title") or "").strip()
                        if not title or "[Removed]" in title:
                            continue
                        src = (raw.get("source") or {}).get("name", "NewsAPI Wire")
                        pub_date = raw.get("publishedAt", datetime.now(timezone.utc).isoformat())
                        desc = (raw.get("description") or raw.get("content") or "").strip()
                        link = raw.get("url", "")
                        article_id = f"newsapi-{abs(hash(link or title)) % 1000000:06d}"

                        articles.append({
                            "id": article_id,
                            "title": title,
                            "source": src,
                            "published_date": pub_date,
                            "category": "Global NewsAPI Ingestion",
                            "summary": desc[:400] + ("..." if len(desc) > 400 else ""),
                            "content": desc,
                            "url": link,
                            "ingestion_method": "NEWS_API_AUTHENTICATED"
                        })
                    logger.info(f"Successfully fetched {len(articles)} articles via NewsAPI.")
                    return articles
                else:
                    logger.warning(f"NewsAPI error response: {data.get('message')}")
            else:
                logger.warning(f"NewsAPI returned status {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            logger.warning(f"NewsAPI fetch failed: {e}")

        return []

    def fetch_from_rss(self, feeds: Optional[List[Dict[str, str]]] = None, limit_per_feed: int = 3) -> List[Dict[str, Any]]:
        """
        Fetches live articles from configured RSS feeds.
        """
        feeds_to_fetch = feeds or DEFAULT_RSS_FEEDS
        articles: List[Dict[str, Any]] = []

        for feed_config in feeds_to_fetch:
            feed_name = feed_config.get("name", "Unknown Feed")
            feed_url = feed_config.get("url", "")
            feed_category = feed_config.get("category", "General Climate")

            try:
                logger.info(f"Parsing RSS feed: {feed_name} -> {feed_url}")
                parsed = feedparser.parse(feed_url)
                
                count = 0
                for entry in parsed.entries:
                    if count >= limit_per_feed:
                        break

                    title = entry.get("title", "No Title").strip()
                    summary = entry.get("summary", entry.get("description", ""))
                    link = entry.get("link", "")
                    pub_date = entry.get("published", datetime.now(timezone.utc).isoformat())

                    # Clean summary HTML
                    clean_summary = BeautifulSoup(summary, "html.parser").get_text(strip=True) if summary else ""

                    article_id = f"rss-{abs(hash(link or title)) % 1000000:06d}"
                    articles.append({
                        "id": article_id,
                        "title": title,
                        "source": feed_name,
                        "published_date": pub_date,
                        "category": feed_category,
                        "summary": clean_summary[:400] + ("..." if len(clean_summary) > 400 else ""),
                        "content": clean_summary,
                        "url": link,
                        "ingestion_method": "RSS_FEED"
                    })
                    count += 1
            except Exception as e:
                logger.warning(f"Failed to fetch RSS feed '{feed_name}': {e}")

        if not articles:
            logger.info("Live RSS returned 0 articles. Falling back to offline sample dataset.")
            return self.load_sample_articles()

        return articles

    def fetch_by_custom_topic(self, topic: str, limit: int = 6) -> List[Dict[str, Any]]:
        """
        Dynamically queries live Google News RSS for any specific custom climate topic or region.
        """
        import urllib.parse
        clean_t = topic.replace('"', '').replace(' OR ', ' ')
        encoded_query = urllib.parse.quote(f"{clean_t} climate")
        custom_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        
        logger.info(f"Querying live dynamic RSS for topic: '{topic}' -> {custom_url}")
        articles: List[Dict[str, Any]] = []
        try:
            parsed = feedparser.parse(custom_url)
            for entry in parsed.entries[:limit]:
                title = entry.get("title", "No Title").strip()
                summary = entry.get("summary", entry.get("description", ""))
                link = entry.get("link", "")
                pub_date = entry.get("published", datetime.now(timezone.utc).isoformat())

                clean_summary = BeautifulSoup(summary, "html.parser").get_text(strip=True) if summary else ""
                article_id = f"custom-{abs(hash(link or title)) % 1000000:06d}"

                src = "Google Climate Radar"
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    title = parts[0].strip()
                    src = parts[1].strip()

                articles.append({
                    "id": article_id,
                    "title": title,
                    "source": src,
                    "published_date": pub_date,
                    "category": "Live Climate Wire",
                    "summary": clean_summary[:400] + ("..." if len(clean_summary) > 400 else ""),
                    "content": clean_summary,
                    "url": link,
                    "ingestion_method": "LIVE_DYNAMIC_SEARCH"
                })
        except Exception as e:
            logger.warning(f"Failed to fetch dynamic topic '{topic}': {e}")

        if not articles:
            logger.info(f"No live results found for '{topic}'. Falling back to verified sample dataset.")
            return self.load_sample_articles(limit=limit)

        return articles

    def load_sample_articles(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Loads pre-curated scientific and news articles from the local dataset.
        """
        if self.sample_data_path.exists():
            with open(self.sample_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    item["ingestion_method"] = "OFFLINE_VERIFIED_DATASET"
                return data[:limit] if limit else data
        return []

    def fetch_full_text(self, url: str) -> str:
        """
        Attempts to scrape full readable text from a news URL.
        """
        if not url or not url.startswith("http"):
            return ""
        try:
            response = self.session.get(url, timeout=6)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = soup.find_all("p")
                text = " ".join(p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30)
                return text[:2500]
        except Exception as e:
            logger.debug(f"Full text extraction skipped for {url}: {e}")
        return ""

