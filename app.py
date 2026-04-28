from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)


def get_all_questions():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, question, answer_type, option_a, option_b, option_c, option_d,
               correct_answer, explanation, category, keywords
        FROM questions
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def get_question_by_id(question_id):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, question, answer_type, option_a, option_b, option_c, option_d,
               correct_answer, explanation, category, keywords
        FROM questions
        WHERE id = ?
    """, (question_id,))

    data = cursor.fetchone()
    conn.close()
    return data


def check_text_answer(user_answer, keywords):
    if not keywords:
        return False

    keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    user_answer = user_answer.lower()

    matches = 0

    for keyword in keyword_list:
        if keyword in user_answer:
            matches += 1

    return matches >= 2


@app.route("/")
def index():
    questions = get_all_questions()
    return render_template("index.html", questions=questions)


@app.route("/quiz")
def quiz():
    questions = get_all_questions()

    if not questions:
        return "Keine Fragen vorhanden."

    question = random.choice(questions)
    return render_template("quiz.html", question=question)


@app.route("/check", methods=["POST"])
def check():
    question_id = request.form.get("question_id")
    user_answer = request.form.get("answer", "")

    question = get_question_by_id(question_id)

    if not question:
        return "Frage nicht gefunden."

    correct_answer = question[7]
    explanation = question[8]
    answer_type = question[2]
    keywords = question[10]

    if answer_type == "multiple_choice":
        is_correct = user_answer.upper() == correct_answer.upper()
    else:
        is_correct = check_text_answer(user_answer, keywords)

    return render_template(
        "result.html",
        question=question,
        user_answer=user_answer,
        is_correct=is_correct,
        correct_answer=correct_answer,
        explanation=explanation
    )


if __name__ == "__main__":
    app.run(debug=True)