import sqlite3
import random

def get_questions():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("SELECT question, answer FROM questions")
    data = cursor.fetchall()

    conn.close()
    return data

def start_quiz():
    questions = get_questions()

    if not questions:
        print("Keine Fragen in der Datenbank!")
        return

    random.shuffle(questions)

    for q, a in questions:
        print("\nFrage:", q)
        user = input("Deine Antwort: ")

        if user.lower() == a.lower():
            print("Richtig")
        else:
            print("Falsch. Richtige Antwort:", a)

if __name__ == "__main__":
    start_quiz()