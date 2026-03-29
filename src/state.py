from typing import TypedDict, Optional, List

class WorkflowState(TypedDict):
    invoice_text: str
    extracted_data: Optional[dict]
    compliance_status: Optional[str]
    execution_status: Optional[str]
    audit_log: List[str]
    error_count: int