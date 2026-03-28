from typing import TypedDict, Optional, List

class WorkflowState(TypedDict):
    invoice_text: str
    extracted_data: Optional[dict]
    compliance_status: Optional[str] # "APPROVED", "REJECTED", "NEEDS_REVIEW"
    execution_status: Optional[str]  # "SUCCESS", "FAILED"
    audit_log: List[str]
    error_count: int