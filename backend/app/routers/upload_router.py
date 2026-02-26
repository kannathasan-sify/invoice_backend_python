from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/logo")
async def upload_logo(file: UploadFile = File(...)):
    # Simple file saving logic. In production, use S3/Supabase Storage.
    file_ext = file.filename.split(".")[-1]
    file_name = f"logo_{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return {"url": f"/static/{file_name}", "message": "Logo uploaded successfully"}

@router.post("/signature")
async def upload_signature(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    file_name = f"sig_{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return {"url": f"/static/{file_name}", "message": "Signature uploaded successfully"}
