# 24/7 Cloud Deployment Guide: GATE CS Master

This guide explains how to host your **GATE CS Master** app online 24/7 for **FREE ($0)** so that both you and your friend can practice anytime, share data, compare scores, and review each other's quiz papers **even when your personal PC is turned off**.

---

## 🏗️ Architecture Overview

```
                        ┌───────────────────────────────┐
                        │   Free Cloud Database (Neon)   │
                        │   • PostgreSQL (500MB Free)   │
                        │   • Stores all 693 Questions  │
                        │   • Stores You & Friend Data  │
                        └──────────────▲────────────────┘
                                       │
                                       │ (24/7 Live Connection)
                                       │
                        ┌──────────────┴────────────────┐
                        │   Cloud Web Service (Render)  │
                        │   • FastAPI + React Built-in  │
                        │   • URL: gate-cs.onrender.com │
                        └──────────────▲────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                │                                             │
      ┌─────────┴─────────┐                         ┌─────────┴─────────┐
      │   Your Browser    │                         │  Friend's Browser │
      │  (PC / Phone)     │                         │   (PC / Phone)    │
      └───────────────────┘                         └───────────────────┘
```

---

## ⚡ Step 1: Create a Free Cloud Database on Neon.tech (60 Seconds)

1. Open **[Neon.tech](https://neon.tech)** in your browser and click **"Sign Up"** (use your Google or GitHub account).
2. Click **"Create Project"**:
   - Project Name: `gate-quiz-db`
   - Region: Select nearest (e.g., `AWS Asia Pacific (Singapore)` or `US East`).
3. On the project dashboard, you will see your **Connection String**:
   - Make sure **"Pooled connection"** is selected.
   - It will look like this:
     ```text
     postgresql://neondb_owner:npg_xxxxxx@ep-cool-fog-xxxxxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
     ```
   - **Copy this connection string.**

---

## 🚀 Step 2: Push Project to GitHub

If you haven't initialized a git repo yet, run these commands in your project folder (`gate-quiz-app`):

```bash
cd C:\Users\anjan\.gemini\antigravity\scratch\gate-quiz-app

# 1. Initialize git
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "GATE CS Master with Study Buddy and 24/7 cloud deployment"

# 4. Create a new repository on GitHub (e.g. gate-cs-master) and link it:
git remote add origin https://github.com/<your-username>/gate-cs-master.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 3: Deploy on Render.com (Free Web Service)

1. Open **[Render.com](https://render.com)** and sign in with your GitHub account.
2. Click **"New +"** in the top-right corner and select **"Web Service"**.
3. Choose **"Build and deploy from a Git repository"** and select your `gate-cs-master` repository.
4. Fill in the deployment settings:
   - **Name**: `gate-cs-master` (or any name you like)
   - **Region**: Choose closest to you (e.g. `Singapore` or `Oregon`)
   - **Language**: `Docker` (Render will automatically detect the root `Dockerfile`!)
   - **Instance Type**: **Free** ($0/month)
5. Under **"Environment Variables"**, add:
   - **Key**: `DATABASE_URL`
   - **Value**: *(Paste your Neon connection string from Step 1)*
   - **Key**: `SECRET_KEY`
   - **Value**: `gate-super-secret-key-2026-production`
6. Click **"Create Web Service"**.

---

## 🎉 Step 4: Access and Share with Your Friend!

1. Render will build the container (takes ~2-3 minutes) and show a green **"Live"** status.
2. On startup, the backend automatically detects that the cloud database is brand new and **auto-seeds all 693 authentic GATE questions** in seconds!
3. Render gives you a public HTTPS URL:
   ```text
   https://gate-cs-master.onrender.com
   ```
4. **Share this link with your friend!**
   - You register your account (`Anjan`).
   - Your friend registers her account (`Friend Name`).
   - Both of you can click **"Study Buddy"** in the top navbar to:
     - See each other's test attempts in real time.
     - Compare subject accuracy side-by-side.
     - Click **"Review Test Paper"** on any attempt to inspect questions, student answers, and detailed step-by-step explanations.
   - **Your PC can be turned off completely!** The app and database will remain live 24/7 on the cloud.
