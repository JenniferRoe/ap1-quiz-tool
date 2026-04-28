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

    # Lernstand Tabelle
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        category TEXT,
        is_correct INTEGER,
        answered_at TEXT,
        FOREIGN KEY (question_id) REFERENCES questions(id)
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

    insert_question(
    "Was ist das Ziel eines Service Level Agreements?",
    "multiple_choice",
    "Marketing verbessern",
    "Leistungen zwischen Kunde und Anbieter festlegen",
    "Software verkaufen",
    "Personal einstellen",
    "B",
    "Ein SLA definiert Leistungen wie Verfügbarkeit, Reaktionszeit und Support.",
    "Kundenkontakt",
    "leistung,vereinbarung,kunde,anbieter,sla"
)

insert_question(
    "Was versteht man unter Liquidität?",
    "multiple_choice",
    "Gewinn",
    "Zahlungsfähigkeit",
    "Schulden",
    "Produktion",
    "B",
    "Liquidität beschreibt die Fähigkeit eines Unternehmens, seine Rechnungen zu bezahlen.",
    "BWL",
    "zahlung,geld,liquide,zahlungsfähigkeit"
)

insert_question(
    "Was ist RAM?",
    "multiple_choice",
    "Festplatte",
    "Arbeitsspeicher",
    "Netzwerkgerät",
    "CPU",
    "B",
    "RAM ist der Arbeitsspeicher, in dem Daten temporär gespeichert werden.",
    "IT Grundlagen",
    "speicher,arbeitsspeicher,ram,temporär"
)

insert_question(
    "Was ist eine IP-Adresse?",
    "multiple_choice",
    "Name eines Computers",
    "Eindeutige Adresse im Netzwerk",
    "Software",
    "Passwort",
    "B",
    "Eine IP-Adresse identifiziert ein Gerät eindeutig im Netzwerk.",
    "Netzwerke",
    "adresse,netzwerk,ip,gerät"
)

insert_question(
    "Was bedeutet Datenschutz?",
    "text",
    None, None, None, None,
    "Schutz personenbezogener Daten",
    "Datenschutz bedeutet, persönliche Daten vor Missbrauch zu schützen.",
    "Datenschutz & Sicherheit",
    "daten,schutz,personenbezogen,privat"
)

insert_question(
    "Was ist ein Router?",
    "multiple_choice",
    "Speichergerät",
    "Netzwerkgerät zur Weiterleitung von Daten",
    "Software",
    "Monitor",
    "B",
    "Ein Router verbindet Netzwerke und leitet Datenpakete weiter.",
    "Netzwerke",
    "netzwerk,router,weiterleitung,daten"
)

insert_question(
    "Was ist ein Backup?",
    "multiple_choice",
    "Löschen von Daten",
    "Sicherung von Daten",
    "Virus",
    "Programm",
    "B",
    "Ein Backup dient zur Wiederherstellung von Daten im Fehlerfall.",
    "IT Grundlagen",
    "backup,sicherung,daten,wiederherstellung"
)

insert_question(
    "Was ist ein Virus in der IT?",
    "multiple_choice",
    "Hardwarefehler",
    "Schadsoftware",
    "Netzwerkgerät",
    "Benutzer",
    "B",
    "Ein Virus ist eine Schadsoftware, die Systeme infizieren kann.",
    "Datenschutz & Sicherheit",
    "virus,malware,schadsoftware,angriff"
)

insert_question(
    "Was ist ein LAN?",
    "multiple_choice",
    "Weitverkehrsnetz",
    "Lokales Netzwerk",
    "Cloud",
    "Server",
    "B",
    "LAN steht für Local Area Network und beschreibt ein lokales Netzwerk.",
    "Netzwerke",
    "lan,netzwerk,lokal"
)

insert_question(
    "Was bedeutet Angebot und Nachfrage?",
    "text",
    None, None, None, None,
    "Preisbildung durch Angebot und Nachfrage",
    "Angebot und Nachfrage bestimmen den Preis auf dem Markt.",
    "BWL",
    "angebot,nachfrage,preis,markt"
)

insert_question(
    "Was ist eine Firewall?",
    "multiple_choice",
    "Speicher",
    "Schutzsystem für Netzwerke",
    "Monitor",
    "Software zum Drucken",
    "B",
    "Eine Firewall schützt Netzwerke vor unbefugtem Zugriff.",
    "Datenschutz & Sicherheit",
    "firewall,schutz,netzwerk,sicherheit"
)

insert_question(
    "Was ist ein Server?",
    "multiple_choice",
    "Client",
    "Dienstanbieter im Netzwerk",
    "Kabel",
    "Switch",
    "B",
    "Ein Server stellt Dienste oder Daten für andere Geräte bereit.",
    "IT Grundlagen",
    "server,dienst,netzwerk,bereitstellung"
)

insert_question(
    "Was ist ein Client?",
    "multiple_choice",
    "Server",
    "Gerät das Dienste nutzt",
    "Switch",
    "Router",
    "B",
    "Ein Client nutzt Dienste eines Servers.",
    "IT Grundlagen",
    "client,nutzer,gerät,dienst"
)

insert_question(
    "Was ist DHCP?",
    "multiple_choice",
    "Manuelle IP-Vergabe",
    "Automatische IP-Vergabe",
    "Firewall",
    "Backup",
    "B",
    "DHCP vergibt automatisch IP-Adressen im Netzwerk.",
    "Netzwerke",
    "dhcp,ip,automatisch,netzwerk"
)

insert_question(
    "Was ist DNS?",
    "multiple_choice",
    "IP-Adresse",
    "Namensauflösungssystem",
    "Router",
    "Software",
    "B",
    "DNS übersetzt Domainnamen in IP-Adressen.",
    "Netzwerke",
    "dns,name,ip,auflösung"
)

insert_question(
    "Was ist ein Switch?",
    "multiple_choice",
    "Router",
    "Verteiler im Netzwerk",
    "CPU",
    "RAM",
    "B",
    "Ein Switch verbindet Geräte innerhalb eines Netzwerks.",
    "Netzwerke",
    "switch,netzwerk,verteilen,geräte"
)

insert_question(
    "Was bedeutet Verschlüsselung?",
    "text",
    None, None, None, None,
    "Daten unlesbar machen",
    "Verschlüsselung schützt Daten vor unbefugtem Zugriff.",
    "Datenschutz & Sicherheit",
    "verschlüsselung,daten,sicherheit,schutz"
)

insert_question(
    "Was ist eine SSD?",
    "multiple_choice",
    "Langsamer Speicher",
    "Schneller Massenspeicher",
    "Netzwerkgerät",
    "Software",
    "B",
    "SSD ist ein schneller Speicher ohne bewegliche Teile.",
    "IT Grundlagen",
    "ssd,speicher,schnell,daten"
)

insert_question(
    "Was ist eine HDD?",
    "multiple_choice",
    "Arbeitsspeicher",
    "Festplatte mit mechanischen Teilen",
    "Router",
    "CPU",
    "B",
    "HDD ist eine klassische Festplatte mit rotierenden Scheiben.",
    "IT Grundlagen",
    "hdd,festplatte,speicher"
)

insert_question(
    "Was bedeutet Gewinn?",
    "multiple_choice",
    "Einnahmen minus Kosten",
    "Kosten",
    "Umsatz",
    "Steuern",
    "A",
    "Gewinn entsteht, wenn Einnahmen größer als Kosten sind.",
    "BWL",
    "gewinn,einnahmen,ausgaben"
)

insert_question(
    "Was ist Umsatz?",
    "multiple_choice",
    "Gewinn",
    "Gesamte Einnahmen",
    "Kosten",
    "Steuern",
    "B",
    "Umsatz ist die Summe aller Einnahmen.",
    "BWL",
    "umsatz,einnahmen,verkauf"
)

insert_question(
    "Was ist ein Betriebssystem?",
    "multiple_choice",
    "Software zur Steuerung des Computers",
    "Hardware",
    "Netzwerkgerät",
    "Speicher",
    "A",
    "Das Betriebssystem verwaltet Hardware und Software.",
    "IT Grundlagen",
    "betriebssystem,steuerung,software"
)

insert_question(
    "Was ist Malware?",
    "multiple_choice",
    "Schadsoftware",
    "Hardware",
    "Netzwerk",
    "Backup",
    "A",
    "Malware ist schädliche Software.",
    "Datenschutz & Sicherheit",
    "malware,virus,schadsoftware"
)

insert_question(
    "Was ist Phishing?",
    "multiple_choice",
    "Angriff über E-Mails",
    "Backup",
    "Hardware",
    "Router",
    "A",
    "Phishing versucht Zugangsdaten zu stehlen.",
    "Datenschutz & Sicherheit",
    "phishing,email,betrug,daten"
)

insert_question(
    "Was ist ein Passwort?",
    "text",
    None, None, None, None,
    "Geheime Zugangsdaten",
    "Ein Passwort schützt den Zugriff auf Systeme.",
    "Datenschutz & Sicherheit",
    "passwort,zugang,sicherheit"
)

insert_question(
    "Was ist ein VPN?",
    "multiple_choice",
    "Sicherer Tunnel im Netzwerk",
    "Router",
    "CPU",
    "Speicher",
    "A",
    "VPN ermöglicht sichere Verbindungen über das Internet.",
    "Netzwerke",
    "vpn,sicher,netzwerk,tunnel"
)

insert_question(
    "Was bedeutet Redundanz?",
    "text",
    None, None, None, None,
    "Doppelte Systeme zur Sicherheit",
    "Redundanz erhöht die Ausfallsicherheit.",
    "IT Grundlagen",
    "redundanz,sicherheit,backup"
)

insert_question(
    "Was ist ein Backup?",
    "text",
    None, None, None, None,
    "Datensicherung",
    "Backup dient zur Wiederherstellung von Daten.",
    "IT Grundlagen",
    "backup,daten,sicherung"
)

insert_question(
    "Was ist Cloud Computing?",
    "multiple_choice",
    "Speicherung und Nutzung über Internet",
    "Lokaler Speicher",
    "Router",
    "CPU",
    "A",
    "Cloud Computing nutzt externe Server.",
    "IT Grundlagen",
    "cloud,internet,server"
)

insert_question(
    "Was ist ein Protokoll im Netzwerk?",
    "multiple_choice",
    "Regelwerk für Kommunikation",
    "Hardware",
    "Software",
    "Kabel",
    "A",
    "Protokolle definieren Datenübertragung.",
    "Netzwerke",
    "protokoll,regeln,kommunikation"
)

insert_question(
    "Was bedeutet Virtualisierung?",
    "text",
    None, None, None, None,
    "Mehrere virtuelle Systeme auf einer Hardware",
    "Virtualisierung ermöglicht mehrere Betriebssysteme auf einem physischen Rechner.",
    "IT Grundlagen",
    "virtualisierung,virtuell,mehrere,systeme"
)

insert_question(
    "Was ist eine virtuelle Maschine?",
    "multiple_choice",
    "Physischer Server",
    "Softwarebasierter Computer",
    "Router",
    "Switch",
    "B",
    "Eine VM ist ein emulierter Computer innerhalb eines Systems.",
    "IT Grundlagen",
    "vm,virtualisierung,software,rechner"
)

insert_question(
    "Was ist ein Hypervisor?",
    "multiple_choice",
    "Datenbank",
    "Verwaltung von virtuellen Maschinen",
    "Firewall",
    "Backup",
    "B",
    "Ein Hypervisor verwaltet virtuelle Maschinen.",
    "IT Grundlagen",
    "hypervisor,vm,verwaltung"
)

insert_question(
    "Was ist eine Datenbank?",
    "text",
    None, None, None, None,
    "Strukturierte Sammlung von Daten",
    "Eine Datenbank speichert und verwaltet Daten.",
    "Datenbanken",
    "datenbank,daten,struktur"
)

insert_question(
    "Was ist SQL?",
    "multiple_choice",
    "Programmiersprache für Spiele",
    "Abfragesprache für Datenbanken",
    "Netzwerkprotokoll",
    "Hardware",
    "B",
    "SQL wird verwendet um Datenbanken zu steuern.",
    "Datenbanken",
    "sql,datenbank,abfrage"
)

insert_question(
    "Was ist ein Primärschlüssel?",
    "multiple_choice",
    "Mehrere gleiche Werte",
    "Eindeutiger Identifikator",
    "Passwort",
    "Backup",
    "B",
    "Ein Primärschlüssel identifiziert jeden Datensatz eindeutig.",
    "Datenbanken",
    "primary key,schlüssel,eindeutig"
)

insert_question(
    "Was ist ein Fremdschlüssel?",
    "multiple_choice",
    "Verbindung zwischen Tabellen",
    "Passwort",
    "Backup",
    "CPU",
    "A",
    "Ein Fremdschlüssel verbindet Tabellen miteinander.",
    "Datenbanken",
    "fremdschlüssel,relation,tabellen"
)

insert_question(
    "Was ist ein Trigger in einer Datenbank?",
    "text",
    None, None, None, None,
    "Automatische Aktion bei Ereignis",
    "Ein Trigger führt automatisch Aktionen bei Änderungen aus.",
    "Datenbanken",
    "trigger,automatisch,aktion"
)

insert_question(
    "Was ist eine Transaktion?",
    "multiple_choice",
    "Einzelne Abfrage",
    "Zusammenhängende Datenbankoperation",
    "Backup",
    "Server",
    "B",
    "Eine Transaktion wird vollständig oder gar nicht ausgeführt.",
    "Datenbanken",
    "transaktion,datenbank,operation"
)

insert_question(
    "Was bedeutet ACID?",
    "multiple_choice",
    "Netzwerkprotokoll",
    "Eigenschaften von Transaktionen",
    "Hardware",
    "Firewall",
    "B",
    "ACID beschreibt Zuverlässigkeit von Datenbanktransaktionen.",
    "Datenbanken",
    "acid,transaktion,sicherheit"
)

insert_question(
    "Was ist ein digitales Zertifikat?",
    "multiple_choice",
    "Hardware",
    "Nachweis der Identität im Internet",
    "Router",
    "Backup",
    "B",
    "Zertifikate bestätigen Identitäten und ermöglichen Verschlüsselung.",
    "Datenschutz & Sicherheit",
    "zertifikat,identität,ssl,verschlüsselung"
)

insert_question(
    "Was ist SSL/TLS?",
    "multiple_choice",
    "Speicher",
    "Verschlüsselungsprotokoll",
    "Router",
    "CPU",
    "B",
    "SSL/TLS verschlüsselt Datenübertragungen im Internet.",
    "Datenschutz & Sicherheit",
    "ssl,tls,verschlüsselung"
)

insert_question(
    "Was bedeutet Authentifizierung?",
    "text",
    None, None, None, None,
    "Identität prüfen",
    "Authentifizierung überprüft die Identität eines Nutzers.",
    "Datenschutz & Sicherheit",
    "authentifizierung,identität,login"
)

insert_question(
    "Was bedeutet Autorisierung?",
    "text",
    None, None, None, None,
    "Zugriffsrechte vergeben",
    "Autorisierung bestimmt was ein Nutzer darf.",
    "Datenschutz & Sicherheit",
    "autorisierung,rechte,zugriff"
)

insert_question(
    "Was ist ein Protokoll im IT Kontext?",
    "multiple_choice",
    "Hardware",
    "Regelwerk für Kommunikation",
    "Speicher",
    "CPU",
    "B",
    "Protokolle regeln den Datenaustausch.",
    "Netzwerke",
    "protokoll,kommunikation,regeln"
)

insert_question(
    "Was bedeutet Skalierbarkeit?",
    "text",
    None, None, None, None,
    "System anpassbar erweitern",
    "Skalierbarkeit beschreibt die Anpassungsfähigkeit eines Systems.",
    "IT Grundlagen",
    "skalierbarkeit,leistung,erweiterung"
)

insert_question(
    "Was ist ein RAID-System?",
    "multiple_choice",
    "Netzwerk",
    "Speicherverbund",
    "CPU",
    "Software",
    "B",
    "RAID kombiniert mehrere Festplatten zur Sicherheit oder Geschwindigkeit.",
    "IT Grundlagen",
    "raid,speicher,festplatte"
)

insert_question(
    "Was bedeutet Backupstrategie?",
    "text",
    None, None, None, None,
    "Plan zur Datensicherung",
    "Eine Backupstrategie legt fest wie Daten gesichert werden.",
    "IT Grundlagen",
    "backup,strategie,sicherung"
)

insert_question(
    "Was ist ein Benutzerkonto?",
    "multiple_choice",
    "Hardware",
    "Zugang zu Systemen",
    "Router",
    "Switch",
    "B",
    "Ein Benutzerkonto ermöglicht Zugriff auf Systeme.",
    "Kundenkontakt",
    "benutzer,login,zugang"
)

insert_question(
    "Was bedeutet SLA im Support?",
    "text",
    None, None, None, None,
    "Vereinbarte Reaktionszeiten",
    "SLA definiert wie schnell Support reagiert.",
    "Kundenkontakt",
    "sla,reaktion,zeit,support"
)

insert_question(
    "Was ist ein VPN?",
    "multiple_choice",
    "Ein Speichergerät",
    "Ein sicherer Tunnel über das Internet",
    "Ein Router",
    "Ein Betriebssystem",
    "B",
    "Ein VPN stellt eine verschlüsselte Verbindung über ein unsicheres Netzwerk her.",
    "Netzwerke",
    "vpn,verschlüsselung,tunnel,sicher"
)

insert_question(
    "Warum wird ein VPN verwendet?",
    "text",
    None, None, None, None,
    "Sichere Verbindung über Internet",
    "Ein VPN schützt Daten bei der Übertragung über öffentliche Netzwerke.",
    "Netzwerke",
    "sicher,verschlüsselung,internet,schutz"
)

insert_question(
    "Was macht die CPU?",
    "multiple_choice",
    "Speichert Daten",
    "Verarbeitet Befehle",
    "Zeigt Bilder",
    "Verbindet Netzwerke",
    "B",
    "Die CPU ist die zentrale Recheneinheit und verarbeitet Befehle.",
    "IT Grundlagen",
    "cpu,prozessor,rechnen"
)

insert_question(
    "Was ist ein Mainboard?",
    "multiple_choice",
    "Grafikkarte",
    "Zentrale Platine im Computer",
    "Festplatte",
    "Router",
    "B",
    "Das Mainboard verbindet alle Komponenten eines Computers.",
    "IT Grundlagen",
    "mainboard,hardware,platine"
)

insert_question(
    "Was ist eine Grafikkarte?",
    "multiple_choice",
    "Netzwerkgerät",
    "Berechnet Bilddarstellung",
    "Speicher",
    "CPU",
    "B",
    "Die Grafikkarte berechnet Bilder und Videos.",
    "IT Grundlagen",
    "gpu,grafik,bild"
)

insert_question(
    "Was ist Qualitätsmanagement?",
    "text",
    None, None, None, None,
    "Sicherung und Verbesserung von Qualität",
    "Qualitätsmanagement stellt sicher, dass Produkte und Prozesse bestimmte Standards erfüllen.",
    "BWL",
    "qualität,prozess,verbesserung"
)

insert_question(
    "Was bedeutet ISO 9001?",
    "multiple_choice",
    "IT Standard",
    "Qualitätsmanagement Norm",
    "Netzwerkprotokoll",
    "Software",
    "B",
    "ISO 9001 ist eine Norm für Qualitätsmanagementsysteme.",
    "BWL",
    "iso,qualität,norm"
)

insert_question(
    "Ein Kredit von 1000 Euro hat 5% Zinsen. Wie hoch sind die Zinsen nach einem Jahr?",
    "text",
    None, None, None, None,
    "50",
    "5 Prozent von 1000 Euro sind 50 Euro.",
    "BWL",
    "50,fünfzig,zinsen"
)

insert_question(
    "Ein Kredit beträgt 2000 Euro mit 10% Zinsen. Wie hoch sind die Zinsen?",
    "text",
    None, None, None, None,
    "200",
    "10 Prozent von 2000 Euro sind 200 Euro.",
    "BWL",
    "200,zinsen"
)

insert_question(
    "Du nimmst einen Kredit über 5000 Euro mit 4% Zinsen. Wie viel Zinsen zahlst du im Jahr?",
    "text",
    None, None, None, None,
    "200",
    "4 Prozent von 5000 Euro sind 200 Euro.",
    "BWL",
    "200,zinsen"
)

insert_question(
    "Ein Kredit über 3000 Euro hat 3% Zinsen. Wie hoch ist der Zinsbetrag?",
    "text",
    None, None, None, None,
    "90",
    "3 Prozent von 3000 Euro sind 90 Euro.",
    "BWL",
    "90,zinsen"
)

insert_question(
    "Was bedeutet Effektivität?",
    "multiple_choice",
    "Dinge richtig tun",
    "Die richtigen Dinge tun",
    "Kosten sparen",
    "Gewinn steigern",
    "B",
    "Effektivität bedeutet, die richtigen Dinge zu tun, also das richtige Ziel zu erreichen.",
    "BWL",
    "effektivität,ziel,richtig"
)

insert_question(
    "Was bedeutet Effizienz?",
    "multiple_choice",
    "Die richtigen Dinge tun",
    "Dinge richtig tun",
    "Mehr Gewinn machen",
    "Kosten ignorieren",
    "B",
    "Effizienz bedeutet, Dinge richtig zu tun, also mit möglichst wenig Aufwand ein Ziel erreichen.",
    "BWL",
    "effizienz,aufwand,ressourcen"
)

insert_question(
    "Was ist der Unterschied zwischen Effektivität und Effizienz?",
    "text",
    None, None, None, None,
    "Effektivität richtige Ziele Effizienz richtiger Weg",
    "Effektivität = richtige Ziele erreichen. Effizienz = Ziele mit minimalem Aufwand erreichen.",
    "BWL",
    "effektivität,effizienz,ziel,aufwand"
)

insert_question(
    "Was ist Qualitätsmanagement?",
    "multiple_choice",
    "Kosten senken",
    "Qualität sichern und verbessern",
    "Personal einstellen",
    "Marketing",
    "B",
    "Qualitätsmanagement sorgt für gleichbleibende und verbesserte Qualität.",
    "BWL",
    "qualität,management,verbesserung"
)

insert_question(
    "Was ist das Ziel von Qualitätsmanagement?",
    "text",
    None, None, None, None,
    "Qualität sichern und verbessern",
    "Ziel ist es, Produkte und Prozesse zu optimieren.",
    "BWL",
    "qualität,verbesserung,prozesse"
)

insert_question(
    "Was bedeutet KVP?",
    "multiple_choice",
    "Kontrollierter Verkaufsprozess",
    "Kontinuierlicher Verbesserungsprozess",
    "Kunden Verkaufs Plan",
    "Kosten Vermeidungs Prozess",
    "B",
    "KVP steht für kontinuierliche Verbesserung von Prozessen.",
    "BWL",
    "kvp,verbesserung,prozess"
)

insert_question(
    "Was ist der kontinuierliche Verbesserungsprozess?",
    "text",
    None, None, None, None,
    "Ständige Verbesserung von Prozessen",
    "KVP bedeutet, Prozesse dauerhaft zu optimieren.",
    "BWL",
    "kvp,verbesserung,prozess"
)

insert_question(
    "Was ist eine Norm im Qualitätsmanagement?",
    "multiple_choice",
    "Gesetz",
    "Vorgabe oder Standard",
    "Software",
    "Gerät",
    "B",
    "Normen legen Standards für Qualität fest.",
    "BWL",
    "norm,standard,qualität"
)

insert_question(
    "Was bedeutet ISO 9001?",
    "text",
    None, None, None, None,
    "Norm für Qualitätsmanagement",
    "ISO 9001 ist eine internationale Norm für Qualitätsmanagementsysteme.",
    "BWL",
    "iso,9001,qualität"
)

insert_question(
    "Was ist ein Prozess?",
    "multiple_choice",
    "Ein Gerät",
    "Abfolge von Arbeitsschritten",
    "Software",
    "Netzwerk",
    "B",
    "Ein Prozess besteht aus mehreren Schritten zur Zielerreichung.",
    "BWL",
    "prozess,ablauf,schritte"
)

insert_question(
    "Was bedeutet Kundenorientierung?",
    "text",
    None, None, None, None,
    "Bedürfnisse des Kunden im Mittelpunkt",
    "Unternehmen richten sich nach Kundenanforderungen.",
    "Kundenkontakt",
    "kunde,bedarf,service"
)

insert_question(
    "Was ist ein Qualitätsziel?",
    "multiple_choice",
    "Gewinn",
    "Festgelegtes Qualitätsniveau",
    "Marketing",
    "Kosten",
    "B",
    "Qualitätsziele definieren gewünschte Qualitätsstandards.",
    "BWL",
    "qualität,ziel,standard"
)

insert_question(
    "Was bedeutet Fehlervermeidung im QM?",
    "text",
    None, None, None, None,
    "Fehler von Anfang an verhindern",
    "Ziel ist es, Fehler gar nicht erst entstehen zu lassen.",
    "BWL",
    "fehler,vermeidung,qualität"
)

insert_question(
    "Was ist Dokumentation im Qualitätsmanagement?",
    "multiple_choice",
    "Unnötig",
    "Wichtige Aufzeichnung von Prozessen",
    "Backup",
    "Server",
    "B",
    "Dokumentation sorgt für Nachvollziehbarkeit.",
    "BWL",
    "dokumentation,prozess,qualität"
)

insert_question(
    "Warum ist Qualität wichtig für Unternehmen?",
    "text",
    None, None, None, None,
    "Kundenzufriedenheit sichern",
    "Qualität sorgt für zufriedene Kunden und langfristigen Erfolg.",
    "BWL",
    "qualität,kunde,erfolg"
)

insert_question(
    "Ein Kredit über 1000 Euro hat 5 Prozent Zinsen. Wie viel Zinsen fallen an?",
    "text",
    None, None, None, None,
    "50",
    "5 Prozent von 1000 sind 50.",
    "BWL",
    "50,zinsen"
)

insert_question(
    "Ein Produkt kostet 200 Euro. Es wird um 10 Prozent erhöht. Neuer Preis?",
    "text",
    None, None, None, None,
    "220",
    "10 Prozent von 200 sind 20, also 220.",
    "BWL",
    "220,preis"
)

insert_question(
    "Ein Rabatt von 20 Prozent auf 150 Euro. Wie viel zahlst du?",
    "text",
    None, None, None, None,
    "120",
    "20 Prozent von 150 sind 30, also 120.",
    "BWL",
    "120,rabatt"
)

insert_question(
    "Ein Kredit beträgt 5000 Euro mit 4 Prozent Zinsen. Zinsbetrag?",
    "text",
    None, None, None, None,
    "200",
    "4 Prozent von 5000 sind 200.",
    "BWL",
    "200,zinsen"
)
