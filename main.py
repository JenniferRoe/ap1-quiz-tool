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

    total_questions = len(questions)
    correct_answers = 0

    for q in questions:
        question, atype, a, b, c, d, correct, explanation = q

        print("\n---------------------------")
        print("Frage:", question)

        is_correct = False

        if atype == "multiple_choice":
            print("A:", a)
            print("B:", b)
            print("C:", c)
            print("D:", d)

            user = input("Deine Antwort (A/B/C/D): ").upper()

            if user == correct:
                is_correct = True

        elif atype == "text":
            user = input("Deine Antwort: ").lower()

            if user in correct.lower():
                is_correct = True

        if is_correct:
            print("Richtig")
            correct_answers += 1
        else:
            print("Falsch")
            print("Richtige Antwort:", correct)

        print("Erklärung:", explanation)

    percentage = (correct_answers / total_questions) * 100

    print("\n===========================")
    print("Quiz beendet")
    print(f"Richtig: {correct_answers} von {total_questions}")
    print(f"Ergebnis: {percentage:.0f} %")

    if percentage < 60:
        print("Du musst noch viel lernen")
    elif percentage < 85:
        print("Du bist auf einem guten Weg")
    else:
        print("Super Nerd")


if __name__ == "__main__":
    start_quiz()