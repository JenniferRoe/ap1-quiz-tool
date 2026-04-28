from flask import Flask, render_template, request
import sqlite3
import random
from collections import Counter
from datetime import datetime

app = Flask(__name__)

DB_PATH = "questions.db"
WRONG_FILE = "wrong_questions.txt"


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_all_questions():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, question, answer_type, option_a, option_b, option_c, option_d,
                   correct_answer, explanation, category, keywords
            FROM questions
        """)
        return cursor.fetchall()


def get_categories():
    questions = get_all_questions()
    return sorted(set(q[9] for q in questions))


def get_questions_by_category(category):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, question, answer_type, option_a, option_b, option_c, option_d,
                   correct_answer, explanation, category, keywords
            FROM questions
            WHERE category = ?
        """, (category,))
        return cursor.fetchall()


def get_question_by_id(question_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, question, answer_type, option_a, option_b, option_c, option_d,
                   correct_answer, explanation, category, keywords
            FROM questions
            WHERE id = ?
        """, (question_id,))
        return cursor.fetchone()


def check_text_answer(user_answer, keywords):
    if not keywords:
        return False

    keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    user_answer = user_answer.lower()

    matches = sum(1 for keyword in keyword_list if keyword in user_answer)
    required_matches = max(1, min(2, len(keyword_list)))

    return matches >= required_matches


# 🔥 NEU: Fortschritt speichern
def save_progress(question_id, category, is_correct):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_progress (question_id, category, is_correct, answered_at)
            VALUES (?, ?, ?, ?)
        """, (
            question_id,
            category,
            1 if is_correct else 0,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()


def save_wrong_question(category, question_text):
    with open(WRONG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{category}||{question_text}\n")


def load_wrong_entries():
    try:
        with open(WRONG_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

        entries = []
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "||" in line:
                category, question_text = line.split("||", 1)
                entries.append((category.strip(), question_text.strip()))

        return entries

    except FileNotFoundError:
        return []


# 🔥 NEU: Statistik aus DB
def get_progress_stats():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM user_progress")
        total_answers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM user_progress WHERE is_correct = 1")
        correct_answers = cursor.fetchone()[0]

        cursor.execute("""
            SELECT category, COUNT(*)
            FROM user_progress
            WHERE is_correct = 0
            GROUP BY category
            ORDER BY COUNT(*) DESC
        """)
        weak_categories = cursor.fetchall()

    percentage = round((correct_answers / total_answers) * 100) if total_answers else 0

    return total_answers, correct_answers, percentage, weak_categories


@app.route("/")
def index():
    questions = get_all_questions()
    categories = get_categories()
    wrong_entries = load_wrong_entries()

    return render_template(
        "index.html",
        question_count=len(questions),
        category_count=len(categories),
        wrong_count=len(wrong_entries)
    )


@app.route("/categories")
def categories():
    categories = get_categories()
    return render_template("categories.html", categories=categories)


@app.route("/quiz")
def quiz():
    category = request.args.get("category")

    if category:
        questions = get_questions_by_category(category)
    else:
        questions = get_all_questions()

    if not questions:
        return "Keine Fragen vorhanden."

    question = random.choice(questions)

    return render_template(
        "quiz.html",
        question=question,
        category=category
    )


@app.route("/check", methods=["POST"])
def check():
    question_id = request.form.get("question_id")
    user_answer = request.form.get("answer", "")
    category_filter = request.form.get("category_filter")

    question = get_question_by_id(question_id)

    if not question:
        return "Frage nicht gefunden."

    answer_type = question[2]
    correct_answer = question[7]
    explanation = question[8]
    category = question[9]
    keywords = question[10]

    if answer_type == "multiple_choice":
        is_correct = user_answer.upper() == correct_answer.upper()
    else:
        is_correct = check_text_answer(user_answer, keywords)

    # 🔥 Fortschritt speichern
    save_progress(question[0], category, is_correct)

    if not is_correct:
        save_wrong_question(category, question[1])

    return render_template(
        "result.html",
        question=question,
        user_answer=user_answer,
        is_correct=is_correct,
        correct_answer=correct_answer,
        explanation=explanation,
        category_filter=category_filter
    )


@app.route("/all-questions")
def all_questions():
    questions = get_all_questions()
    return render_template("all_questions.html", questions=questions)


@app.route("/progress")
def progress():
    total_answers, correct_answers, percentage, weak_categories = get_progress_stats()

    return render_template(
        "progress.html",
        total_answers=total_answers,
        correct_answers=correct_answers,
        percentage=percentage,
        weak_categories=weak_categories
    )


from database import create_database

create_database()

if __name__ == "__main__":
    app.run(debug=True)