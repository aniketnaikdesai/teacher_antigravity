import traceback
from fastapi import FastAPI, HTTPException, status
from pydantic import ValidationError

from app.core.config import settings
from app.core.logger import logger
from app.models.schemas import ConversationStore
from app.services.storage import StorageService

app = FastAPI(
    title=settings.APP_NAME,
    description="Teacher Antigravity - Deterministic Knowledge Engine",
    version="1.0"
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Teacher Antigravity API...", extra={"stage": "System Boot"})
    logger.info(f"Primary Router: {'Gemini' if settings.is_gemini_enabled else 'Ollama Failsafe'}")

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Baseline /health endpoint (Section 26 / A1).
    Checks configuration status for provider routing.
    """
    provider_status = {
        "gemini_enabled": settings.is_gemini_enabled,
        "ollama_api_base": settings.OLLAMA_API_BASE
    }
    return {"status": "healthy", "providers": provider_status}

@app.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_conversation(payload: ConversationStore):
    """
    Stage 1: Conversation Intake
    Accepts raw conversational data and validates against Section 12 schema.
    """
    run_id = f"run_{payload.conversation_id}"
    logger.info(f"Intake started for {payload.conversation_id}", extra={"run_id": run_id, "stage": "Conversation Intake"})

    try:
        # Step 1: Save immutably
        stored_path = StorageService.save_conversation(payload)
        
        # Pipeline orchestration will trigger downstream from here.
        # For Phase 1, we just return success after immutable storage.

        return {
            "status": "success",
            "message": "Conversation ingested and saved immutably.",
            "conversation_id": payload.conversation_id,
            "path": str(stored_path)
        }
        
    except FileExistsError as e:
        # Immutability failure
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(
            f"Intake pipeline failed: {str(e)}", 
            extra={
                "run_id": run_id, 
                "stage": "Conversation Intake", 
                "failure_class": "UnhandledException",
                "exception": "".join(traceback.format_exception(None, e, e.__traceback__))
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Pipeline execution failed."
        )
