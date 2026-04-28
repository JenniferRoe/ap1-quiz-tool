import random
import sqlite3
import time
from collections import Counter
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
WRONG_FILE = "wrong_questions.txt"


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


def choose_mode() -> str:
    console.print(Panel("[bold cyan]AP1 Quiz Tool[/bold cyan]", subtitle="Lernmodus auswählen"))

    table = Table(title="Menü")
    table.add_column("Nr.")
    table.add_column("Funktion")

    table.add_row("1", "Normales Lernen")
    table.add_row("2", "Fehlermodus")
    table.add_row("3", "Schwächen anzeigen")
    table.add_row("4", "Fehlerliste löschen")
    table.add_row("q", "Beenden")

    console.print(table)

    return Prompt.ask("Was möchtest du starten?", choices=["1", "2", "3", "4", "q"], default="1")


def choose_category(questions: List[Question]) -> List[Question]:
    categories = get_categories(questions)

    console.print(Panel("[bold cyan]Kategorie auswählen[/bold cyan]"))

    table = Table(title="Verfügbare Kategorien")
    table.add_column("Nr.", justify="right")
    table.add_column("Kategorie")

    table.add_row("0", "Alle Kategorien")

    for index, category in enumerate(categories, start=1):
        table.add_row(str(index), category)

    console.print(table)

    choice = Prompt.ask("Welche Kategorie möchtest du lernen?", default="0")

    if choice.lower() == "q":
        console.print("[yellow]Quiz wurde beendet.[/yellow]")
        return []

    if choice == "0":
        return questions

    try:
        selected_category = categories[int(choice) - 1]
        return [q for q in questions if q.category == selected_category]

    except (ValueError, IndexError):
        console.print("[red]Ungültige Auswahl. Es werden alle Fragen geladen.[/red]")
        return questions


def load_wrong_entries() -> List[tuple[str, str]]:
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
            else:
                entries.append(("Unbekannt", line))

        return entries

    except FileNotFoundError:
        return []


def save_wrong_question(question: Question) -> None:
    with open(WRONG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{question.category}||{question.question}\n")


def clear_wrong_questions() -> None:
    with open(WRONG_FILE, "w", encoding="utf-8") as file:
        file.write("")


def get_wrong_questions(all_questions: List[Question]) -> List[Question]:
    wrong_entries = load_wrong_entries()

    if not wrong_entries:
        return []

    wrong_question_texts = {question_text for _, question_text in wrong_entries}

    return [q for q in all_questions if q.question in wrong_question_texts]


def show_weaknesses() -> None:
    wrong_entries = load_wrong_entries()

    if not wrong_entries:
        console.print("[green]Keine gespeicherten Fehler vorhanden.[/green]")
        return

    category_counter = Counter(category for category, _ in wrong_entries)

    table = Table(title="Deine schwächsten Kategorien")
    table.add_column("Kategorie")
    table.add_column("Fehler", justify="right")

    for category, count in category_counter.most_common():
        table.add_row(category, str(count))

    console.print(table)


def check_text_answer(user_answer: str, keywords: Optional[str]) -> bool:
    if not keywords:
        return False

    keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    answer = user_answer.lower()

    matches = sum(1 for keyword in keyword_list if keyword in answer)
    required_matches = max(1, min(2, len(keyword_list)))

    return matches >= required_matches


def ask_multiple_choice(question: Question) -> Optional[bool]:
    answer_table = Table(title="Antwortmöglichkeiten")
    answer_table.add_column("Auswahl")
    answer_table.add_column("Antwort")

    answer_table.add_row("A", str(question.option_a or ""))
    answer_table.add_row("B", str(question.option_b or ""))
    answer_table.add_row("C", str(question.option_c or ""))
    answer_table.add_row("D", str(question.option_d or ""))

    console.print(answer_table)

    while True:
        user_answer = Prompt.ask("Deine Antwort oder q zum Beenden").upper()

        if user_answer == "Q":
            return None

        if user_answer in ["A", "B", "C", "D"]:
            break

        console.print("[red]Bitte A, B, C, D oder q eingeben.[/red]")

    return user_answer == question.correct_answer.upper()


def ask_text_question(question: Question) -> Optional[bool]:
    user_answer = Prompt.ask("Deine Antwort oder q zum Beenden")

    if user_answer.lower() == "q":
        return None

    return check_text_answer(user_answer, question.keywords)


def show_result(is_correct: bool, question: Question, save_wrong: bool = True) -> None:
    if is_correct:
        console.print("[green]Richtig[/green]")
    else:
        console.print("[red]Falsch[/red]")
        console.print(f"[yellow]Richtige Lösung:[/yellow] {question.correct_answer}")

        if save_wrong:
            save_wrong_question(question)

    console.print(Panel(question.explanation, title="Erklärung"))


def run_questions(
    questions: List[Question],
    repeat_mode: bool = False,
    save_wrong: bool = True
) -> tuple[int, int, bool]:
    correct_answers = 0
    answered_questions = 0
    test_start = time.time()
    total_questions = len(questions)

    for number, question in enumerate(questions, start=1):
        if not repeat_mode and time.time() - test_start >= TOTAL_TEST_TIME_LIMIT:
            console.print("[red]Die Gesamtzeit von 120 Minuten ist abgelaufen.[/red]")
            break

        title = (
            f"Fehlermodus {number} von {total_questions}"
            if repeat_mode
            else f"Frage {number} von {total_questions}"
        )

        console.print()
        console.print(
            Panel(
                f"[bold]{question.question}[/bold]",
                title=title,
                subtitle=f"Kategorie: {question.category} | Zeitlimit: 2 Minuten | q = abbrechen",
            )
        )

        question_start = time.time()

        if question.answer_type == "multiple_choice":
            result = ask_multiple_choice(question)
        elif question.answer_type == "text":
            result = ask_text_question(question)
        else:
            console.print("[red]Unbekannter Fragetyp.[/red]")
            result = False

        if result is None:
            console.print("[yellow]Quiz wurde abgebrochen.[/yellow]")
            return correct_answers, answered_questions, True

        answered_questions += 1
        is_correct = result

        if time.time() - question_start > QUESTION_TIME_LIMIT:
            console.print("[red]Zeit abgelaufen.[/red]")
            is_correct = False

        if is_correct:
            correct_answers += 1

        show_result(is_correct, question, save_wrong=save_wrong)

    return correct_answers, answered_questions, False


def show_final_result(correct_answers: int, answered_questions: int) -> None:
    percentage = (correct_answers / answered_questions) * 100 if answered_questions else 0

    console.print()
    console.print(
        Panel(
            f"Richtig: {correct_answers} von {answered_questions}\n"
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


def start_normal_quiz(all_questions: List[Question]) -> None:
    questions = choose_category(all_questions)

    if not questions:
        return

    random.shuffle(questions)

    correct_answers, answered_questions, aborted = run_questions(
        questions,
        repeat_mode=False,
        save_wrong=True
    )

    if answered_questions > 0:
        show_final_result(correct_answers, answered_questions)


def start_error_mode(all_questions: List[Question]) -> None:
    wrong_questions = get_wrong_questions(all_questions)

    if not wrong_questions:
        console.print("[green]Keine gespeicherten Fehler vorhanden.[/green]")
        return

    console.print(Panel("[bold blue]Fehlermodus startet[/bold blue]"))
    random.shuffle(wrong_questions)

    correct_answers, answered_questions, aborted = run_questions(
        wrong_questions,
        repeat_mode=True,
        save_wrong=False
    )

    if answered_questions > 0:
        show_final_result(correct_answers, answered_questions)

    if answered_questions > 0 and not aborted:
        clear_choice = Prompt.ask(
            "Fehlerliste nach diesem Durchlauf löschen?",
            choices=["j", "n"],
            default="n"
        )

        if clear_choice == "j":
            clear_wrong_questions()
            console.print("[green]Fehlerliste wurde gelöscht.[/green]")


def start_quiz() -> None:
    all_questions = get_questions()

    if not all_questions:
        console.print("[red]Keine Fragen vorhanden.[/red]")
        return

    while True:
        mode = choose_mode()

        if mode == "q":
            console.print("[yellow]Programm beendet.[/yellow]")
            return

        if mode == "1":
            start_normal_quiz(all_questions)

        elif mode == "2":
            start_error_mode(all_questions)

        elif mode == "3":
            show_weaknesses()

        elif mode == "4":
            confirm = Prompt.ask(
                "Fehlerliste wirklich löschen?",
                choices=["j", "n"],
                default="n"
            )

            if confirm == "j":
                clear_wrong_questions()
                console.print("[green]Fehlerliste wurde gelöscht.[/green]")


if __name__ == "__main__":
    start_quiz()