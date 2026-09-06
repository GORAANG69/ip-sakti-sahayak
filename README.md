# IP-SAKTI Sahayak

**Turn a rough innovation description into a structured, evidence-grounded IP readiness check.**

IP-SAKTI Sahayak helps an inventor go from "I built something" to "I understand how a patent examiner would see it." Describe your innovation in plain language, and the app breaks it into its patentable building blocks, argues both sides (inventor vs. examiner), flags IP risks (novelty, traditional knowledge, regulatory, biodiversity/ABS), and lays out a practical next-steps pathway — all backed by a retrievable evidence base, not just free-form AI chat.

Built as a full-stack demo: **FastAPI backend with Google Gemini**, **React/TypeScript frontend**, and a graceful fallback system so the app never breaks or shows raw errors even if the AI service is unavailable.

## What it does

- **Innovation DNA** — breaks an innovation into 9 structured elements (problem, mechanism, novel elements, advantages, etc.)
- **Two-Sided AI** — generates the patent examiner's likely objections *and* the inventor's counter-explanation, side by side
- **IP Risk Radar** — flags risk areas (novelty/prior art, traditional knowledge, regulatory, biodiversity/ABS, jurisdiction, missing evidence)
- **Pathway** — practical staged next steps toward filing
- **AI Copilot** — evidence-grounded chat for follow-up questions
- Every AI response falls back to a well-written, on-topic answer if Gemini is unreachable — the demo never shows an error, even offline

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

---

*Demo knowledge records are clearly marked as demo data. This application is decision support, not legal advice.*
