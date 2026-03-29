# Enterprise P2P Orchestration Agent

**Submission for ET AI Hackathon 2026**

**Problem Statement 2 - Agentic AI for Autonomous Enterprise Workflows**

A multi-agent system designed to take ownership of the Procurement-to-Payment (P2P) enterprise workflow featuring autonomous data extraction, compliance checking, and self-correcting execution.

## Setup Instructions

1. **Clone the repository and navigate to the directory:**
   ```bash
   git clone https://github.com/surya10602/p2p-agent.git
   cd p2p-agent
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```   
4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Google API key for the Gemini vision model:
   ```Code snippet
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage
To run the interactive Streamlit UI for the agent workflow:
```Bash
streamlit run app.py
```
This will launch a local web server where you can input raw invoice text or upload scanned invoice images, and watch the agents process the workflow.
