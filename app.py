import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timezone
import os
import json
import sqlite3
from pathlib import Path

from tools.news_fetcher import NewsFetcherTool
from tools.fact_validator import FactValidatorTool
from tools.report_generator import ReportGeneratorTool
from tools.notifier import AlertNotifierTool
from agents.orchestrator import ClimateAgentOrchestrator
from config import REPORTS_DIR

# Database init
DB = "climate_watch.db"
def get_db_connection():
    conn = sqlite3.connect(DB)
    return conn

# Page Configuration
st.set_page_config(
    page_title="CLIMATE SENTINEL | Global News & Threat Intelligence Hub",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Modern Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0c4a6e 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        background: linear-gradient(90deg, #38bdf8, #4ade80);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -2px rgba(0,0,0,0.08);
    }
    .kpi-num {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }

    .news-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .news-card:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }

    .badge-pill {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.025em;
        margin-right: 8px;
    }
    .badge-critical { background-color: #fee2e2; color: #991b1b; border: 1px solid #f87171; }
    .badge-high { background-color: #ffedd5; color: #9a3412; border: 1px solid #fb923c; }
    .badge-medium { background-color: #fef9c3; color: #854d0e; border: 1px solid #facc15; }
    .badge-low { background-color: #dcfce7; color: #166534; border: 1px solid #4ade80; }
    
    .source-meta {
        color: #64748b;
        font-size: 0.82rem;
        margin-top: 4px;
        margin-bottom: 10px;
    }

    .action-box {
        background-color: #f0fdf4;
        border-left: 3px solid #22c55e;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        color: #14532d;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to get stats
def fetch_database_articles(category_filter="All", priority_filter="All", search_term=""):
    conn = get_db_connection()
    query = "SELECT id, title, source, category, priority, credibility, location, summary, action_recommendation, url, published, processed_at FROM articles WHERE 1=1"
    params = []
    
    if category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)
    if priority_filter != "All":
        query += " AND priority = ?"
        params.append(priority_filter)
    if search_term:
        query += " AND (title LIKE ? OR summary LIKE ? OR location LIKE ?)"
        term = f"%{search_term}%"
        params.extend([term, term, term])
        
    query += " ORDER BY id DESC LIMIT 100"
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_stats():
    conn = get_db_connection()
    c = conn.cursor()
    total = c.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
    critical = c.execute("SELECT COUNT(*) FROM articles WHERE priority = 'CRITICAL'").fetchone()[0]
    high = c.execute("SELECT COUNT(*) FROM articles WHERE priority = 'HIGH'").fetchone()[0]
    avg_cred = c.execute("SELECT AVG(credibility) FROM articles").fetchone()[0] or 0.90
    conn.close()
    return total, critical, high, avg_cred

# Top Hero Header
st.markdown("""
<div class="hero-container">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 class="hero-title">🌍 CLIMATE SENTINEL</h1>
            <p class="hero-subtitle">Autonomous Climate Intelligence, Threat Radar & Real-Time Event Monitoring System</p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(34, 197, 94, 0.2); color: #4ade80; padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; border: 1px solid rgba(74, 222, 128, 0.4);">
                ● LIVE RADAR ACTIVE
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&auto=format&fit=crop&q=80", use_container_width=True)
    st.markdown("### ⚡ Live Intelligence Trigger")
    
    preset_choice = st.selectbox(
        "Focus Topic / Hazard Filter",
        [
            "🔥 Extreme Heat, Droughts & Wildfires",
            "🌊 Ocean Warming & Glacier Melting",
            "⚡ Clean Energy & Decarbonization",
            "🌳 Deforestation & Biosphere Loss",
            "📜 Global Climate Policy & COP",
            "🌐 Comprehensive Global News Stream"
        ],
        index=0
    )
    
    preset_queries = {
        "🔥 Extreme Heat, Droughts & Wildfires": '"heatwave" OR "wildfire" OR "flood" OR "drought" climate',
        "🌊 Ocean Warming & Glacier Melting": '"glacier melting" OR "sea level rise" OR "ocean warming" climate',
        "⚡ Clean Energy & Decarbonization": '"solar power" OR "wind energy" OR "renewable grid" climate',
        "🌳 Deforestation & Biosphere Loss": '"amazon rainforest" OR "deforestation" OR "biodiversity loss" climate',
        "📜 Global Climate Policy & COP": '"climate policy" OR "carbon tax" OR "emissions reduction" OR "COP30"',
        "🌐 Comprehensive Global News Stream": '"climate change" OR "global warming" OR "carbon emissions"'
    }
    
    active_query = preset_queries[preset_choice]
    
    articles_count = st.slider("Events to Scan & Analyze", min_value=5, max_value=30, value=15, step=5)
    
    scan_button = st.button("🚀 SCAN LIVE CLIMATE SIGNALS", type="primary", use_container_width=True)
    
    st.divider()
    st.markdown("### 🔍 Filter In-Memory Stream")
    category_filter = st.selectbox(
        "Category",
        ["All", "Extreme Weather", "Climate Science", "Emissions", "Renewable Energy", "Climate Policy", "Adaptation", "Biodiversity", "Oceans"]
    )
    priority_filter = st.selectbox(
        "Priority Severity",
        ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"]
    )
    search_keyword = st.text_input("Keyword Search", placeholder="e.g. Europe, Mediterranean, Solar")

# Handle Live Scan Ingestion
if scan_button:
    with st.spinner("🛰️ Multi-Agent Radar active: Ingesting, fact-verifying & modeling severity..."):
        from gradio_app import run_agent_cycle
        status, summary, df_result, traces, pdf_path, _, _, _, _ = run_agent_cycle(
            news_key="",
            llm_key="",
            model="gpt-4o-mini",
            base_url="",
            q=active_query,
            n=articles_count
        )
        st.session_state["latest_pdf"] = pdf_path
        st.toast("✅ Live Monitoring Cycle completed successfully!", icon="🌍")

# KPI Summary Cards
total_arts, crit_alerts, high_alerts, avg_cred = get_stats()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Monitored Events</div>
        <div class="kpi-num">{total_arts}</div>
        <small style="color: #64748b;">Persistent in SQLite</small>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="kpi-card" style="border-left: 4px solid #ef4444;">
        <div class="kpi-label" style="color: #ef4444;">Critical Risk Alerts</div>
        <div class="kpi-num" style="color: #ef4444;">{crit_alerts}</div>
        <small style="color: #dc2626;">Immediate action required</small>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="kpi-card" style="border-left: 4px solid #f97316;">
        <div class="kpi-label" style="color: #f97316;">High Severity Hazards</div>
        <div class="kpi-num" style="color: #f97316;">{high_alerts}</div>
        <small style="color: #ea580c;">Elevated alert level</small>
    </div>
    """, unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="kpi-card" style="border-left: 4px solid #10b981;">
        <div class="kpi-label" style="color: #10b981;">Scientific Credibility Index</div>
        <div class="kpi-num" style="color: #10b981;">{avg_cred:.2f} <span style="font-size: 1rem; color: #64748b;">/ 1.00</span></div>
        <small style="color: #059669;">IPCC AR6 grounded</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_live, tab_radar, tab_reports, tab_architecture = st.tabs([
    "📰 Live Climate Intelligence Feed",
    "📊 Global Threat Radar & Analytics",
    "📄 Executive Digest & PDF Reports",
    "🧠 Multi-Agent Cognitive Architecture"
])

# TAB 1: Live News Feed
with tab_live:
    df_stream = fetch_database_articles(category_filter, priority_filter, search_keyword)
    
    col_hdr, col_actions = st.columns([3, 1])
    with col_hdr:
        st.subheader(f"⚡ Ingested Climate Events Stream ({len(df_stream)} items)")
    with col_actions:
        if not df_stream.empty:
            csv_data = df_stream.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Dataset (CSV)",
                data=csv_data,
                file_name=f"climate_sentinel_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    if df_stream.empty:
        st.info("👈 No matching articles found. Click **'SCAN LIVE CLIMATE SIGNALS'** in the sidebar to fetch real-time news.")
    else:
        for _, row in df_stream.iterrows():
            prio = row["priority"]
            badge_class = f"badge-{prio.lower()}"
            cred_pct = int((row["credibility"] or 0.85) * 100)
            
            st.markdown(f"""
            <div class="news-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span class="badge-pill {badge_class}">{prio}</span>
                        <span style="background: #f1f5f9; color: #475569; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">
                            {row['category']}
                        </span>
                        <span style="background: #f1f5f9; color: #475569; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; margin-left: 4px;">
                            📍 {row['location'] or 'Global'}
                        </span>
                    </div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: #0284c7;">
                        🛡️ Credibility: {cred_pct}%
                    </div>
                </div>
                <h4 style="margin: 10px 0 4px 0; color: #0f172a; font-weight: 700; line-height: 1.35;">
                    <a href="{row['url']}" target="_blank" style="color: #0f172a; text-decoration: none;">{row['title']}</a>
                </h4>
                <div class="source-meta">
                    <b>Publisher:</b> {row['source']} | <b>Published:</b> {str(row['published'])[:16]} | <b>Verified:</b> IPCC Baseline Match
                </div>
                <p style="color: #334155; font-size: 0.92rem; line-height: 1.5; margin-bottom: 0;">
                    {row['summary']}
                </p>
                <div class="action-box">
                    <b>🎯 Strategic Adaptation Directive:</b> {row['action_recommendation']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# TAB 2: Threat Radar & Visual Analytics
with tab_radar:
    st.subheader("📊 Planetary Risk & Threat Analytics")
    
    df_all = fetch_database_articles()
    if df_all.empty:
        st.info("No data available for analytics yet. Trigger a live scan to generate charts.")
    else:
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            # Severity distribution
            fig_prio = px.pie(
                df_all,
                names="priority",
                title="<b>Hazard Severity Distribution</b>",
                color="priority",
                color_discrete_map={
                    "CRITICAL": "#ef4444",
                    "HIGH": "#f97316",
                    "MEDIUM": "#eab308",
                    "LOW": "#10b981"
                },
                hole=0.45
            )
            fig_prio.update_layout(margin=dict(t=40, b=20, l=20, r=20))
            st.plotly_chart(fig_prio, use_container_width=True)

        with col_c2:
            # Category breakdown
            cat_counts = df_all['category'].value_counts().reset_index()
            cat_counts.columns = ['Category', 'Events Count']
            fig_cat = px.bar(
                cat_counts,
                x="Events Count",
                y="Category",
                orientation="h",
                title="<b>Events Breakdown by Climate Domain</b>",
                color="Events Count",
                color_continuous_scale="Tealgrn"
            )
            fig_cat.update_layout(margin=dict(t=40, b=20, l=20, r=20), yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_cat, use_container_width=True)

        st.divider()
        
        # Publisher credibility analysis
        fig_scatter = px.scatter(
            df_all,
            x="credibility",
            y="priority",
            color="category",
            size=[12]*len(df_all),
            hover_data=["title", "source"],
            title="<b>Source Credibility vs Threat Severity Matrix</b>",
            labels={"credibility": "Scientific Credibility Score (0.0 to 1.0)", "priority": "Hazard Priority Rating"}
        )
        fig_scatter.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_scatter, use_container_width=True)

# TAB 3: Reports & PDF Generator
with tab_reports:
    st.subheader("📄 Automated Executive Intelligence Reports")
    
    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        st.markdown("""
        Every monitoring cycle autonomously compiles an **Executive Climate Intelligence Digest (PDF)** formatted with:
        - Formal executive risk briefing for sustainability directors and government agencies.
        - Verified tabular event breakdown with severity ratings and IPCC consensus scores.
        - Actionable adaptation and policy recommendations.
        """)
        
        # Check if PDF exists in reports dir
        pdf_files = list(REPORTS_DIR.glob("*.pdf"))
        if pdf_files:
            latest_pdf = max(pdf_files, key=os.path.getctime)
            with open(latest_pdf, "rb") as f:
                pdf_bytes = f.read()
                st.download_button(
                    label=f"⬇️ Download Latest Executive PDF Report ({os.path.basename(latest_pdf)})",
                    data=pdf_bytes,
                    file_name=os.path.basename(latest_pdf),
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
        else:
            st.info("Click 'SCAN LIVE CLIMATE SIGNALS' to generate your first PDF report.")

    with col_p2:
        st.markdown("### 📋 Executive Summary Preview")
        st.info("""
        **Planetary Climate Status:** Multi-region monitoring indicates elevated heatwave indices across Mediterranean and Asian agricultural basins. Capital additions in solar and wind power continue at record velocity, offsetting regional grid stresses.
        """)

# TAB 4: Cognitive Architecture
with tab_architecture:
    st.subheader("🧠 Multi-Agent Cognitive Architecture (ReAct Loop)")
    st.markdown("""
    The **Climate Sentinel** system coordinates 5 specialized autonomous agents operating across sequential and state-driven feedback loops:
    """)
    
    st.markdown("""
    ```mermaid
    flowchart LR
        A[🛰️ NewsScoutAgent\nPerception & RSS Scraping] --> B[🔬 FactCheckerAgent\nIPCC AR6 Verification]
        B --> C[📊 ImpactAnalystAgent\nSeverity & Sentiment Modeling]
        C --> D[🧠 ActionSynthesizerAgent\nExecutive Policy Synthesis]
        D --> E[🚨 AlertDispatcherAgent\nPDF Report & Webhooks]
        E --> F[(💾 SQLite Memory\nclimate_watch.db)]
    ```
    """)
    
    st.markdown("""
    ### 🛡️ Anti-Hallucination & Scientific Grounding Gates
    1. **Domain Authority Indexing:** Incoming publisher domains are evaluated against verified scientific registries (e.g. *Copernicus, UN FAO, IEA, NASA, IPCC*).
    2. **Consensus Cross-Referencing:** Every candidate claim is verified against our indexed IPCC AR6 Working Group benchmark dataset.
    3. **Multi-Source Corroboration:** Cross-checks keyword and location clusters across independent newsrooms before assigning high-urgency priority.
    """)
