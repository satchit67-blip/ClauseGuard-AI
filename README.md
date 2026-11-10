# ClauseGuard AI ⚖️

ClauseGuard AI is an automated legal contract auditing tool built to scan multi-page PDF agreements, detect predatory clauses, calculate overall risk exposure scores, and propose actionable counter-clauses.

## 🛠️ Tech Stack & Architecture

ClauseGuard AI is designed with a clean, modular architecture separating the frontend user interface, core utilities, and AI orchestration. While the core engine leverages Python, future expansions and alternative components are planned across multiple languages.

* **Frontend UI**: Streamlit (Python) / *Planned frontend expansions in TypeScript & React*
* **Backend Intelligence**: Google GenAI SDK (`google-genai`), Python
* **Core Logic & Parsing**: `pypdf`, Heuristic Rule Engine (Python) / *Potential future microservices in Go or Node.js*
* **Environment & Deployment**: Git, GitHub, PowerShell

## 📂 Project Structure

```text
├── app.py              # Streamlit frontend interface and state management
├── ai_client.py        # Gemini API integration and structured JSON parsing
├── utils.py            # PDF text extraction and deterministic heuristic audit engine
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation

## Installation
```bash
pip install -r requirements.txt
streamlit run app.py
```

