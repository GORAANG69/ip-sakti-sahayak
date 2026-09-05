# IP-SAKTI Sahayak

Fresh full-stack demo build for innovation and IP decision support.

## Stack
React + TypeScript + Vite + Tailwind CSS | FastAPI + SQLite | Google Gemini

## Windows setup

Backend:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

Frontend (new terminal):
```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL.

### Demo login
With `DEMO_MODE=true`, any non-empty ID/email + any non-empty password works.
Examples: `judge / judge123`, `test@gmail.com / hello`, `anything / anything`.

### Gemini
Put the key only in `backend/.env`:
`GEMINI_API_KEY=...`
The frontend never receives the key. If Gemini is unavailable, the app uses a deterministic evidence fallback or abstains.

Demo knowledge records are clearly marked as demo data. This application is decision support, not legal advice.
