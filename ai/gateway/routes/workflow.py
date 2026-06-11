from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import uuid

from db import AsyncSessionLocal
from models.workflow import Workflow
from schemas.workflow import (
    WorkflowCreate,
    WorkflowResponse
)
from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

class TextRequest(BaseModel):
    text: str

router = APIRouter(prefix="/workflow", tags=["workflow"])


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        
@router.post(
    "",
    response_model=WorkflowResponse
)
async def create_workflow(
    payload: WorkflowCreate,
    db: AsyncSession = Depends(get_db)
):

    workflow = Workflow(
        name=payload.name,
        definition=payload.definition,
        webhook_token=str(uuid.uuid4())
    )

    db.add(workflow)

    await db.commit()

    await db.refresh(workflow)

    return workflow

@router.post("/analyze")
async def analyze_text(request: TextRequest):
    try:
        print(f"Received text: {request}") 
        result = classifier(request.text)
        
        return {
            "input": request.text,
            "label": result[0]['label'],
            "confidence": round(result[0]['score'], 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))