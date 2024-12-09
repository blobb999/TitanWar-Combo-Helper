#utils.py:

import os
import sys
import json
from PIL import Image, ImageTk


def get_localized_image_name(name, language, data):
    """
    Gibt den lokalen Namen eines Charakters zurück, basierend auf der Sprachkonfiguration und Daten.
    
    Args:
        name (str): Der Charaktername.
        language (str): Aktuelle Sprache ("EN" oder "DE").
        data (dict): Kartendaten mit Übersetzungen.
    
    Returns:
        str: Lokalisierter Name des Charakters.
    """
    for card in data.values():
        for char in card["characters"]:
            if char.get(language) == name:
                return char.get("DE")  # Fallback auf Deutsch
    return name  # Standardname, falls keine Übersetzung verfügbar

def get_resource_path(relative_path):
    """
    Holt den absoluten Pfad zur Ressource, egal ob das Programm als .exe oder .py läuft.
    """
    try:
        # PyInstaller verwendet einen temporären Ordner, wenn es gebündelt wird.
        base_path = sys._MEIPASS
    except AttributeError:
        # Wenn nicht gebündelt, benutze das aktuelle Verzeichnis.
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_data(data_file):
    """
    Lädt Daten aus einer JSON-Datei.
    """
    full_path = get_resource_path(data_file)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"{full_path} fehlt. Bitte erstellen Sie die Datei mit den erforderlichen Daten.")
    with open(full_path, "r", encoding="utf-8") as file:
        return json.load(file)

def load_config(config_file):
    """
    Lädt die Konfigurationsdaten aus der Datei.
    Gibt drei Werte zurück:
    - Spracheinstellung
    - Ausgeschlossene Charaktere
    - Teams
    """
    language = "EN"  # Standardwert
    excluded = set()
    teams = {}

    if not os.path.exists(config_file):
        return language, excluded, teams

    with open(config_file, "r") as file:
        current_section = None
        for line in file:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]
            elif current_section == "Settings" and ":" in line:
                key, value = line.split(":", 1)
                if key.strip() == "language":
                    language = value.strip()
            elif current_section == "Excluded":
                excluded.add(line)
            elif current_section == "Teams" and ":" in line:
                team_name, characters = line.split(":", 1)
                teams[team_name.strip()] = [char.strip() for char in characters.split(",") if char.strip()]
    
    return language, excluded, teams

def save_config(config_file, language, excluded, teams):
    """
    Speichert die Konfigurationsdaten in die Datei.
    """
    with open(config_file, "w") as file:
        # Schreibe Spracheinstellung
        file.write("[Settings]\n")
        file.write(f"language: {language}\n\n")

        # Schreibe ausgeschlossene Charaktere
        file.write("[Excluded]\n")
        for char in sorted(excluded):
            file.write(f"{char}\n")

        # Schreibe Teams
        file.write("\n[Teams]\n")
        for team_name, characters in teams.items():
            file.write(f"{team_name}: {','.join(characters)}\n")

def load_image(image_path, size, language=None, data=None, char_name=None):
    """
    Lädt ein Bild basierend auf der Sprachpräferenz. Fallback auf Deutsch bei fehlenden Dateien.
    """
    # Wenn char_name nicht angegeben ist, laden Sie das Bild wie gewohnt
    if char_name is None or data is None or language is None:
        try:
            img = Image.open(image_path).resize(size)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Fehler beim Laden des Bildes {image_path}: {e}")
            raise

    # Übersetzte Namen und lokalisierte Pfade nur verwenden, wenn char_name angegeben ist
    localized_name = get_localized_image_name(char_name, language, data)
    localized_path = os.path.join("./img/chars", f"{localized_name}.jpg")
    
    if not os.path.exists(localized_path):
        print(f"Bilddatei {localized_path} nicht gefunden. Platzhalter wird verwendet.")
        localized_path = "./img/placeholder.jpg"  # Fallback
    try:
        img = Image.open(localized_path).resize(size)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Fehler beim Laden des Bildes {localized_path}: {e}")
        raise

def save_team(config_file, team_name, characters):
    """
    Speichert ein Team in der Konfigurationsdatei.
    """
    if not os.path.exists(config_file):
        open(config_file, "w").close()

    with open(config_file, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        found_team = False

        # Überschreibe das gewählte Team
        for line in lines:
            if line.startswith(f"{team_name}:"):
                file.write(f"{team_name}: {','.join(characters)}\n")
                found_team = True
            else:
                file.write(line)

        # Falls das Team nicht existiert, füge es hinzu
        if not found_team:
            file.write(f"{team_name}: {','.join(characters)}\n")
        file.truncate()

def load_team(config_file, team_name):
    """
    Lädt ein Team aus der Konfigurationsdatei.
    """
    if not os.path.exists(config_file):
        return []

    with open(config_file, "r") as file:
        for line in file:
            if line.startswith(f"{team_name}:"):
                return [char.strip() for char in line.strip().split(":")[1].split(",") if char.strip()]
    return []



