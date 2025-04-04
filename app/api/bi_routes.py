from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.agents.bi_agent import BusinessIntelligenceAgent

router = APIRouter()
bi_agent = BusinessIntelligenceAgent()

class AnalysisRequest(BaseModel):
    data: Dict[str, Any]
    analysis_type: str

@router.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    try:
        analysis = await bi_agent.analyze_data(request.data, request.analysis_type)
        return {
            "status": "success",
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def agent_health():
    return {
        "status": "healthy",
        "agent": "BI_Analyst"
    } 