from fastapi import APIRouter, Depends, HTTPException
from ..services.ai_service import ai_service
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/ai", tags=["ai"])

class DescriptionRequest(BaseModel):
    item_name: str
    industry: Optional[str] = None

@router.post("/generate-description")
def generate_description(request: DescriptionRequest):
    description = ai_service.generate_description(request.item_name, request.industry)
    return {"description": description}
