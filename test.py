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
AKTUELLE_VERSION = "1.1"  # Aktuelle Version des Programms
UPDATE_URL = "https://raw.githubusercontent.com/crystalliizee/Wochentage-berechnen/refs/heads/main/version.txt"  # URL zur neuesten Versionsnummer

def ist_schaltjahr(jahr):
    """Prüft, ob ein Jahr ein Schaltjahr ist."""
    return (jahr % 4 == 0 and jahr % 100 != 0) or (jahr % 400 == 0)

def monatscode(monat, jahr):
    """Gibt den Monatscode für einen bestimmten Monat und Jahr zurück."""
    if ist_schaltjahr(jahr) and monat in [1, 2]:
        return MONATSCODES[monat - 1] - 1
    return MONATSCODES[monat - 1]

def jahrescode(jahr):
    """Berechnet den Jahrescode gemäß der Formel."""
    jahr_zwei_ziffern = jahr % 100
    code = (jahr_zwei_ziffern + jahr_zwei_ziffern // 4) % 7
    return code

def jahrhundertcode(jahr):
    """Gibt den Jahrhundertcode zurück."""
    jahrhundert = jahr // 100
    return JAHRHUNDERTCODES.get(jahrhundert, 0)

def berechne_wochentag(tag, monat, jahr):
    """Berechnet den Wochentag für ein gegebenes Datum."""
    code = (jahrhundertcode(jahr) + jahrescode(jahr) + monatscode(monat, jahr) + tag) % 7
    return WOCHENTAGE[code]

def wochentag_als_string(datum):
    """Gibt den Wochentag als String zurück."""
    return WOCHENTAGE[datum.weekday()]

def zufaelliges_datum(start_jahr=1900, end_jahr=2024):
    """Generiert ein zufälliges gültiges Datum."""
    jahr = random.randint(start_jahr, end_jahr)
    monat = random.randint(1, 12)
    max_tag = calendar.monthrange(jahr, monat)[1]
    tag = random.randint(1, max_tag)
    return datetime.date(jahr, monat, tag)

# --- GUI Fenster ---

def tipps_fenster(datum):
    """Erstellt das Tipps-Fenster mit den Codes für das gegebene Datum."""
    monat = aktuelles_datum.month
    jahr = aktuelles_datum.year
    monats_code = monatscode(monat, jahr)
    jahres_code = jahrescode(jahr)
    jahrhundert_code = jahrhundertcode(jahr)

    layout = [
        [sg.Text('Codes für das Datum:', font=('Helvetica', 16))],
        [sg.Text(f'{aktuelles_datum.strftime("%d.%m.%Y")}', font=('Helvetica', 14))],
        [sg.Text('')],
        [sg.Text(f'Monatscode: {monats_code}', font=('Helvetica', 12))],
        [sg.Text(f'Jahrescode: {jahres_code}', font=('Helvetica', 12))],
        [sg.Text(f'Jahrhundertcode: {jahrhundert_code}', font=('Helvetica', 12))],
        [sg.Text('')],
        [sg.Column([[sg.Button('Zurück', font=('Helvetica', 12))]], justification='center')],
    ]
    return sg.Window('Tipps', layout, finalize=True, size=(300, 300))

def anleitung_fenster():
    """Erstellt das Anleitung-Fenster."""
    layout = [
        [sg.Text('Anleitung zur Berechnung des Wochentags', font=('Helvetica', 16))],
        [sg.Text('Monatscode:', font=('Helvetica', 12))],
        [sg.Text('Januar: 0', font=('Helvetica', 12)), sg.Text('Februar: 3', font=('Helvetica', 12)), sg.Text('März: 3', font=('Helvetica', 12))],
        [sg.Text('April: 6', font=('Helvetica', 12)), sg.Text('Mai: 1', font=('Helvetica', 12)), sg.Text('Juni: 4', font=('Helvetica', 12))],
        [sg.Text('Juli: 6', font=('Helvetica', 12)), sg.Text('August: 2', font=('Helvetica', 12)), sg.Text('September: 5', font=('Helvetica', 12))],
        [sg.Text('Oktober: 0', font=('Helvetica', 12)), sg.Text('November: 3', font=('Helvetica', 12)), sg.Text('Dezember: 5', font=('Helvetica', 12))],
        [sg.Text('')],
        [sg.Text('Jahrescode:', font=('Helvetica', 12))],
        [sg.Text('Berechnung: (letzte zwei Stellen des Jahres + (letzte zwei Stellen des Jahres // 4)) % 7', font=('Helvetica', 12))],
        [sg.Text('')],
        [sg.Text('Jahrhundertcode:', font=('Helvetica', 12))],
        [sg.Text('1700-1799: 4', font=('Helvetica', 12)), sg.Text('1800-1899: 2', font=('Helvetica', 12))],
        [sg.Text('1900-1999: 0', font=('Helvetica', 12)), sg.Text('2000-2099: 6', font=('Helvetica', 12))],
        [sg.Text('2100-2199: 4', font=('Helvetica', 12))],
        [sg.Text('')],
        [sg.Text('Berechnung des Wochentags:', font=('Helvetica', 12))],
        [sg.Text('1. Berechne den Monatscode, Jahrescode und Jahrhundertcode.', font=('Helvetica', 12))],
        [sg.Text('2. Addiere den Tag, den Monatscode, den Jahrescode und den Jahrhundertcode.', font=('Helvetica', 12))],
        [sg.Text('3. Dividiere die Summe durch 7 und nimm den Rest.', font=('Helvetica', 12))],
        [sg.Text('4. Der Rest entspricht dem Wochentag (0=Sonntag, 1=Montag, ..., 6=Samstag).', font=('Helvetica', 12))],
        [sg.Text('')],
        [sg.Column([[sg.Button('Zurück', font=('Helvetica', 12))]], justification='center')],
    ]
    return sg.Window('Anleitung', layout, finalize=True, size=(600, 600))

def hauptfenster():
    """Erstellt das Hauptfenster des Spiels."""
    sg.theme('DarkTeal9')
    layout = [
        [sg.Text('Wochentags-Challenge', font=('Helvetica', 24), justification='center')],  # Titel geändert
        [sg.Text(f"Version {AKTUELLE_VERSION}", font=('Helvetica', 10), justification='center')],  # Versionsanzeige hinzugefügt
        [sg.Text('Errate den Wochentag für das folgende Datum:', font=('Helvetica', 18), justification='center')],
        [sg.Text(f"{aktuelles_datum.strftime('%d.%m.%Y')}", key='-DATUM-', font=('Helvetica', 24), justification='center')],
        [sg.Button(w, size=(10, 2), font=('Helvetica', 14)) for w in WOCHENTAGE],
        [sg.Text('', key='-ERGEBNIS-', font=('Helvetica', 14), text_color='red', justification='center')],
        [sg.Text('Highscore:', font=('Helvetica', 16)), sg.Text(highscore, key='-HIGHSCORE-', font=('Helvetica', 16))],
        [sg.Button('Anleitung', font=('Helvetica', 14)), sg.Button('Tipps', font=('Helvetica', 14)), sg.Button('Einstellungen', font=('Helvetica', 14)), sg.Button('Beenden', font=('Helvetica', 14))]
    ]
    return sg.Window('Wochentags-Challenge', layout, finalize=True, element_justification='c')  # Fenstertitel geändert
    element_justification='c'

def schwierigkeitsfenster():
    """Erstellt das Fenster zur Auswahl der Schwierigkeit."""
    layout = [
        [sg.Text('Wähle die Schwierigkeit:', font=('Helvetica', 16))],
        [sg.Radio('Leicht (1900-2024)', "RADIO1", default=True, key='-LEICHT-', font=('Helvetica', 12))],
        [sg.Radio('Mittel (1800-2024)', "RADIO1", key='-MITTEL-', font=('Helvetica', 12))],
        [sg.Radio('Schwer (1700-2024)', "RADIO1", key='-SCHWER-', font=('Helvetica', 12))],
        [sg.Button('Starten', font=('Helvetica', 12)), sg.Button('Abbrechen', font=('Helvetica', 12))]
    ]
    return sg.Window('Schwierigkeit', layout, finalize=True, element_justification='c')

# --- Einstellungen speichern und laden ---
def lade_einstellungen():
    """Lädt die Schwierigkeitseinstellungen aus der settings.ini Datei."""
    config = configparser.ConfigParser()
    try:
        with open('settings.ini', 'r') as f:  # Versuche die Datei zu öffnen
            config.read_file(f)  # Lese die Datei, wenn sie existiert
            schwierigkeit = config['Einstellungen']['Schwierigkeit']
            highscore = int(config['Einstellungen']['Highscore'])
    except FileNotFoundError:  # Wenn die Datei nicht existiert
        schwierigkeit = 'leicht'  # Standardwerte setzen
        highscore = 0
        speichere_einstellungen(schwierigkeit, highscore)  # Neue Datei erstellen und speichern
    except KeyError:
        schwierigkeit = 'leicht'  # Standardwerte setzen
        highscore = 0
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
        response.raise_for_status()
        neueste_version = response.text.strip()
        
        # Versionsnummern in Tupel umwandeln
        aktuelle_version_tupel = tuple(map(int, AKTUELLE_VERSION.split('.')))
        neueste_version_tupel = tuple(map(int, neueste_version.split('.')))

        return neueste_version if neueste_version_tupel > aktuelle_version_tupel else None  # Nur zurückgeben, wenn die neueste Version größer ist
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Überprüfen auf Updates: {e}")
        return None

def download_update(neueste_version):
    """Lädt die neueste Version des Skripts herunter."""
    try:
        response = requests.get("https://raw.githubusercontent.com/crystalliizee/Wochentage-berechnen/refs/heads/main/test.py")  # URL zum Skript
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
        schwierigkeit, highscore = lade_einstellungen()  # Highscore laden
except FileNotFoundError:
    # --- Schwierigkeit auswählen ---
    schwierigkeit_window = schwierigkeitsfenster()
    highscore = 0  # highscore hier definieren
    while True:
        event_schwierigkeit, values_schwierigkeit = schwierigkeit_window.read()
        if event_schwierigkeit in (sg.WIN_CLOSED, 'Abbrechen'):
            schwierigkeit_window.close()
            exit()
        if event_schwierigkeit == 'Starten':
            schwierigkeit = 'leicht'
            if values_schwierigkeit['-MITTEL-']:
                schwierigkeit = 'mittel'
            elif values_schwierigkeit['-SCHWER-']:
                schwierigkeit = 'schwer'
            speichere_einstellungen(schwierigkeit, highscore)  # Einstellungen speichern
            break
    schwierigkeit_window.close()

# --- Datum generieren basierend auf der Schwierigkeit ---
start_jahr = 1900
if schwierigkeit == 'mittel':
    start_jahr = 1800
elif schwierigkeit == 'schwer':
    start_jahr = 1700
aktuelles_datum = zufaelliges_datum(start_jahr, 2024)

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

    if event == 'Anleitung':
        anleitung_window = anleitung_fenster()
        while True:
            event_hilfe, values_hilfe = anleitung_window.read()
            if event_hilfe == sg.WINDOW_CLOSED or event_hilfe == 'Zurück':
                anleitung_window.close()
                break

    if event == 'Tipps':
        tipps_window = tipps_fenster(aktuelles_datum)
        while True:
            event_tipps, values_tipps = tipps_window.read()
            if event_tipps == sg.WINDOW_CLOSED or event_tipps == 'Zurück':
                tipps_window.close()
                break

    if event == 'Einstellungen':
        # --- Einstellungen ändern ---
        layout_einstellungen = [
            [sg.Text('Wähle die Schwierigkeit:', font=('Helvetica', 12))],
            [sg.Combo(['Leicht (1900-2024)', 'Mittel (1800-2024)', 'Schwer (1700-2024)'], default_value=f'{schwierigkeit.capitalize()} ({start_jahr}-2024)', key='-SCHWIERIGKEIT-', font=('Helvetica', 12))],
            [sg.Button('Highscore zurücksetzen', font=('Helvetica', 12)), sg.Button('Speichern', font=('Helvetica', 12)), sg.Button('Abbrechen', font=('Helvetica', 12))]  # Highscore-Button hinzugefügt
        ]
        einstellungen_window = sg.Window('Einstellungen', layout_einstellungen, finalize=True, element_justification='c')
        while True:
            event_einstellungen, values_einstellungen = einstellungen_window.read()
            if event_einstellungen in (sg.WIN_CLOSED, 'Abbrechen'):
                einstellungen_window.close()
                break
            if event_einstellungen == 'Speichern':
                schwierigkeit = values_einstellungen['-SCHWIERIGKEIT-'].split()[0].lower()
                speichere_einstellungen(schwierigkeit, highscore)
                # --- Datum neu generieren basierend auf der neuen Schwierigkeit ---
                start_jahr = 1900
                if schwierigkeit == 'mittel':
                    start_jahr = 1800
                elif schwierigkeit == 'schwer':
                    start_jahr = 1700
                aktuelles_datum = zufaelliges_datum(start_jahr, 2024)
                window['-DATUM-'].update(f"{aktuelles_datum.strftime('%d.%m.%Y')}")
                einstellungen_window.close()
                break
            if event_einstellungen == 'Highscore zurücksetzen':  # Event für Highscore zurücksetzen
                highscore = 0
                window['-HIGHSCORE-'].update(highscore)
                speichere_einstellungen(schwierigkeit, highscore)  # Highscore speichern

    richtiger_wochentag = berechne_wochentag(aktuelles_datum.day, aktuelles_datum.month, aktuelles_datum.year)

    if event == richtiger_wochentag:
        anzahl_richtig += 1
        window['-ERGEBNIS-'].update(f'Richtig! ({anzahl_richtig} in Folge)', text_color='green')
        aktuelles_datum = zufaelliges_datum(start_jahr, 2024)
        window['-DATUM-'].update(f"{aktuelles_datum.strftime('%d.%m.%Y')}")
    elif event in WOCHENTAGE:
        window['-ERGEBNIS-'].update(f'Falsch. Der richtige Wochentag ist {richtiger_wochentag}.', text_color='red')
        if anzahl_richtig > highscore:
            highscore = anzahl_richtig
            window['-HIGHSCORE-'].update(highscore)
            speichere_einstellungen(schwierigkeit, highscore)  # Highscore speichern
        anzahl_richtig = 0

window.close()