from langgraph.graph import StateGraph, END
from .state import WorkflowState
from .agents import intelligence_agent, compliance_agent, execution_agent

def route_after_compliance(state: WorkflowState):
    if state["compliance_status"] == "APPROVED":
        return "execution"
    else:
        return "human_review" # Ends workflow for manual intervention

def route_after_execution(state: WorkflowState):
    if state["execution_status"] == "FAILED" and state["error_count"] < 3:
        state["audit_log"].append("System: Self-correcting, retrying execution.")
        return "execution" 
    return "end"  # <--- Return the string "end" instead

def build_workflow():
    workflow = StateGraph(WorkflowState)
    
    # Add Nodes (The Agents)
    workflow.add_node("intelligence", intelligence_agent)
    workflow.add_node("compliance", compliance_agent)
    workflow.add_node("execution", execution_agent)
    
    # Define Edges (The Flow)
    workflow.set_entry_point("intelligence")
    workflow.add_edge("intelligence", "compliance")
    
    # Conditional Routing
    workflow.add_conditional_edges(
        "compliance",
        route_after_compliance,
        {
            "execution": "execution",
            "human_review": END
        }
    )
    
    workflow.add_conditional_edges(
        "execution",
        route_after_execution,
        {
            "execution": "execution",
            "end": END
        }
    )
    
    return workflow.compile()

# To run a test:
if __name__ == "__main__":
    app = build_workflow()
    initial_state = {
        "invoice_text": "Invoice from TechCorp for 5000 USD for Servers.",
        "extracted_data": None,
        "compliance_status": None,
        "execution_status": None,
        "audit_log": ["System: Workflow initialized."],
        "error_count": 0
    }
    
    final_state = app.invoke(initial_state)
    print("\nFinal Audit Log:")
    for log in final_state["audit_log"]:
        print(f"- {log}")