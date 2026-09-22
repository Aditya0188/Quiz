# 🎯 GATE CS Quiz Master (36-Year PYQs, Study Buddy & 24/7 Cloud App)

A modern, full-stack application designed for GATE Computer Science & Information Technology aspirants. It features an authentic **36-year archive of GATE CS PYQs (1991–2026, All Sets)**, complete **65-question official papers (2024, 2025, 2026)**, an authentic **GATE CBT interface**, **Study Buddy peer collaboration**, **36-year paper intelligence analysis**, and **24/7 cloud deployment** support.

---

## ✨ Key Features

- **📚 36 Years of Authentic GATE CS PYQs (1991 – 2026)**:
  - 693 100% unique curated questions across all 11 GATE CS subjects.
  - Complete official **65-Question / 100-Mark Papers** for **GATE 2026**, **GATE 2025**, and **GATE 2024**.
  - All 3 official question formats: **MCQ** (Multiple Choice), **MSQ** (Multiple Select), and **NAT** (Numerical Answer Type).
  - Clean LaTeX mathematical equations, C/C++ code blocks, and step-by-step solutions.

- **🤝 Study Buddy & Peer Collaboration Hub**:
  - Compare performance side-by-side with a friend (accuracy, average marks, test scores).
  - Head-to-head subject accuracy comparison chart across all 11 GATE subjects.
  - Shared live activity feed of recent test submissions.
  - **"Review Test Paper"**: Inspect each other's completed test papers to learn from mistakes and discuss solutions.

- **📊 36-Year Paper Intelligence & Analysis**:
  - Detailed breakdown of marks and question counts for every year from 1991 to 2026.
  - High-yield topic frequency trends over 36 years.
  - One-click practice for any previous year examination.

- **🖥️ Authentic GATE CBT Interface**:
  - Official layout: Question view (70%) + Color-coded Question Palette (30%).
  - Live Countdown Timer with automatic submission upon expiry.
  - Full customizability: timer duration (5 to 180 mins) and question count (5 to 65 questions).
  - Smart anti-repetition engine ensures fresh questions on every attempt.

- **⚖️ Official GATE Marking Scheme**:
  - **MCQ**: +1 or +2 for correct; **-1/3** or **-2/3** negative marking for incorrect.
  - **MSQ**: +1 or +2 for all correct; **0 negative marking** (all-or-nothing evaluation).
  - **NAT**: +1 or +2 with numerical tolerance evaluation; **0 negative marking**.

- **🌐 24/7 Cloud Ready**:
  - Pre-configured `Dockerfile` and `render.yaml` for 1-click cloud hosting on Render.com.
  - Cloud PostgreSQL compatibility (Neon.tech / Supabase) with automatic question database bootstrapping.

---

## 🏗️ Architecture & Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18, Vite, TailwindCSS, KaTeX, Recharts, Lucide Icons |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy, Direct Bcrypt, PyJWT, Pydantic v2 |
| **Database** | SQLite (Local) / PostgreSQL (Cloud via Neon/Supabase) |
| **Cloud** | Docker, Render, Neon.tech |

---

## 🚀 Quick Start (Local Run)

Double-click `start_app.bat` in the root folder. It boots both the backend (`http://localhost:8000`) and frontend (`http://localhost:5173`) and opens your browser.

---

## ☁️ 24/7 Cloud Deployment (PC Off Mode)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for full instructions on hosting the app online for free on **Render.com** and **Neon.tech**.
