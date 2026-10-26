# XAUUSD Terminal

A real-market XAUUSD signal dashboard with:
- live market data from OANDA
- fallback demo mode
- technical analysis
- AI summary with Gemini
- dark trading-terminal UI

## Stack
- Frontend: Next.js + TypeScript
- Backend: FastAPI
- Data: OANDA
- AI: Gemini API
- Hosting: Vercel + Render/Railway
- Database: PostgreSQL-ready

## Run locally

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open:
- http://localhost:3000

## Real data setup
Add your keys to backend/.env:

```env
OANDA_API_KEY=your_key_here
OANDA_ACCOUNT_ID=your_account_id_here
OANDA_BASE_URL=https://api-fxpractice.oanda.com

GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-1.5-flash
```

If keys are missing, app falls back to demo mode.

## Deployment
- push repo to GitHub
- deploy frontend on Vercel
- deploy backend on Render or Railway
- add environment variables in hosting dashboard

## Important
This is analytical support software, not guaranteed financial advice.
