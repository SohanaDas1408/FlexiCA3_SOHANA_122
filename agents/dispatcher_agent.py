import logging
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from tools.report_generator import ReportGeneratorTool
from tools.notifier import AlertNotifierTool

logger = logging.getLogger("AlertDispatcherAgent")


class AlertDispatcherAgent(BaseAgent):
    """
    Automation & Dispatcher Agent: Executes automated tool actions including
    PDF/Markdown intelligence report generation and multi-channel critical alert dispatch.
    """

    def __init__(self, report_tool: ReportGeneratorTool = None, notifier_tool: AlertNotifierTool = None):
        super().__init__(
            name="AlertDispatcherAgent",
            role="Autonomous Automation & Multi-Channel Dispatch Specialist",
            system_prompt=(
                "You are an autonomous operations dispatcher. "
                "Execute publication actions, compile executive reports, and trigger "
                "automated emergency alerts for high-risk climate occurrences."
            )
        )
        self.report_tool = report_tool or ReportGeneratorTool()
        self.notifier = notifier_tool or AlertNotifierTool()

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        digest_data = state.get("digest_data", {})
        analyzed_articles = digest_data.get("articles", [])

        self.log_step(
            stage="Dispatch Init",
            thought="Beginning automated report generation and high-severity alert triggering.",
            action="Invoke ReportGeneratorTool (PDF/MD) and AlertNotifierTool",
            observation=f"Processing {len(analyzed_articles)} articles for publication and dispatch."
        )

        # 1. Generate Markdown Report
        md_path = self.report_tool.generate_markdown_report(digest_data)

        # 2. Generate PDF Report
        pdf_path = self.report_tool.generate_pdf_report(digest_data)

        # 3. Scan for Critical / High alerts and dispatch
        dispatched_list = []
        for art in analyzed_articles:
            analysis = art.get("agent_analysis", {})
            severity = analysis.get("severity", "LOW")

            if severity in ["CRITICAL", "HIGH"]:
                alert_payload = {
                    "severity": severity,
                    "title": art.get("title"),
                    "summary": art.get("summary"),
                    "recommended_action": analysis.get("recommended_action")
                }
                dispatched = self.notifier.dispatch_alert(alert_payload)
                dispatched_list.append(dispatched)

        self.log_step(
            stage="Dispatch Complete",
            thought=f"Automation cycle finalized. PDF/MD reports generated and {len(dispatched_list)} alerts dispatched.",
            action="Persist generated artifacts to system state",
            observation={
                "pdf_report": str(pdf_path),
                "md_report": str(md_path),
                "dispatched_alerts_count": len(dispatched_list)
            }
        )

        state["output_artifacts"] = {
            "pdf_report_path": str(pdf_path),
            "md_report_path": str(md_path),
            "dispatched_alerts": dispatched_list
        }
        state["trace_logs"] = state.get("trace_logs", []) + self.reasoning_trace
        return state
