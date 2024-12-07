#TitanWar_Combo_Helper.py:

from tkinter import Tk, Label, Button, Frame, Canvas, Scrollbar
from character_utils import calculate_best_combination, activate_cards
from utils import load_data, save_config, load_config, load_image, save_team, load_team, get_localized_image_name
from image_utils import combine_images, add_overlay, remove_overlay
from gui_layout import setup_gui_layout
from update import download_and_extract_zip
import os
import subprocess

def check_and_update_img():
    """
    Überprüft, ob das Verzeichnis 'img' und die Datei 'data.json' existieren.
    Falls nicht, wird die ZIP-Datei heruntergeladen und entpackt.
    """
    img_url = "https://github.com/blobb999/TitanWar-Combo-Helper/raw/main/img.zip"
    if not os.path.exists("./img") or not os.path.exists("data.json"):
        print("Notwendige Dateien fehlen. Update wird durchgeführt...")
        download_and_extract_zip(img_url, "./")
    else:
        print("Alle erforderlichen Dateien sind vorhanden.")

# Konfigurations- und Datenpfade
CONFIG_FILE = "config.cfg"
BUFFS_DIR = "./img/Buffs"
DATA_FILE = "data.json"

# Daten laden
data = load_data(DATA_FILE)

class CardSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TitanWar Combo Helper")

        # Sprache Laden
        self.language, self.excluded_characters, self.teams = load_config(CONFIG_FILE)

        # Initialisierungen
        self.selected_characters = []
        self.activated_cards = set()

        self.img_dir = "./img/chars"
        self.overlay_path = os.path.join(self.img_dir, "deactivated.png")
        self.overlay_image = (
            load_image(self.overlay_path, (80, 80)) if os.path.exists(self.overlay_path) else None
        )

        # GUI-Aufbau über ausgelagertes Layout
        setup_gui_layout(self)

        # Lade die Charaktere
        self.load_characters()

        # Aktualisiere Texte basierend auf Sprache
        self.update_texts()

    def load_characters(self):
        row_limit = 12
        current_row = 0
        current_column = 0

        for file in os.listdir(self.img_dir):
            if file.endswith(".jpg"):
                char_name = file.replace(".jpg", "")
                self.create_character_button(char_name, current_row, current_column)

                current_column += 1
                if current_column >= row_limit:
                    current_column = 0
                    current_row += 1

    def create_character_button(self, name, row, column):
        try:
            localized_name = get_localized_image_name(name, self.language, data)
            img_path = os.path.join(self.img_dir, f"{localized_name}.jpg")
            
            photo = load_image(img_path, (80, 80))
            btn = Button(self.inner_frame, image=photo, text=name, compound="top")
            btn.image = photo
            btn.grid(row=row, column=column, padx=5, pady=5)

            # Linksklick: Auswählen/Abwählen, Rechtsklick: Ausschließen/Wieder aufnehmen
            btn.bind("<Button-1>", lambda e: self.select_character(name))
            btn.bind("<Button-3>", lambda e: self.toggle_exclusion(name, btn))

            # Overlay anwenden, falls Charakter ausgeschlossen ist
            if name in self.excluded_characters:
                self.add_overlay(btn)

        except Exception as e:
            print(f"Fehler beim Laden des Bildes für {name}: {e}")

    def select_character(self, name):
        if name in self.selected_characters:
            self.selected_characters.remove(name)
        else:
            if len(self.selected_characters) < 6:
                self.selected_characters.append(name)
        self.update_selection()

    def toggle_exclusion(self, name, button):
        """
        Aktiviert/Deaktiviert einen Charakter und aktualisiert die Anzeige.
        """
        if name in self.excluded_characters:
            self.excluded_characters.remove(name)
            self.remove_overlay(button)
        else:
            self.excluded_characters.add(name)
            self.add_overlay(button)

        # Speichere die Änderungen in der Konfigurationsdatei
        save_config(CONFIG_FILE, self.language, self.excluded_characters, self.teams)
        self.update_selection()



    def add_overlay(self, button):
        """
        Fügt ein Overlay-Bild über den Charakterbutton.
        """
        char_name = button.cget("text")
        img_path = os.path.join(self.img_dir, f"{char_name}.jpg")
        if self.overlay_path:
            overlay_image = combine_images(img_path, self.overlay_path, (80, 80))
            if overlay_image:
                button.configure(image=overlay_image)
                button.image = overlay_image

    def remove_overlay(self, button):
        """
        Entfernt das Overlay und stellt das Originalbild wieder her.
        """
        char_name = button.cget("text")
        img_path = os.path.join(self.img_dir, f"{char_name}.jpg")
        try:
            photo = load_image(img_path, (80, 80))
            button.configure(image=photo)
            button.image = photo
        except Exception as e:
            print(f"Fehler beim Wiederherstellen des Bildes für {char_name}: {e}")

    def update_selection(self):
        """
        Aktualisiert die Anzeige der ausgewählten Charaktere und der aktivierten Karten.
        """
        # Aktualisiere die Anzeige der ausgewählten Charaktere
        for widget in self.selected_characters_frame.winfo_children():
            widget.destroy()

        positions = ["center", "left", "right", "center", "left", "right"]
        rows = [0, 0, 0, 1, 1, 1]

        for index, char in enumerate(self.selected_characters):
            img_path = os.path.join(self.img_dir, f"{char}.jpg")
            try:
                photo = load_image(img_path, (80, 80))
                lbl = Button(
                    self.selected_characters_frame,
                    image=photo,
                    text=char,
                    compound="top",
                    command=lambda c=char: self.select_character(c),
                )
                lbl.image = photo
                lbl.grid(row=rows[index], column=positions.index(positions[index]), padx=5, pady=5)
            except Exception as e:
                print(f"Fehler beim Anzeigen des Bildes für {char}: {e}")

        # Aktivierte Karten aktualisieren
        self.activated_cards = activate_cards(data, self.selected_characters, self.language)

        # Entferne alte Kartenbuffs
        for widget in self.activated_cards_frame.winfo_children():
            widget.destroy()

        # Neue Kartenbuffs anzeigen
        for index, card in enumerate(self.activated_cards):
            buff_image_path = os.path.join(BUFFS_DIR, f"{card['name']['DE']}.jpg")  # Bild immer auf DE basieren
            try:
                if os.path.exists(buff_image_path):
                    buff_photo = load_image(buff_image_path, (50, 50))
                    frame = Frame(self.activated_cards_frame)
                    frame.grid(row=0, column=index, padx=5, pady=5)

                    img_label = Label(frame, image=buff_photo)
                    img_label.image = buff_photo
                    img_label.pack(side="top")

                    # Buff-Name und Typ in der ausgewählten Sprache anzeigen
                    text_label = Label(
                        frame,
                        text=f"{card['name'][self.language]} ({card['type'][self.language]})"
                    )
                    text_label.pack(side="top")
                else:
                    Label(
                        self.activated_cards_frame,
                        text=f"{card['name'][self.language]} ({card['type'][self.language]})"
                    ).grid(row=0, column=index, padx=5, pady=5)
            except Exception as e:
                print(f"Fehler beim Anzeigen des Buff-Bildes für {card['name']['DE']}: {e}")

    def autofill_characters(self):
        def translate_type(selected_type, language):
            """
            Übersetzt den Typ von EN zu DE und umgekehrt.
            """
            type_mapping = {
                "EN": {"random": "random", "attack": "Angriff", "defense": "Verteidigung"},
                "DE": {"zufällig": "random", "angriff": "attack", "verteidigung": "defense"}
            }
            # Normalisierung des Typs (in Kleinbuchstaben umwandeln)
            selected_type = selected_type.lower()
            
            translated = type_mapping.get(language, {}).get(selected_type, None)
            if translated is None:
                print(f"Fehler: Typ '{selected_type}' konnte nicht übersetzt werden. Fallback auf 'random'.")
                return "random"
            print(f"Übersetzter Typ: {translated}")
            return translated
        
        print("Autofill gestartet...")  # Debugging-Ausgabe

        # Ausgewählten Typ aus der Filtervariable abrufen
        selected_type_key = self.filter_var.get()
        print(f"Selected type key: {selected_type_key}")  # Debugging-Ausgabe

        # Typ übersetzen
        translated_type = translate_type(selected_type_key.lower(), self.language)
        print(f"Selected type (localized): {translated_type}")  # Debugging-Ausgabe

        # Verfügbare Charaktere sammeln
        used_characters = {char for team_chars in self.teams.values() for char in team_chars}
        available_characters = {
            char[self.language] for buff in data.values() for char in buff["characters"]
        } - self.excluded_characters - used_characters

        print(f"Verfügbare Charaktere: {available_characters}")

        if not available_characters:
            print("Keine verfügbaren Charaktere für Autofill.")
            return

        # Debugging: Karten und Typen prüfen
        print("Datenstruktur:")
        for card_name, card_info in data.items():
            print(f"{card_name}: Typ: {card_info['type'][self.language]}, Benötigte Charaktere: {[char[self.language] for char in card_info['characters']]}")

        # Filter gültige Karten
        valid_cards = {
            card_name: card_info
            for card_name, card_info in data.items()
            if translated_type == "random" or card_info["type"][self.language].lower() == selected_type_key.lower()
        }

        if not valid_cards:
            print(f"Keine gültigen Buffs für den Typ '{selected_type_key}'.")
            return

        # Beste Kombination berechnen
        preselected = set(self.selected_characters)
        print(f"Vorab ausgewählte Charaktere: {preselected}")

        best_combination = calculate_best_combination(data, available_characters, preselected, self.language, valid_cards=valid_cards)

        if not best_combination:
            print("Keine optimale Kombination gefunden.")
            return

        print(f"Beste Kombination: {best_combination}")

        # Aktualisiere die Charakterauswahl
        self.selected_characters = list(preselected.union(best_combination))[:6]
        self.update_selection()


    def save_team(self):
        """
        Speichert das aktuelle Team in der Konfigurationsdatei.
        """
        team_name = self.team_var.get()  # Aktuellen Team-Namen abrufen
        self.teams[team_name] = self.selected_characters  # Speichere das Team

        # Speichere alle Konfigurationsdaten
        save_config(CONFIG_FILE, self.language, self.excluded_characters, self.teams)

        # Aktualisiere den Info-Text
        self.info_label.config(
            text=f"{team_name} gespeichert!" if self.language == "DE" else f"{team_name} saved!"
        )



    def select_team(self, team_name):
        """
        Wählt das angegebene Team aus der Konfigurationsdatei aus.
        """
        # Aktualisiere die Auswahlvariable
        self.team_var.set(team_name)

        # Lade das Team aus dem gespeicherten Dictionary
        self.selected_characters = self.teams.get(team_name, [])

        # Aktualisiere die Anzeige
        self.update_selection()

        # Markiere den aktiven Button
        for name, button in self.team_buttons.items():
            if name == team_name:
                button.config(bg="blue", fg="white")  # Hintergrundfarbe für aktives Team
            else:
                button.config(bg="lightgray", fg="black")  # Standardfarbe für andere Teams

        # Aktualisiere den Info-Text
        self.info_label.config(text=f"Aktuelles Team: {team_name}")

    def change_language(self):
        """
        Aktualisiert die Sprache des GUIs.
        """
        self.language = self.language_var.get()
        save_config(CONFIG_FILE, self.language, self.excluded_characters, self.teams)

        # Aktualisiere alle Texte basierend auf der neuen Sprache
        self.update_texts()

    def update_texts(self):
        """
        Aktualisiert die Texte im GUI basierend auf der aktuellen Sprache.
        """
        # Labels aktualisieren
        self.selected_label.config(text="Selected Characters:" if self.language == "EN" else "Ausgewählte Charaktere:")
        self.cards_label.config(text="Activated Cards:" if self.language == "EN" else "Aktivierte Karten:")
        self.info_label.config(text=f"Current Team: {self.team_var.get()}" if self.language == "EN" else f"Aktuelles Team: {self.team_var.get()}")

        # Pulldown-Menü-Optionen aktualisieren
        menu = self.filter_menu["menu"]
        menu.delete(0, "end")  # Entfernt alte Optionen
        for option in self.filter_options[self.language]:
            menu.add_command(label=option, command=lambda value=option: self.filter_var.set(value))
        self.filter_var.set(self.filter_options[self.language][0])  # Standardwert setzen  # Sicherstellen, dass ein Standardwert gesetzt ist
        
        # Aktualisiere den Header des Pulldown-Menüs
        self.filter_var.set(self.filter_options[self.language][0])

        # Sprachumschaltung für Team-Buttons
        for team_name, button in self.team_buttons.items():
            button.config(text=team_name if self.language == "EN" else f"Team {team_name.split()[-1]}")

if __name__ == "__main__":
    check_and_update_img()  # Verzeichnisprüfung und ggf. Update
    root = Tk()
    app = CardSelectorApp(root)
    root.mainloop()
