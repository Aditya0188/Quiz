import json
import random
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.question import Question
from models.quiz_session import QuizSession

# Canonical subject normalization map: resolves full names, abbreviations, and aliases to exact DB names
SUBJECT_MAP = {
    # OS
    "os": "OS",
    "operating systems": "OS",
    "operating system": "OS",
    "os - operating systems": "OS",
    # COA
    "coa": "COA",
    "computer organization & architecture": "COA",
    "computer organization and architecture": "COA",
    "computer organization": "COA",
    # TOC
    "toc": "TOC",
    "theory of computation": "TOC",
    "automata": "TOC",
    # DBMS
    "dbms": "DBMS",
    "database management systems": "DBMS",
    "databases": "DBMS",
    "database": "DBMS",
    # Programming & DS
    "programming & ds": "Programming & DS",
    "programming & data structures": "Programming & DS",
    "programming and data structures": "Programming & DS",
    "data structures": "Programming & DS",
    "pds": "Programming & DS",
    # Engineering Mathematics
    "engineering mathematics": "Engineering Mathematics",
    "engineering math": "Engineering Mathematics",
    "mathematics": "Engineering Mathematics",
    "math": "Engineering Mathematics",
    "em": "Engineering Mathematics",
    # General Aptitude
    "general aptitude": "General Aptitude",
    "aptitude": "General Aptitude",
    "ga": "General Aptitude",
    # Digital Logic
    "digital logic": "Digital Logic",
    "digital logic design": "Digital Logic",
    "dl": "Digital Logic",
    # Algorithms
    "algorithms": "Algorithms",
    "algo": "Algorithms",
    # Compiler Design
    "compiler design": "Compiler Design",
    "compiler": "Compiler Design",
    "cd": "Compiler Design",
    # Computer Networks
    "computer networks": "Computer Networks",
    "networks": "Computer Networks",
    "cn": "Computer Networks",
}

ALL_DB_SUBJECTS = [
    "Algorithms", "COA", "Compiler Design", "Computer Networks", "DBMS",
    "Digital Logic", "Engineering Mathematics", "General Aptitude", "OS",
    "Programming & DS", "TOC"
]

def normalize_subject(subj: str) -> str:
    if not subj:
        return ""
    clean = subj.strip().lower()
    return SUBJECT_MAP.get(clean, subj.strip())

TOPIC_MAP = {
    "DP": "Dynamic Programming",
    "Divide-Conquer": "Divide & Conquer",
    "Greedy": "Greedy Algorithms",
    "Sorting & Hashing": "Sorting & Searching",
    "NP-Completeness": "NP-Completeness & Complexity",
    "Addressing Modes": "Machine Instructions & Addressing Modes",
    "Cache Memory": "Memory Hierarchy & Cache",
    "I/O": "I/O Interface & DMA",
    "I/O and DMA": "I/O Interface & DMA",
    "Pipelining": "Instruction Pipelining",
    "Computer Arithmetic": "Number Representations & Computer Arithmetic",
    "Code Optimization": "Code Optimization & Data Flow Analysis",
    "Parsing": "Parsing Techniques",
    "SDT": "Syntax-Directed Translation",
    "Data Link Layer": "Data Link Layer & Framing",
    "Network Layer (IP/Subnetting)": "Network Layer & IPv4/IPv6",
    "Transport Layer (TCP)": "Transport Layer & TCP/UDP",
    "Application Layer": "Application Layer Protocols",
    "B/B+ Trees": "Indexing & B/B+ Trees",
    "Normalization": "Normalization & Functional Dependencies",
    "SQL & Relational Algebra": "Relational Algebra & Relational Calculus",
    "Transactions": "Transactions & Concurrency Control",
    "Transactions & Concurrency": "Transactions & Concurrency Control",
    "Boolean Algebra": "Boolean Algebra & K-Maps",
    "Number Representations": "Number Representations & Computer Arithmetic",
    "Discrete Math": "Discrete Mathematics",
    "Probability": "Probability & Statistics",
    "Quantitative": "Quantitative Aptitude",
    "Verbal": "Verbal Aptitude",
    "Analytical": "Analytical Aptitude",
    "Processes": "Processes & Threads",
    "Synchronization & Deadlocks": "Synchronization",
    "C Programming": "C Programming & Pointers",
    "Heaps": "Binary Heaps & Priority Queues",
    "Trees": "Trees & Binary Search Trees",
    "Trees & BST": "Trees & Binary Search Trees",
    "CFG & PDA": "Context-Free Grammars & Pushdown Automata",
    "Finite Automata": "Finite Automata & Regular Languages",
    "Turing Machines": "Turing Machines & Undecidability",
}

def normalize_topic(topic: str) -> str:
    if not topic:
        return ""
    clean = topic.strip()
    return TOPIC_MAP.get(clean, clean)

def generate_quiz(db: Session, user_id: int, config: dict):
    raw_subjects = config.get("subjects", [])
    raw_topics = config.get("topics", [])
    difficulty = config.get("difficulty", "mixed")
    num_questions = int(config.get("num_questions", 10))
    question_types = config.get("question_types", ["MCQ", "MSQ", "NAT"])
    year_range = config.get("year_range", (1991, 2026))

    # Normalize subject list
    normalized_subjects = []
    is_mix_or_all = False

    if not raw_subjects:
        is_mix_or_all = True
    else:
        for s in raw_subjects:
            s_clean = str(s).strip()
            if s_clean.upper() in ["MIX", "ALL", "CUSTOM MIX", "ALL SUBJECTS", ""]:
                is_mix_or_all = True
                break
            norm = normalize_subject(s_clean)
            if norm:
                normalized_subjects.append(norm)

    # Normalize & expand topics list to include both canonical and raw names
    expanded_topics = []
    if raw_topics:
        for t in raw_topics:
            t_clean = str(t).strip()
            norm_t = normalize_topic(t_clean)
            if norm_t and norm_t not in expanded_topics:
                expanded_topics.append(norm_t)
            if t_clean and t_clean not in expanded_topics:
                expanded_topics.append(t_clean)

    query = db.query(Question)

    # Subject filter: if specific subject(s) are chosen, STRICTLY filter to those subjects
    if not is_mix_or_all and normalized_subjects:
        query = query.filter(Question.subject.in_(normalized_subjects))
    
    # Topic filter: STRICT isolation
    if expanded_topics:
        query = query.filter(Question.topic.in_(expanded_topics))

    # Difficulty filter
    if difficulty and difficulty.lower() != "mixed":
        query = query.filter(Question.difficulty == difficulty.lower())

    # Question types filter
    if question_types and len(question_types) > 0:
        query = query.filter(Question.question_type.in_(question_types))

    # Year range filter
    if year_range:
        query = query.filter(Question.year >= year_range[0], Question.year <= year_range[1])

    all_questions = query.all()

    # STRICT Fallback: If no questions matched due to restrictive difficulty/type,
    # relax difficulty and question_types ONLY, BUT NEVER DROP SUBJECT OR TOPIC!
    if not all_questions:
        fallback_query = db.query(Question)
        if not is_mix_or_all and normalized_subjects:
            fallback_query = fallback_query.filter(Question.subject.in_(normalized_subjects))
        if expanded_topics:
            # Topic filter remains strictly enforced!
            fallback_query = fallback_query.filter(Question.topic.in_(expanded_topics))
        if year_range:
            fallback_query = fallback_query.filter(Question.year >= year_range[0], Question.year <= year_range[1])
        all_questions = fallback_query.all()

    # If still empty (e.g. year range was too narrow), try without year restriction but KEEP topic & subject!
    if not all_questions:
        relaxed_query = db.query(Question)
        if not is_mix_or_all and normalized_subjects:
            relaxed_query = relaxed_query.filter(Question.subject.in_(normalized_subjects))
        if expanded_topics:
            relaxed_query = relaxed_query.filter(Question.topic.in_(expanded_topics))
        all_questions = relaxed_query.all()

    if not all_questions:
        return []

    # -------------------------------------------------------------
    # SMART ANTI-REPETITION ENGINE:
    # Retrieve ALL questions that this user has ever seen across past sessions.
    # -------------------------------------------------------------
    past_sessions = db.query(QuizSession).filter(QuizSession.user_id == user_id).order_by(QuizSession.started_at.desc()).all()
    seen_q_ids_set = set()
    seen_q_ids_ordered = []

    for s in past_sessions:
        # Check questions_order (all served questions, even unsubmitted)
        if s.questions_order:
            try:
                q_list = json.loads(s.questions_order)
                for qid in q_list:
                    qid_int = int(qid)
                    if qid_int not in seen_q_ids_set:
                        seen_q_ids_set.add(qid_int)
                        seen_q_ids_ordered.append(qid_int)
            except Exception:
                pass
        # Check evaluated responses
        if s.responses:
            try:
                res_dict = json.loads(s.responses)
                for qid in res_dict.keys():
                    qid_int = int(qid)
                    if qid_int not in seen_q_ids_set:
                        seen_q_ids_set.add(qid_int)
                        seen_q_ids_ordered.append(qid_int)
            except Exception:
                pass

    # Partition available questions into UNSEEN vs SEEN
    unseen_pool = [q for q in all_questions if q.id not in seen_q_ids_set]
    seen_pool = [q for q in all_questions if q.id in seen_q_ids_set]

    # Shuffle unseen pool for randomness
    random.shuffle(unseen_pool)

    selected = []
    if len(unseen_pool) >= num_questions:
        # 100% completely brand-new, unseen questions! Zero repetition!
        selected = unseen_pool[:num_questions]
    else:
        # Take all remaining unseen questions first
        selected = list(unseen_pool)
        needed = num_questions - len(selected)

        # For remaining slots, pick from seen_pool sorted by LEAST RECENTLY SEEN
        # Higher index in seen_q_ids_ordered means seen longer ago
        seen_order_map = {qid: idx for idx, qid in enumerate(seen_q_ids_ordered)}
        seen_pool.sort(key=lambda q: seen_order_map.get(q.id, 999999), reverse=True)

        selected.extend(seen_pool[:needed])

    # Final shuffle
    random.shuffle(selected)
    return selected

def evaluate_quiz(db: Session, session_id: int, responses: dict):
    session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not session:
        return None

    questions_order = json.loads(session.questions_order)
    questions = db.query(Question).filter(Question.id.in_(questions_order)).all()
    q_dict = {q.id: q for q in questions}

    total_score = 0.0
    max_score = 0.0
    correct = 0
    wrong = 0
    unanswered = 0

    evaluated_responses = {}

    for q_id_str in questions_order:
        q_id = int(q_id_str)
        q = q_dict.get(q_id)
        if not q:
            continue

        max_score += q.marks
        user_resp = responses.get(str(q_id), {})
        ans = user_resp.get("answer")

        evaluated_responses[str(q_id)] = {
            "user_answer": ans,
            "correct_answer": q.correct_answer,
            "marks_awarded": 0.0,
            "status": "unanswered"
        }

        if ans is None or str(ans).strip() == "":
            unanswered += 1
            continue

        is_correct = False
        ans_str = str(ans).strip()

        if q.question_type == "MCQ":
            if ans_str.upper() == str(q.correct_answer).strip().upper():
                is_correct = True
                total_score += q.marks
            else:
                total_score -= (q.marks / 3.0)
        elif q.question_type == "MSQ":
            user_opts = set(x.strip().upper() for x in ans_str.split(",") if x.strip())
            corr_opts = set(x.strip().upper() for x in str(q.correct_answer).split(",") if x.strip())
            if user_opts == corr_opts:
                is_correct = True
                total_score += q.marks
        elif q.question_type == "NAT":
            try:
                ans_val = float(ans_str)
                corr_val = float(str(q.correct_answer).strip())
                tolerance = q.nat_tolerance if q.nat_tolerance is not None else 0.01
                if abs(ans_val - corr_val) <= tolerance:
                    is_correct = True
                    total_score += q.marks
            except ValueError:
                pass

        if is_correct:
            correct += 1
            evaluated_responses[str(q_id)]["marks_awarded"] = float(q.marks)
            evaluated_responses[str(q_id)]["status"] = "correct"
        else:
            wrong += 1
            evaluated_responses[str(q_id)]["marks_awarded"] = -(q.marks / 3.0) if q.question_type == "MCQ" else 0.0
            evaluated_responses[str(q_id)]["status"] = "wrong"

    session.score = round(total_score, 2)
    session.max_score = round(max_score, 2)
    session.correct_count = correct
    session.wrong_count = wrong
    session.unanswered_count = unanswered
    session.responses = json.dumps(evaluated_responses)
    session.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(session)
    return session
