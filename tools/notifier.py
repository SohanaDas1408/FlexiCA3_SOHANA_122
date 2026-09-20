import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import requests

logger = logging.getLogger("AlertNotifierTool")


class AlertNotifierTool:
    """
    Autonomous tool to dispatch real-time climate alerts across notification
    channels (Webhooks, simulated emails, and alert logs).
    """

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self.dispatched_alerts: List[Dict[str, Any]] = []

    def dispatch_alert(self, alert_data: Dict[str, Any], channel: str = "webhook_simulated") -> Dict[str, Any]:
        """
        Dispatches high-severity climate alert to destination channels.
        """
        severity = alert_data.get("severity", "MODERATE")
        title = alert_data.get("title", "Climate Event Alert")
        summary = alert_data.get("summary", "")
        action = alert_data.get("recommended_action", "")
        
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "timestamp": timestamp,
            "severity": severity,
            "title": title,
            "summary": summary,
            "recommended_action": action,
            "status": "DISPATCHED",
            "channel": channel
        }

        # If live webhook is provided, post it
        if self.webhook_url and self.webhook_url.startswith("http"):
            try:
                response = requests.post(
                    self.webhook_url,
                    json={
                        "content": f"🚨 **[CLIMATE ALERT - {severity}]** {title}\n> {summary}\n**Action:** {action}"
                    },
                    timeout=5
                )
                payload["webhook_status_code"] = response.status_code
                logger.info(f"Webhook dispatched successfully: {response.status_code}")
            except Exception as e:
                logger.warning(f"Webhook dispatch failed: {e}")
                payload["error"] = str(e)

        self.dispatched_alerts.append(payload)
        return payload

    def get_dispatched_history(self) -> List[Dict[str, Any]]:
        return self.dispatched_alerts
