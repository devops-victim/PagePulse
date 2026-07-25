from fastapi import APIRouter
from schemas import AuditRequest, AuditResponse
from services.audit import audit_website

router = APIRouter(tags=["Audit"])

@router.post("/audit", response_model=AuditResponse)
async def audit_endpoint(request: AuditRequest):
    return await audit_website(str(request.url))