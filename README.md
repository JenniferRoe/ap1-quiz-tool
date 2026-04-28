AP1 Quiz Tool

Das Projekt ist während meiner Umschulung zur Fachinformatikerin für Systemintegration entstanden. Ziel war es, ein eigenes Lernsystem für die AP1 Prüfung zu entwickeln, das nicht nur Fragen stellt, sondern auch wirklich beim Verstehen hilft.

Das Programm basiert auf Python und arbeitet mit einer SQLite Datenbank. Fragen werden dort gespeichert und beim Start des Quiz geladen. Es gibt sowohl Multiple Choice Aufgaben als auch offene Fragen. Bei den offenen Fragen wird nicht einfach nur ein exakter Text verglichen, sondern über Schlüsselbegriffe geprüft, ob die Antwort inhaltlich passt.

Beim Start kann eine Kategorie ausgewählt werden, zum Beispiel Kundenkontakt oder BWL. Dadurch lassen sich gezielt Themen üben. Jede Frage hat ein Zeitlimit von zwei Minuten und zusätzlich gibt es ein Gesamtzeitlimit für den kompletten Test.

Nach jeder Antwort wird direkt angezeigt, ob sie richtig oder falsch ist. Zusätzlich wird eine Erklärung ausgegeben, damit man nicht nur auswendig lernt, sondern auch versteht, warum eine Antwort korrekt ist.

Am Ende gibt es eine Auswertung mit Prozentanzeige und einer kurzen Einschätzung des Ergebnisses.

Technisch habe ich mit Python, SQLite und der Rich Bibliothek gearbeitet, um die Darstellung im Terminal übersichtlicher und moderner zu gestalten.

Das Projekt ist bewusst so aufgebaut, dass es leicht erweitert werden kann. Weitere Fragen, neue Kategorien oder zusätzliche Funktionen lassen sich ohne große Änderungen ergänzen.

Start des Programms erfolgt über:

python database.py
python main.py

Das Projekt zeigt, wie ich Themen aus der Umschulung praktisch umsetze und eigenständig weiterentwickle.
