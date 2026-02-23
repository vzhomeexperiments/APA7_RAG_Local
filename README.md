# ⚡ AI‑Powered APA 7 + BibTeX Generator  
*A research‑grade citation assistant for PDFs + arXiv*

- **OpenAI-powered backend**
- **arXiv integration**
- **APA + BibTeX generation**
- **Pattern B1‑B (prepare once → download twice)**
- **uv‑based setup**
- **Desktop launchers for Windows/macOS/Linux**

It’s written to feel professional, research‑ready, and easy for collaborators to follow.

---


`https://img.shields.io/badge/Python-3.10%2B-blue`
`https://img.shields.io/badge/FastAPI-Backend-green`
`https://img.shields.io/badge/Streamlit-Frontend-red`
`https://img.shields.io/badge/OpenAI-API-black`
`https://img.shields.io/badge/arXiv-Integrated-orange`

This project provides a **next‑generation citation workflow** for researchers.  
Upload your PDFs, optionally search arXiv, and generate:

- **APA 7 Word (.docx)** bibliography  
- **BibTeX (.bib)** file for Zotero, Mendeley, EndNote, LaTeX  

All powered by **OpenAI GPT‑4 models** and a clean **microservice architecture**.

---

# 🚀 Features

### 🧠 OpenAI‑Powered Citation Generation
- APA 7 formatting  
- BibTeX conversion  
- Automatic fallback to lightweight models  

### 📚 Hybrid Corpus (PDFs + arXiv)
- Upload any number of PDFs  
- Add arXiv papers via keyword search  
- Extracts text using `pymupdf4llm`  

### 🧩 Microservice Architecture
- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Pattern B1‑B:**  
  - One “prepare” call  
  - Two download endpoints (APA + BibTeX)  
  - Only **one** LLM call → faster, cheaper, consistent  

### 🖥️ Desktop Launchers
Start/stop the entire application with one click (Windows/macOS/Linux).

---

# 🛠️ Installation (using `uv` — recommended)

This project is optimized for **uv**, the ultra‑fast Python package manager.

## 1. Clone the repository
```bash
git clone https://github.com/Aylinee/APA7_RAG_Local
cd APA7_RAG_Local
```

## 2. Create a virtual environment
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

You need **two terminals**, or use the launchers below.

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

# 🧪 How It Works

### 1. Upload PDFs  
### 2. (Optional) Enter arXiv search query  
### 3. Click **Prepare Bibliography**  
Backend will:
- Extract text from PDFs  
- Fetch arXiv papers  
- Generate APA citations  
- Convert APA → BibTeX  
- Store both files under a `session_id`  

### 4. Download:
- **APA 7 Word file**  
- **BibTeX file**  

---

# 🖥️ Desktop Launchers

These scripts let you start/stop the app like a desktop program.

---

## Windows — `start_app.bat`

```bat
@echo off
echo Starting APA7 RAG Application...

set BASE_DIR=%USERPROFILE%\Documents\GitHub\APA7_RAG_Local

start "APA7 Backend" cmd /k "cd /d %BASE_DIR%\backend && uv run python main.py"
start "APA7 Frontend" cmd /k "cd /d %BASE_DIR%\frontend && uv run streamlit run app.py"

echo Application started.
```

---

## Windows — `stop_app.bat`

```bat
@echo off
echo Stopping APA7 RAG Application...

for /f "tokens=2 delims=," %%a in ('tasklist /v /fo csv ^| findstr /i "APA7 Backend"') do taskkill /PID %%a /F
for /f "tokens=2 delims=," %%a in ('tasklist /v /fo csv ^| findstr /i "APA7 Frontend"') do taskkill /PID %%a /F

echo Application stopped.
```

---

## macOS/Linux — `start_app.sh`

```bash
#!/bin/bash
echo "Starting APA7 RAG Application..."

BASE_DIR="$HOME/Documents/GitHub/APA7_RAG_Local"

cd "$BASE_DIR/backend"
uv run python main.py &
BACKEND_PID=$!

cd "$BASE_DIR/frontend"
uv run streamlit run app.py &
FRONTEND_PID=$!

echo $BACKEND_PID > "$BASE_DIR/backend.pid"
echo $FRONTEND_PID > "$BASE_DIR/frontend.pid"

echo "Application started."
```

---

## macOS/Linux — `stop_app.sh`

```bash
#!/bin/bash
echo "Stopping APA7 RAG Application..."

BASE_DIR="$HOME/Documents/GitHub/APA7_RAG_Local"

if [ -f "$BASE_DIR/backend.pid" ]; then
    kill $(cat "$BASE_DIR/backend.pid")
    rm "$BASE_DIR/backend.pid"
fi

if [ -f "$BASE_DIR/frontend.pid" ]; then
    kill $(cat "$BASE_DIR/frontend.pid")
    rm "$BASE_DIR/frontend.pid"
fi

echo "Application stopped."
```

---

# 📄 License
MIT License

