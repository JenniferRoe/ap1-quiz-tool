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
        category TEXT,
        keywords TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_question(question, answer_type, a, b, c, d, correct, explanation, category, keywords):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO questions (
        question, answer_type, option_a, option_b, option_c, option_d,
        correct_answer, explanation, category, keywords
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (question, answer_type, a, b, c, d, correct, explanation, category, keywords))

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
        "Ein Service Level Agreement ist eine Vereinbarung zwischen Anbieter und Kunde.",
        "Kundenkontakt",
        "service,level,agreement,kunde,leistung"
    )

    insert_question(
        "Erkläre Eskalation im IT-Support.",
        "text",
        None, None, None, None,
        "Weiterleitung an höhere Support-Stufe",
        "Ein Problem wird an eine höhere Support-Ebene weitergegeben.",
        "Kundenkontakt",
        "weiterleitung,support,problem,höher"
    )