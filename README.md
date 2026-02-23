Here you go, Vladimir — a clean, modern **README.md** fully aligned with your new OpenAI‑powered architecture, arXiv integration, and a smooth `uv`‑based setup. I’ve also added **desktop launcher scripts** (start/stop) so you can run the whole system like a local research app.

---

# ⚡ AI‑Powered APA 7 Bibliography Generator (OpenAI + arXiv)
`https://github.com/user-attachments/assets/2fa19dc2-3b2e-44da-abc0-2c9dd3d85a43`

`https://img.shields.io/badge/Python-3.10%2B-blue`
`https://img.shields.io/badge/FastAPI-Backend-green`
`https://img.shields.io/badge/Streamlit-Frontend-red`
`https://img.shields.io/badge/OpenAI-API-black`
`https://img.shields.io/badge/arXiv-Integrated-orange`

A next‑generation academic assistant that generates **APA 7 citations** from:

- **Uploaded PDF research papers**
- **arXiv papers fetched automatically via search**
- **OpenAI GPT‑4.1 / GPT‑4o / GPT‑4o‑mini models**

Built with a clean **microservice architecture**:

- **Backend:** FastAPI (PDF extraction, arXiv ingestion, LLM citation generation)  
- **Frontend:** Streamlit (UI for uploads, arXiv search, model selection)

Perfect for **scientific writing**, **research workflows**, and **rapid literature processing**.

---

# 🚀 Features

### 🔍 Hybrid Corpus (PDFs + arXiv)
Upload your own PDFs **and** automatically fetch arXiv papers by keyword.

### 🧠 OpenAI Model Support
Choose from:
- `gpt-4.1`
- `gpt-4o`
- `gpt-4o-mini` (default)
- `gpt-4.1-mini`

Automatic fallback to lightweight models if needed.

### 📚 APA 7 Citation Generator
- One citation per line  
- No hallucinated metadata  
- Uses “n.d.” or “Unknown” when fields are missing  
- Alphabetically sorted when possible  

### 🧩 RAG‑Ready PDF Extraction
Uses `pymupdf4llm` for robust extraction of academic PDFs.

### 🖥️ Desktop Launchers
Start/stop the entire application with simple scripts.

---

# 🛠️ Setup (using **uv**, recommended)

This project is optimized for **uv**, the ultra‑fast Python package manager.

## 1. Clone the repository
```bash
git clone https://github.com/Aylinee/APA7_RAG_Local
cd APA7_RAG_Local
```

## 2. Create the environment
```bash
uv venv
```

## 3. Activate the environment
**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
.venv\Scripts\Activate.ps1
```

## 4. Install dependencies
```bash
uv pip install -r requirements.txt
```

## 5. Add your OpenAI API key  
Create a `.env` file inside the **backend/** folder:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

# ▶️ Running the Application

You need **two terminals** (or use the desktop launchers below).

---

## **Terminal 1 — Start Backend**
```bash
cd backend
uv run python main.py
```

Backend runs at:
```
http://127.0.0.1:8001
```

---

## **Terminal 2 — Start Frontend**
```bash
cd frontend
uv run streamlit run app.py
```

Frontend runs at:
```
http://localhost:8501
```

---

# 🖥️ Desktop Launchers (macOS/Linux/Windows)

These scripts let you start/stop the entire system like a desktop app.

---

## **start_app.sh** (macOS/Linux)

```bash
#!/bin/bash
echo "Starting APA7 RAG Application..."

# Start backend
cd backend
uv run python main.py &
BACKEND_PID=$!
cd ..

# Start frontend
cd frontend
uv run streamlit run app.py &
FRONTEND_PID=$!
cd ..

echo $BACKEND_PID > backend.pid
echo $FRONTEND_PID > frontend.pid

echo "Application started."
```

Make executable:
```bash
chmod +x start_app.sh
```

---

## **stop_app.sh** (macOS/Linux)

```bash
#!/bin/bash
echo "Stopping APA7 RAG Application..."

if [ -f backend.pid ]; then
    kill $(cat backend.pid)
    rm backend.pid
fi

if [ -f frontend.pid ]; then
    kill $(cat frontend.pid)
    rm frontend.pid
fi

echo "Application stopped."
```

---

## **Windows Start Script (start_app.bat)**

```bat
@echo off
echo Starting APA7 RAG Application...

start cmd /k "cd backend && uv run python main.py"
start cmd /k "cd frontend && uv run streamlit run app.py"

echo Application started.
```

---

## **Windows Stop Script (stop_app.bat)**

```bat
@echo off
echo Stopping APA7 RAG Application...

taskkill /IM python.exe /F
taskkill /IM streamlit.exe /F

echo Application stopped.
```

---

# 📄 License
MIT License
