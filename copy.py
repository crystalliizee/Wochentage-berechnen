import random
import datetime
import PySimpleGUI as sg
import calendar
import configparser
import requests
import os

# --- Konstanten ---
WOCHENTAGE = ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]
MONATSCODES = [0, 3, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5]
JAHRHUNDERTCODES = {17: 4, 18: 2, 19: 0, 20: 6, 21: 4}
AKTUELLE_VERSION = "1.2.0"  # Aktuelle Version des Programms
UPDATE_URL = "https://raw.githubusercontent.com/dein-github-username/dein-repository-name/main/version.txt"  # URL zur neuesten Versionsnummer

# --- Funktionen ---
# ... (Die Funktionen ist_schaltjahr, monatscode, jahrescode, jahrhundertcode, berechne_wochentag, wochentag_als_string, zufaelliges_datum bleiben unverändert)

# --- GUI Fenster ---
# ... (Die Funktionen tipps_fenster, anleitung_fenster, hauptfenster, schwierigkeitsfenster bleiben unverändert)

# --- Einstellungen speichern und laden ---
def lade_einstellungen():
    """Lädt die Schwierigkeitseinstellungen aus der settings.ini Datei."""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    try:
        schwierigkeit = config['Einstellungen']['Schwierigkeit']
        highscore = int(config['Einstellungen']['Highscore'])  # Highscore laden
    except KeyError:
        schwierigkeit = 'leicht'  # Standardwert, falls keine Einstellung gefunden wird
        highscore = 0  # Standardwert für Highscore
    return schwierigkeit, highscore

def speichere_einstellungen(schwierigkeit, highscore):  # Highscore als Argument hinzufügen
    """Speichert die Schwierigkeitseinstellungen in der settings.ini Datei."""
    config = configparser.ConfigParser()
    config['Einstellungen'] = {'Schwierigkeit': schwierigkeit, 'Highscore': str(highscore)}  # Highscore speichern
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

# --- Update-Funktionen ---
def check_for_updates():
    """Überprüft online, ob eine neue Version verfügbar ist."""
    try:
        response = requests.get(UPDATE_URL)
        response.raise_for_status()  # Fehler auslösen, wenn der Download fehlschlägt
        neueste_version = response.text.strip()
        return neueste_version
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Überprüfen auf Updates: {e}")
        return None

def download_update(neueste_version):
    """Lädt die neueste Version des Skripts herunter."""
    try:
        response = requests.get("https://raw.githubusercontent.com/dein-github-username/dein-repository-name/main/test.py")  # URL zum Skript
        response.raise_for_status()
        with open("test_update.py", "wb") as f:
            f.write(response.content)
        print("Update heruntergeladen.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Herunterladen des Updates: {e}")
        return False

def update_ausfuehren():
    """Ersetzt die alte Version durch die neue."""
    try:
        os.replace("test_update.py", "test.py")
        print("Update ausgeführt.")
        sg.popup("Update erfolgreich!\nDas Programm wird neu gestartet.", title="Update")
        os.execl(sys.executable, sys.executable, *sys.argv)  # Programm neu starten
    except OSError as e:
        print(f"Fehler beim Ausführen des Updates: {e}")
        sg.popup_error(f"Fehler beim Ausführen des Updates:\n{e}", title="Update-Fehler")

# --- Spiellogik ---
anzahl_richtig = 0

# --- Schwierigkeit laden oder auswählen ---
try:
    with open('settings.ini', 'r') as f:
        schwierigkeit, highscore = lade_einstellungen()
except FileNotFoundError:
    # ... (Schwierigkeitsfenster-Code bleibt unverändert)

# --- Datum generieren basierend auf der Schwierigkeit ---
# ... (Code zum Generieren des Datums bleibt unverändert)

window = hauptfenster()

# --- Auf Updates überprüfen ---
neueste_version = check_for_updates()
if neueste_version and neueste_version > AKTUELLE_VERSION:
    if sg.popup_yes_no(f"Eine neue Version ({neueste_version}) ist verfügbar!\nMöchten Sie das Update herunterladen und installieren?", title="Update verfügbar") == "Yes":
        if download_update(neueste_version):
            update_ausfuehren()

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Beenden':
        break

    # ... (Code für Anleitung, Tipps und Einstellungen bleibt unverändert)

    richtiger_wochentag = berechne_wochentag(aktuelles_datum.day, aktuelles_datum.month, aktuelles_datum.year)

    if event == richtiger_wochentag:
        # ... (Spiellogik für richtige Antwort bleibt unverändert)
    elif event in WOCHENTAGE:
        # ... (Spiellogik für falsche Antwort bleibt unverändert)

window.close()