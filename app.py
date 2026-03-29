import streamlit as st
import base64
from src.workflow import build_workflow

st.set_page_config(page_title="P2P Agentic Workflow", layout="centered")

st.title("Enterprise P2P Orchestration Agent")
st.markdown("Autonomous invoice processing with **multimodal AI**, self-correction, and audit trails.")

# UI for selecting input type
input_type = st.radio("Invoice Input Format:", ["Text", "Image"])

invoice_payload = None

if input_type == "Text":
    invoice_payload = st.text_area(
        "Incoming Invoice (Raw Text)", 
        "Invoice from TechCorp for 5000 USD for Servers. Due net 30."
    )
else:
    uploaded_file = st.file_uploader("Upload Scanned Invoice", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="Scanned Document", use_container_width=True)
        # Convert image to Base64 to send directly to Gemini
        image_bytes = uploaded_file.getvalue()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        
        # Create a multimodal payload format that LangChain and Gemini understand
        invoice_payload = [
            {"type": "text", "text": "Extract the vendor name, total amount (as a number), and items from this invoice image. Return ONLY valid JSON with keys: 'vendor', 'amount', 'items'."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]

if st.button("Run Autonomous Workflow"):
    if not invoice_payload:
        st.warning("Please provide an invoice (text or image) to start.")
    else:
        with st.spinner("Multi-agent system initialized..."):
            app = build_workflow()
            
            # Pass the content into the state graph
            initial_state = {
                "invoice_text": invoice_payload, 
                "extracted_data": None,
                "compliance_status": None,
                "execution_status": None,
                "audit_log": ["System: Workflow initialized. Input received."],
                "error_count": 0
            }
            
            final_state = app.invoke(initial_state)
            
            st.subheader("Live Agent Audit Trail")
            for log in final_state["audit_log"]:
                if "Failed" in log or "failed" in log or "Self-correcting" in log:
                    st.warning(log)
                elif "Approved" in log or "successfully" in log or "SUCCESS" in log:
                    st.success(log)
                else:
                    st.info(log)
            
            st.subheader("Extracted Enterprise Data")
            st.json(final_state["extracted_data"])