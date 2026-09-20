import os
import pytest
from agents.orchestrator import ClimateAgentOrchestrator


def test_full_orchestrator_pipeline_sample():
    orchestrator = ClimateAgentOrchestrator()
    results = orchestrator.run_pipeline(
        use_live_rss=False,
        sample_limit=2
    )

    assert results["execution_metadata"]["status"] == "COMPLETED_SUCCESSFULLY"
    assert "digest_data" in results
    assert "metrics" in results["digest_data"]
    assert results["digest_data"]["metrics"]["total_analyzed"] == 2
    assert "output_artifacts" in results
    
    pdf_path = results["output_artifacts"]["pdf_report_path"]
    md_path = results["output_artifacts"]["md_report_path"]
    
    assert os.path.exists(pdf_path)
    assert os.path.exists(md_path)
    assert os.path.getsize(pdf_path) > 0
    assert os.path.getsize(md_path) > 0
