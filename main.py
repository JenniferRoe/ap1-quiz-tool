import random
import sqlite3
import time
from dataclasses import dataclass
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

QUESTION_TIME_LIMIT = 120
TOTAL_TEST_TIME_LIMIT = 120 * 60
DB_PATH = "questions.db"


@dataclass
class Question:
    question: str
    answer_type: str
    option_a: Optional[str]
    option_b: Optional[str]
    option_c: Optional[str]
    option_d: Optional[str]
    correct_answer: str
    explanation: str
    category: str
    keywords: Optional[str]


def get_questions() -> List[Question]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT question, answer_type, option_a, option_b, option_c, option_d,
                       correct_answer, explanation, category, keywords
                FROM questions
                """
            )
            rows = cursor.fetchall()

        return [Question(*row) for row in rows]

    except Exception as e:
        console.print(f"[red]Fehler beim Laden der Datenbank: {e}[/red]")
        return []


def get_categories(questions: List[Question]) -> List[str]:
    return sorted({q.category for q in questions})


def choose_category(questions: List[Question]) -> List[Question]:
    categories = get_categories(questions)

    console.print(Panel("[bold cyan]AP1 Quiz Tool[/bold cyan]", subtitle="Kategorie auswählen"))

    table = Table(title="Verfügbare Kategorien")
    table.add_column("Nr.", justify="right")
    table.add_column("Kategorie")

    table.add_row("0", "Alle Kategorien")

    for index, category in enumerate(categories, start=1):
        table.add_row(str(index), category)

    console.print(table)

    choice = Prompt.ask("Welche Kategorie möchtest du lernen?", default="0")

    if choice == "0":
        return questions

    try:
        selected_category = categories[int(choice) - 1]
        return [q for q in questions if q.category == selected_category]

    except (ValueError, IndexError):
        console.print("[red]Ungültige Auswahl. Es werden alle Fragen geladen.[/red]")
        return questions


def check_text_answer(user_answer: str, keywords: Optional[str]) -> bool:
    if not keywords:
        return False

    keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    answer = user_answer.lower()

    matches = sum(1 for keyword in keyword_list if keyword in answer)
    required_matches = max(1, min(2, len(keyword_list)))

    return matches >= required_matches


def ask_multiple_choice(question: Question) -> bool:
    answer_table = Table(title="Antwortmöglichkeiten")
    answer_table.add_column("Auswahl")
    answer_table.add_column("Antwort")

    answer_table.add_row("A", str(question.option_a or ""))
    answer_table.add_row("B", str(question.option_b or ""))
    answer_table.add_row("C", str(question.option_c or ""))
    answer_table.add_row("D", str(question.option_d or ""))

    console.print(answer_table)

    while True:
        user_answer = Prompt.ask("Deine Antwort").upper()

        if user_answer in ["A", "B", "C", "D"]:
            break

        console.print("[red]Bitte A, B, C oder D eingeben.[/red]")

    return user_answer == question.correct_answer.upper()


def ask_text_question(question: Question) -> bool:
    user_answer = Prompt.ask("Deine Antwort")
    return check_text_answer(user_answer, question.keywords)


def show_result(is_correct: bool, question: Question) -> None:
    if is_correct:
        console.print("[green]Richtig[/green]")
    else:
        console.print("[red]Falsch[/red]")
        console.print(f"[yellow]Richtige Lösung:[/yellow] {question.correct_answer}")

    console.print(Panel(question.explanation, title="Erklärung"))


def run_questions(questions: List[Question], repeat_mode: bool = False) -> tuple[int, List[Question]]:
    correct_answers = 0
    wrong_questions = []
    test_start = time.time()
    total_questions = len(questions)

    for number, question in enumerate(questions, start=1):
        if not repeat_mode and time.time() - test_start >= TOTAL_TEST_TIME_LIMIT:
            console.print("[red]Die Gesamtzeit von 120 Minuten ist abgelaufen.[/red]")
            break

        title = f"Wiederholung {number} von {total_questions}" if repeat_mode else f"Frage {number} von {total_questions}"

        console.print()
        console.print(
            Panel(
                f"[bold]{question.question}[/bold]",
                title=title,
                subtitle=f"Kategorie: {question.category} | Zeitlimit: 2 Minuten",
            )
        )

        question_start = time.time()

        if question.answer_type == "multiple_choice":
            is_correct = ask_multiple_choice(question)
        elif question.answer_type == "text":
            is_correct = ask_text_question(question)
        else:
            console.print("[red]Unbekannter Fragetyp.[/red]")
            is_correct = False

        if time.time() - question_start > QUESTION_TIME_LIMIT:
            console.print("[red]Zeit abgelaufen.[/red]")
            is_correct = False

        if is_correct:
            correct_answers += 1
        else:
            wrong_questions.append(question)

        show_result(is_correct, question)

    return correct_answers, wrong_questions


def show_final_result(correct_answers: int, total_questions: int) -> None:
    percentage = (correct_answers / total_questions) * 100 if total_questions else 0

    console.print()
    console.print(
        Panel(
            f"Richtig: {correct_answers} von {total_questions}\n"
            f"Ergebnis: {percentage:.0f} %",
            title="Quiz beendet",
        )
    )

    if percentage < 60:
        console.print("[red]Du musst noch viel lernen[/red]")
    elif percentage < 85:
        console.print("[yellow]Du bist auf einem guten Weg[/yellow]")
    else:
        console.print("[green]Super Nerd[/green]")


def start_quiz() -> None:
    questions = get_questions()

    if not questions:
        console.print("[red]Keine Fragen vorhanden.[/red]")
        return

    questions = choose_category(questions)
    random.shuffle(questions)

    correct_answers, wrong_questions = run_questions(questions)
    show_final_result(correct_answers, len(questions))

    if wrong_questions:
        console.print()
        repeat = Prompt.ask("Falsche Fragen wiederholen?", choices=["j", "n"], default="j")

        if repeat == "j":
            random.shuffle(wrong_questions)
            console.print(Panel("[bold blue]Wiederholungsmodus startet[/bold blue]"))

            repeat_correct, repeat_wrong = run_questions(wrong_questions, repeat_mode=True)
            show_final_result(repeat_correct, len(wrong_questions))


if __name__ == "__main__":
    start_quiz()