import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from .state import WorkflowState
from .tools import create_purchase_order, execute_erp_payment
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini 1.5 Flash for high-speed, enterprise-grade extraction
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

def intelligence_agent(state: WorkflowState):
    """Extracts data from raw text or images using Gemini."""
    state["audit_log"].append("Intelligence Agent: Starting multimodal extraction via Gemini.")
    
    payload = state["invoice_text"]
    
    # If the payload is a string (Text Input), wrap it in a standard prompt
    if isinstance(payload, str):
        message = HumanMessage(content=f"Extract vendor, amount (number), and items. Return ONLY JSON. Text: {payload}")
    # If the payload is a list (Image Input), pass the multimodal list directly
    else:
         message = HumanMessage(content=payload)
    
    response = llm.invoke([message])
    
    # Parse the JSON from Gemini's response
    try:
        clean_json = response.content.replace("```json", "").replace("```", "").strip()
        state["extracted_data"] = json.loads(clean_json)
        state["audit_log"].append("Intelligence Agent: Data extracted successfully.")
    except Exception as e:
        state["audit_log"].append(f"Intelligence Agent: Extraction failed - {e}")
        state["extracted_data"] = {"vendor": "Unknown", "amount": 0, "items": []}
        
    return state

def compliance_agent(state: WorkflowState):
    """Checks against mock policies."""
    state["audit_log"].append("Compliance Agent: Reviewing extracted data.")
    amount = state["extracted_data"].get("amount", 0)
    
    if amount > 10000:
        state["compliance_status"] = "NEEDS_REVIEW"
        state["audit_log"].append("Compliance Agent: Flagged for human review (Amount > 10k).")
    else:
        state["compliance_status"] = "APPROVED"
        state["audit_log"].append("Compliance Agent: Approved.")
    
    return state

def execution_agent(state: WorkflowState):
    """Mocks API call to ERP system using external tools."""
    state["audit_log"].append("Execution Agent: Attempting payment execution.")
    
    # Simulate an API failure on the first try to demonstrate self-correction
    if state["error_count"] < 1:
        state["error_count"] += 1
        state["execution_status"] = "FAILED"
        state["audit_log"].append("Execution Agent: API Timeout. Failed to connect to ERP.")
    else:
        vendor = state["extracted_data"].get("vendor", "Unknown")
        amount = state["extracted_data"].get("amount", 0)
        items = state["extracted_data"].get("items", [])
        
        # Execute actual python tools
        po_response = create_purchase_order(vendor, amount, items)
        payment_response = execute_erp_payment(po_response["po_number"], amount)
        
        state["execution_status"] = "SUCCESS"
        state["audit_log"].append(f"Execution Agent: {payment_response['message']}")
        
    return state