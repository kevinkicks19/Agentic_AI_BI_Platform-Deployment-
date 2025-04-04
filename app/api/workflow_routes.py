from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
from app.services.workflow_service import WorkflowService
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
workflow_service = WorkflowService()

class ProblemRequest(BaseModel):
    problem: str

class ResponseRequest(BaseModel):
    response: str

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Our typical customer journey starts with a social media ad..."
            }
        }

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError("Response must be a string")
        # Clean the string of any problematic characters
        cleaned = v.strip()
        # Remove any control characters except newlines
        cleaned = ''.join(char if char == '\n' or ord(char) >= 32 else ' ' for char in cleaned)
        # Ensure proper JSON stringification
        try:
            import json
            # First encode to ensure proper escaping
            cleaned = json.dumps(cleaned)
            # Then decode to get the properly escaped string
            cleaned = json.loads(cleaned)
            return cleaned
        except Exception as e:
            logger.error(f"Error in JSON stringification: {str(e)}")
            return cleaned

@router.post("/start")
async def start_session(request: ProblemRequest):
    try:
        logger.info(f"Starting new session with problem: {request.problem}")
        agent_response = await workflow_service.start_session(request.problem)
        logger.info(f"Got response from coaching agent: {agent_response}")
        
        # Store integration data internally
        session_status = workflow_service.get_session_status()
        
        # Return simplified response
        result = {
            "status": agent_response.get("status", "unknown"),
            "response": agent_response.get("content", "No response"),
            "session_id": session_status.get("session_id")
        }
        
        logger.info(f"Returning simplified result: {result}")
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in start_session: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )

@router.post("/respond")
async def continue_session(request: ResponseRequest):
    try:
        # Use the response directly without additional processing
        logger.info(f"Continuing session with response: {request.response}")
        agent_response = await workflow_service.continue_session(request.response)
        logger.info(f"Got response from coaching agent: {agent_response}")
        
        # Store integration data internally
        session_status = workflow_service.get_session_status()
        
        # Return simplified response
        result = {
            "status": agent_response.get("status", "unknown"),
            "response": agent_response.get("content", "No response"),
            "session_id": session_status.get("session_id")
        }
        
        logger.info(f"Returning simplified result: {result}")
        return JSONResponse(content=result)
    except ValueError as e:
        logger.error(f"Value error in continue_session: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "detail": str(e)}
        )
    except Exception as e:
        logger.error(f"Error in continue_session: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )

@router.post("/confirm")
async def confirm_summary():
    try:
        logger.info("Confirming problem summary")
        result = await workflow_service.confirm_problem_summary()
        logger.info(f"Got confirmation result: {result}")
        
        # Return simplified response
        simplified_result = {
            "status": result.get("status", "unknown"),
            "summary": result.get("summary", {}),
            "plan": result.get("plan", {})
        }
        
        return JSONResponse(content=simplified_result)
    except ValueError as e:
        logger.error(f"Value error in confirm_summary: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"status": "error", "detail": str(e)}
        )
    except Exception as e:
        logger.error(f"Error in confirm_summary: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )

@router.get("/status")
async def get_status():
    try:
        logger.info("Getting session status")
        status = workflow_service.get_session_status()
        logger.info(f"Current status: {status}")
        
        # Return simplified status
        simplified_status = {
            "status": status.get("status", "inactive"),
            "has_problem_summary": status.get("has_problem_summary", False),
            "has_solution_plan": status.get("has_solution_plan", False),
            "session_id": status.get("session_id")
        }
        
        return JSONResponse(content=simplified_status)
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        ) 