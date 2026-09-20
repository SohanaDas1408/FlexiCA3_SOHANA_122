import pytest
from tools.climate_telemetry import ClimateTelemetryTool
from tools.news_fetcher import NewsFetcherTool
from gradio_app import copilot_chat


def test_climate_telemetry_planetary_indicators():
    telemetry = ClimateTelemetryTool()
    vitals = telemetry.get_planetary_indicators()
    assert "atmospheric_co2" in vitals
    assert vitals["atmospheric_co2"]["value"] > 400.0
    assert "global_temp_anomaly" in vitals
    assert vitals["global_temp_anomaly"]["value"] >= 1.0


def test_climate_telemetry_regional_anomaly():
    telemetry = ClimateTelemetryTool()
    anomaly = telemetry.get_regional_weather_anomaly("Mediterranean")
    assert anomaly["location"] == "Mediterranean"
    assert "current_temp_c" in anomaly
    assert "hazard_flags" in anomaly


def test_news_fetcher_custom_topic():
    fetcher = NewsFetcherTool()
    results = fetcher.fetch_by_custom_topic("wildfire heatwave", limit=2)
    assert len(results) > 0
    assert "title" in results[0]


def test_copilot_chat_offline_fallback():
    history, empty_input = copilot_chat(
        message="What are the key priorities for extreme heat adaptation?",
        history=[],
        groq_key="",
        model="llama-3.3-70b-versatile",
        temperature=0.2
    )
    assert len(history) == 1
    user_msg, bot_msg = history[0]
    assert "extreme heat" in user_msg
    assert "IPCC" in bot_msg or "adaptation" in bot_msg
