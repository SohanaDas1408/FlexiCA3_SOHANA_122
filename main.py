import argparse
import sys
import os
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from agents.orchestrator import ClimateAgentOrchestrator


def print_banner():
    print("""
========================================================================
   [+] CLIMATE CHANGE NEWS MONITORING AGENT (AGENTIC AI & AUTOMATION)
========================================================================
    Autonomous Multi-Agent Perception, Verification & Policy Pipeline
========================================================================
""")


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Run Climate Change News Monitoring Multi-Agent Pipeline")
    parser.add_argument("--mode", choices=["live", "sample"], default="sample", help="Mode: live (RSS) or sample (offline dataset)")
    parser.add_argument("--topic", type=str, default="", help="Specific live climate topic to search in real-time (e.g. 'Wildfires', 'Amazon', 'Antarctica')")
    parser.add_argument("--limit", type=int, default=4, help="Number of articles to process")
    parser.add_argument("--verbose", action="store_true", help="Print detailed agent thought traces")
    args = parser.parse_args()

    print(f"[*] Initializing Multi-Agent Orchestrator...")
    topic_str = f", Topic='{args.topic}'" if args.topic else ""
    print(f"[*] Configuration: Mode={args.mode.upper()}{topic_str}, Limit={args.limit}\n")

    orchestrator = ClimateAgentOrchestrator()

    def cli_progress(agent_name, pct, msg):
        print(f"[{pct:3d}%] [{agent_name}] -> {msg}")

    results = orchestrator.run_pipeline(
        use_live_rss=(args.mode == "live" or bool(args.topic)),
        custom_topic=args.topic,
        feed_limit=1,
        sample_limit=args.limit,
        progress_callback=cli_progress
    )

    digest = results.get("digest_data", {})
    metrics = digest.get("metrics", {})
    artifacts = results.get("output_artifacts", {})

    print("\n" + "="*72)
    print("                      [*] EXECUTIVE SUMMARY                      ")
    print("="*72)
    print(digest.get("executive_summary", "No summary generated."))

    print("\n[*] INTELLIGENCE METRICS:")
    print(f"  * Total Events Analyzed:    {metrics.get('total_analyzed', 0)}")
    print(f"  * Critical Alerts:          {metrics.get('critical_alerts', 0)}")
    print(f"  * High Risk Alerts:         {metrics.get('high_alerts', 0)}")
    print(f"  * Avg Source Credibility:   {metrics.get('avg_credibility', 0.0):.2f} / 1.00")
    print(f"  * Primary Climate Category: {metrics.get('dominant_category', 'General')}")

    print("\n[*] STRATEGIC RECOMMENDATIONS:")
    for idx, rec in enumerate(digest.get("strategic_recommendations", []), start=1):
        print(f"  {idx}. {rec}")

    print("\n[*] GENERATED ARTIFACTS:")
    print(f"  - PDF Intelligence Digest:  {artifacts.get('pdf_report_path')}")
    print(f"  - Markdown Briefing:        {artifacts.get('md_report_path')}")
    print(f"  - Dispatched Alerts Count:  {len(artifacts.get('dispatched_alerts', []))}")

    if args.verbose:
        print("\n" + "="*72)
        print("                  AGENT COGNITIVE REASONING TRACES            ")
        print("="*72)
        for log in results.get("trace_logs", []):
            print(f"[{log['agent']}] [{log['stage']}]")
            print(f"  Thought:     {log['thought']}")
            print(f"  Action:      {log['action']}")
            print(f"  Observation: {log['observation']}\n")

    print(f"\n[+] Multi-Agent Execution Completed Successfully in "
          f"{results.get('execution_metadata', {}).get('total_execution_seconds', 0)}s!\n")


if __name__ == "__main__":
    main()
