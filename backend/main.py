import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine, Base, SessionLocal
from config import settings
from models.question import Question

from routers import auth, questions, quiz, analytics, ai_generate, peers

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GATE CS Quiz Master API",
    description="Backend API for GATE CS Quiz application with Peer Analytics",
    version="1.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-seed database if empty on startup
@app.on_event("startup")
def startup_db_check():
    db = SessionLocal()
    try:
        count = db.query(Question).count()
        if count == 0:
            print("[Startup] Database is empty. Auto-seeding 693 questions...")
            seed_file = os.path.join(os.path.dirname(__file__), "seed_data", "questions_full_693.json")
            if os.path.exists(seed_file):
                with open(seed_file, "r", encoding="utf-8") as f:
                    q_list = json.load(f)
                new_objs = []
                for q in q_list:
                    new_objs.append(Question(
                        id=q.get("id"),
                        subject=q.get("subject"),
                        topic=q.get("topic"),
                        year=q.get("year"),
                        set_number=q.get("set_number"),
                        question_type=q.get("question_type"),
                        difficulty=q.get("difficulty"),
                        marks=q.get("marks"),
                        question_text=q.get("question_text"),
                        options=json.dumps(q.get("options")) if q.get("options") else None,
                        correct_answer=q.get("correct_answer"),
                        nat_tolerance=q.get("nat_tolerance", 0.0),
                        explanation=q.get("explanation"),
                        is_pyq=q.get("is_pyq", True)
                    ))
                db.bulk_save_objects(new_objs)
                db.commit()
                print(f"[Startup] Successfully seeded {len(new_objs)} questions into the database!")
            else:
                print(f"[Startup] Warning: Seed file not found at {seed_file}")
        else:
            # If DB already has questions, check if any legacy question type mismatches exist (e.g. Q644 as NAT)
            sample_legacy = db.query(Question).filter(Question.id == 644, Question.question_type == 'NAT').first()
            if sample_legacy:
                print("[Startup] Detected legacy question types. Syncing corrected questions from seed...")
                seed_file = os.path.join(os.path.dirname(__file__), "seed_data", "questions_full_693.json")
                if os.path.exists(seed_file):
                    with open(seed_file, "r", encoding="utf-8") as f:
                        q_list = json.load(f)
                    for q in q_list:
                        db.query(Question).filter(Question.id == q.get("id")).update({
                            Question.question_type: q.get("question_type"),
                            Question.options: json.dumps(q.get("options")) if q.get("options") else None,
                            Question.correct_answer: q.get("correct_answer"),
                            Question.nat_tolerance: q.get("nat_tolerance", 0.0),
                            Question.explanation: q.get("explanation")
                        })
                    db.commit()
                    print("[Startup] Successfully synced all updated question types and options!")
            else:
                print(f"[Startup] Database verified with {count} questions.")
    except Exception as e:
        print(f"[Startup] Error checking/seeding database: {e}")
    finally:
        db.close()

# API Routers
app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(quiz.router)
app.include_router(analytics.router)
app.include_router(ai_generate.router)
app.include_router(peers.router)

# Production Frontend Static Serving (if frontend/dist exists)
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        # Allow API routes to be handled by routers
        if full_path.startswith("api/") or full_path == "api":
            return {"error": "API route not found"}
        # Serve static file if exists
        target = os.path.join(frontend_dist, full_path)
        if os.path.isfile(target):
            return FileResponse(target)
        # Fallback to index.html for client-side routing
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "message": "GATE CS Quiz Master API",
            "version": "1.1.0",
            "docs": "/docs",
            "status": "online"
        }
