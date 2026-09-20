import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = DATA_DIR / "reports"

# Ensure essential directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# API Keys & LLM Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Supported Groq Models
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "deepseek-r1-distill-llama-70b",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", DEFAULT_GROQ_MODEL)

# Execution Mode: "groq", "gemini", "openai", or "auto"
AGENT_EXECUTION_MODE = os.getenv("AGENT_EXECUTION_MODE", "auto")

# RSS Feeds for Climate News Ingestion (Live Multi-Source Fallback)
DEFAULT_RSS_FEEDS = [
    {
        "name": "UN News - Climate Change",
        "url": "https://news.un.org/feed/subscribe/en/news/topic/climate-change/feed/rss.xml",
        "category": "International Policy & Governance"
    },
    {
        "name": "Phys.org - Earth & Climate",
        "url": "https://phys.org/rss-feed/earth-news/earth-sciences/",
        "category": "Scientific Research"
    },
    {
        "name": "ScienceDaily - Global Warming",
        "url": "https://www.sciencedaily.com/rss/earth_climate/global_warming.xml",
        "category": "Scientific Research"
    },
    {
        "name": "NASA Earth Observatory",
        "url": "https://earthobservatory.nasa.gov/feeds/earth-observatory.rss",
        "category": "Planetary Satellite Observation"
    },
    {
        "name": "Google News - Climate Hazard Alert",
        "url": "https://news.google.com/rss/search?q=climate+change+extreme+weather+when:7d&hl=en-US&gl=US&ceid=US:en",
        "category": "Global News"
    }
]

# Geographic Coordinates Dictionary for Geospatial Mapping
GEOGRAPHIC_COORDINATES = {
    "Global Scope": (20.0, 0.0),
    "Mediterranean": (35.0, 18.0),
    "Antarctica": (-75.25, 0.0),
    "Arctic": (78.0, 15.0),
    "Amazon Basin": (-3.46, -62.21),
    "North America": (39.82, -98.57),
    "Europe": (54.52, 15.25),
    "Asia-Pacific": (10.0, 110.0),
    "India": (20.59, 78.96),
    "Africa": (1.65, 17.35),
    "Australia": (-25.27, 133.77),
    "Southeast Asia": (12.56, 104.99),
    "South America": (-8.78, -55.49),
    "Middle East": (29.29, 42.55),
    "Caribbean": (15.32, -61.38),
    "California, USA": (36.77, -119.41),
    "Brazil": (-14.23, -51.92),
    "China": (35.86, 104.19),
    "Canada": (56.13, -106.34),
    "Germany": (51.16, 10.45),
    "Japan": (36.20, 138.25),
    "United Kingdom": (55.37, -3.43)
}

# IPCC & Scientific Reference Knowledge Base for Fact Verification
IPCC_FACTUAL_BASE = {
    "global_warming_human_cause": {
        "claim": "Human activities are unequivocally responsible for global warming.",
        "consensus": 1.0,
        "source": "IPCC AR6 Working Group I (2021)"
    },
    "1.5C_threshold": {
        "claim": "Limiting warming to 1.5C requires rapid, deep greenhouse gas emission reductions by 2030.",
        "consensus": 0.98,
        "source": "IPCC Special Report on 1.5C"
    },
    "sea_level_rise": {
        "claim": "Global mean sea level is rising at accelerating rates due to thermal expansion and ice sheet loss.",
        "consensus": 0.99,
        "source": "IPCC AR6 Synthesis Report"
    },
    "extreme_weather_link": {
        "claim": "Anthropogenic climate change increases frequency and intensity of extreme weather events.",
        "consensus": 0.97,
        "source": "World Weather Attribution & IPCC"
    },
    "renewables_viability": {
        "claim": "Solar and wind energy costs have decreased substantially, making them cost-competitive globally.",
        "consensus": 0.99,
        "source": "IRENA & IEA Global Energy Outlook"
    },
    "methane_urgency": {
        "claim": "Cutting methane emissions is the fastest single strategy to slow near-term global warming rate.",
        "consensus": 0.99,
        "source": "UNEP Global Methane Assessment & IPCC AR6"
    }
}

# Alert Severity Thresholds
SEVERITY_LEVELS = {
    "CRITICAL": {"score_min": 0.75, "color": "#ef4444", "badge": "CRITICAL RISK"},
    "HIGH": {"score_min": 0.55, "color": "#f97316", "badge": "HIGH RISK"},
    "MODERATE": {"score_min": 0.35, "color": "#eab308", "badge": "MODERATE"},
    "LOW": {"score_min": 0.0, "color": "#10b981", "badge": "LOW RISK / POSITIVE"}
}

