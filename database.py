import sqlite3

def create_database():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer_type TEXT,
        option_a TEXT,
        option_b TEXT,
        option_c TEXT,
        option_d TEXT,
        correct_answer TEXT,
        explanation TEXT,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_question(q, atype, a, b, c, d, correct, explanation, category):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO questions (
        question, answer_type, option_a, option_b, option_c, option_d,
        correct_answer, explanation, category
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (q, atype, a, b, c, d, correct, explanation, category))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()

    insert_question(
        "Was bedeutet SLA?",
        "multiple_choice",
        "Software License Agreement",
        "Service Level Agreement",
        "System Login Access",
        "Secure Local Area",
        "B",
        "Ein Service Level Agreement ist eine Vereinbarung zwischen Anbieter und Kunde über Leistungen wie Verfügbarkeit oder Support.",
        "Kundenkontakt"
    )

    insert_question(
        "Was ist Eskalation im IT-Support?",
        "text",
        None,
        None,
        None,
        None,
        "Weiterleitung eines Problems an höhere Support-Stufe",
        "Wenn ein Problem nicht gelöst werden kann, wird es an eine höhere Support-Ebene weitergegeben.",
        "Kundenkontakt"
    )