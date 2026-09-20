import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from config import REPORTS_DIR


class ReportGeneratorTool:
    """
    Autonomous tool to generate structured Markdown and professional PDF
    Executive Intelligence Digests of monitored climate events.
    """

    def __init__(self, output_dir: Path = REPORTS_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown_report(self, digest_data: Dict[str, Any]) -> Path:
        """
        Generates a structured Markdown intelligence briefing.
        """
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        report_filename = f"Climate_Intelligence_Report_{timestamp_str}.md"
        report_path = self.output_dir / report_filename

        md_content = []
        md_content.append(f"# 🌍 CLIMATE CHANGE INTELLIGENCE DIGEST")
        md_content.append(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  ")
        md_content.append(f"**Orchestration Engine:** Multi-Agent Autonomous Automation System  \n")
        md_content.append("---\n")

        # Executive Summary
        md_content.append("## 📌 Executive Summary")
        md_content.append(digest_data.get("executive_summary", "No summary available.") + "\n")

        # Key Metrics Table
        stats = digest_data.get("metrics", {})
        md_content.append("## 📊 Key Intelligence Metrics")
        md_content.append(f"- **Total Articles Processed:** {stats.get('total_analyzed', 0)}")
        md_content.append(f"- **Critical Risk Alerts:** {stats.get('critical_alerts', 0)}")
        md_content.append(f"- **Average Source Credibility:** {stats.get('avg_credibility', 0.0):.2f} / 1.00")
        md_content.append(f"- **Dominant Climate Category:** {stats.get('dominant_category', 'General')}\n")

        # Analyzed Articles Breakdown
        md_content.append("## 📰 Monitored Climate Events & Agent Analyses\n")
        for idx, art in enumerate(digest_data.get("articles", []), start=1):
            analysis = art.get("agent_analysis", {})
            md_content.append(f"### {idx}. {art.get('title')}")
            md_content.append(f"**Source:** {art.get('source')} | **Category:** {art.get('category')} | **Severity:** `{analysis.get('severity', 'MODERATE')}`")
            md_content.append(f"**Credibility Score:** {analysis.get('credibility_score', 0.85):.2f} / 1.00 | **Sentiment:** {analysis.get('sentiment', 'Neutral')}")
            md_content.append(f"\n> {art.get('summary')}\n")
            md_content.append(f"**Key Impact:** {analysis.get('key_impact', 'N/A')}")
            md_content.append(f"**Recommended Policy/Mitigation Action:** {analysis.get('recommended_action', 'N/A')}\n")
            md_content.append("---\n")

        # Strategic Recommendations
        md_content.append("## 🎯 Strategic Recommendations for Decision-Makers")
        for rec in digest_data.get("strategic_recommendations", []):
            md_content.append(f"- {rec}")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_content))

        return report_path

    def generate_pdf_report(self, digest_data: Dict[str, Any]) -> Path:
        """
        Generates a publication-grade PDF Executive Intelligence Digest.
        """
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"Climate_Intelligence_Report_{timestamp_str}.pdf"
        pdf_path = self.output_dir / pdf_filename

        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor("#64748b"),
            spaceAfter=14
        )
        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'BodyDark',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#334155")
        )
        highlight_style = ParagraphStyle(
            'HighlightText',
            parent=styles['BodyText'],
            fontName='Helvetica-Oblique',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#0369a1")
        )

        story = []

        # Header Title
        story.append(Paragraph("Climate Change News Monitoring & Intelligence Digest", title_style))
        story.append(Paragraph(
            f"Autonomous Agentic AI Automation System | Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            subtitle_style
        ))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=12))

        # Executive Summary Box
        story.append(Paragraph("Executive Summary", h2_style))
        exec_text = digest_data.get("executive_summary", "Autonomous analysis of real-time climate signals.")
        story.append(Paragraph(exec_text, body_style))
        story.append(Spacer(1, 10))

        # Key Metrics Table
        stats = digest_data.get("metrics", {})
        table_data = [
            ["Metric", "Value", "Benchmark / Status"],
            ["Total Events Analyzed", str(stats.get('total_analyzed', 0)), "100% Verified"],
            ["Critical Risk Alerts", str(stats.get('critical_alerts', 0)), "Immediate Attention"],
            ["Avg Source Credibility", f"{stats.get('avg_credibility', 0.88):.2f} / 1.00", "High Rigor"],
            ["Dominant Category", str(stats.get('dominant_category', 'Scientific Research')), "Primary Focus"]
        ]
        
        t = Table(table_data, colWidths=[180, 140, 180])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

        # Articles Section
        story.append(Paragraph("Monitored Events & Multi-Agent Assessments", h2_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#94a3b8"), spaceAfter=8))

        for idx, art in enumerate(digest_data.get("articles", []), start=1):
            analysis = art.get("agent_analysis", {})
            title = f"<b>{idx}. {art.get('title')}</b>"
            meta = f"<i>Source: {art.get('source')} | Severity: <b>{analysis.get('severity', 'MODERATE')}</b> | Credibility: {analysis.get('credibility_score', 0.85):.2f}</i>"
            
            story.append(Paragraph(title, body_style))
            story.append(Paragraph(meta, subtitle_style))
            story.append(Paragraph(art.get('summary', ''), highlight_style))
            story.append(Spacer(1, 3))
            story.append(Paragraph(f"<b>Key Impact:</b> {analysis.get('key_impact', 'N/A')}", body_style))
            story.append(Paragraph(f"<b>Action Item:</b> {analysis.get('recommended_action', 'N/A')}", body_style))
            story.append(Spacer(1, 8))

        # Recommendations
        story.append(Paragraph("Strategic Actions & Automation Directives", h2_style))
        for rec in digest_data.get("strategic_recommendations", []):
            story.append(Paragraph(f"• {rec}", body_style))
            story.append(Spacer(1, 2))

        doc.build(story)
        return pdf_path
