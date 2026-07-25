from fastapi import APIRouter
from app.schemas import AuditRequest, AuditResponse
from app.services.audit import audit_website

router = APIRouter(tags=["Audit"])

@router.post("/audit", response_model=AuditResponse)
async def audit_endpoint(request: AuditRequest):
    return await audit_website(str(request.url))