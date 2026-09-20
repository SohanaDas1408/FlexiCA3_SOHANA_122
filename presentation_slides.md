# 🌍 Climate Sentinel: Multi-Agent Climate Change News Monitoring
## Continuous Perception, Scientific Verification, Severity Modeling & Automated Policy Alerting
**Course:** Agentic AI and Automation  
**Presentation / Viva Slide Deck**

---

### Slide 1: Title & Introduction
- **Project Title:** Climate Sentinel: Autonomous Climate Change News Monitoring Multi-Agent System
- **Objective:** Build an autonomous cognitive multi-agent pipeline that transforms noisy global climate news into verifiable, high-impact intelligence digests and real-time emergency alerts.
- **Key Paradigms:** Multi-Agent Collaboration, Autonomous Tool Invocation, ReAct Deliberation Loop, IPCC Consensus Grounding.

---

### Slide 2: Problem Statement & Motivation
- **The Challenge:** Global news contains high noise, greenwashing, corporate misinformation, and sensationalist rhetoric.
- **The Cognitive Gap:** Decision-makers lack time to sift through hundreds of articles to compute severity and extract policy action items.
- **The Solution:** A collaborative team of 5 specialized AI agents working sequentially to ingest, verify, analyze, synthesize, and automate reports.

---

### Slide 3: 5-Agent Collaborative Architecture
1. **NewsScoutAgent (Perception):** Ingests live RSS feeds and web articles.
2. **FactCheckerAgent (Verification):** Audits domain authority & IPCC AR6 alignment; filters greenwashing.
3. **ImpactAnalystAgent (Cognition):** Quantifies severity scores, climate sentiment, and regional exposure.
4. **ActionSynthesizerAgent (Synthesis):** Formulates strategic policy recommendations and executive briefing.
5. **AlertDispatcherAgent (Automation):** Compiles vector PDF digests and dispatches webhook alerts.

---

### Slide 4: Autonomous Tool Integration
- **`NewsFetcherTool`:** Multi-source RSS parser and HTML cleaner with automatic sample fallback.
- **`FactValidatorTool`:** Domain credibility weighting + IPCC scientific consensus knowledge base.
- **`ReportGeneratorTool`:** Publication-grade PDF compilation using ReportLab with tables and styling.
- **`AlertNotifierTool`:** Multi-channel webhook and urgent event dispatcher.

---

### Slide 5: System Features & UI
- **Live Streamlit Dashboard:** Complete agent control room with real-time status telemetry.
- **Reasoning Trace Visualizer:** Transparent inspection of each agent's internal Thought-Action-Observation steps.
- **Visual Analytics:** Plotly severity distribution graphs and credibility ranking charts.
- **1-Click Export:** Instant PDF and Markdown intelligence report generation.

---

### Slide 6: Verification, Testing & Results
- **Automated Test Suite:** 100% test coverage with `pytest` on agents, tools, and integration pipeline.
- **Execution Performance:** Sub-4-second end-to-end multi-agent pipeline execution.
- **Dual Execution Engine:** Works seamlessly with LLMs (Gemini / OpenAI) or deterministic cognitive fallback engine.

---

### Slide 7: Expected Viva Questions & Answers
- **Q: Why use multiple agents instead of a single LLM prompt?**  
  *A: Role specialization prevents cognitive overload, provides modular tool access, enables independent quality gates (verification can reject bad data before analysis), and yields auditable reasoning traces.*
- **Q: How does the agent prevent hallucinations?**  
  *A: Through the `FactCheckerAgent` and `FactValidatorTool`, which ground incoming claims against an IPCC AR6 scientific baseline and authoritative domain registries.*
- **Q: What automation does this system perform?**  
  *A: Automated data fetching, quality filtering, PDF compilation, and real-time webhook alerting for high-risk climate events.*

---

### Slide 8: Conclusion & Future Scope
- **Conclusion:** Delivers a production-grade, end-to-end Agentic AI solution fulfilling all academic and practical requirements.
- **Future Scope:** Satellite telemetry integration (Copernicus / NASA FIRMS), multilingual scraping, and Graph-RAG memory.
