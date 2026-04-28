import sqlite3
import random

def get_questions():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT question, answer_type, option_a, option_b, option_c, option_d,
           correct_answer, explanation
    FROM questions
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def start_quiz():
    questions = get_questions()

    if not questions:
        print("Keine Fragen vorhanden.")
        return

    random.shuffle(questions)

    for q in questions:
        question, atype, a, b, c, d, correct, explanation = q

        print("\n---------------------------")
        print("Frage:", question)

        if atype == "multiple_choice":
            print("A:", a)
            print("B:", b)
            print("C:", c)
            print("D:", d)

            user = input("Deine Antwort (A/B/C/D): ").upper()

            if user == correct:
                print("Richtig")
            else:
                print("Falsch")

        elif atype == "text":
            user = input("Deine Antwort: ").lower()

            if user in correct.lower():
                print("Richtig")
            else:
                print("Falsch")

        print("Erklärung:", explanation)


if __name__ == "__main__":
    start_quiz()