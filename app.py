from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_questions():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT question, category FROM questions
    """)

    data = cursor.fetchall()
    conn.close()
    return data


@app.route("/")
def index():
    questions = get_questions()
    return render_template("index.html", questions=questions)


if __name__ == "__main__":
    app.run(debug=True)