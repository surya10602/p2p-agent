import time
import random

def create_purchase_order(vendor: str, amount: float, items: list) -> dict:
    """
    Mock API wrapper for creating a Purchase Order in an enterprise ERP.
    In a real system, this would use the requests library to POST data.
    """
    # Simulate network latency
    time.sleep(1) 
    
    return {
        "status": "success",
        "po_number": f"PO-{random.randint(1000, 9999)}",
        "message": f"Successfully created PO for {vendor}."
    }

def execute_erp_payment(po_number: str, amount: float) -> dict:
    """
    Mock API wrapper for scheduling a payment.
    """
    time.sleep(1)
    
    return {
        "status": "success",
        "transaction_id": f"TXN-{random.randint(10000, 99999)}",
        "message": f"Payment of ${amount} scheduled for {po_number}."
    }