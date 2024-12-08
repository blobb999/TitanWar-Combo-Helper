import threading
import tkinter as tk
from tkinter import ttk
import time

class CalculationFeedback:
    def __init__(self, root, task_function, *task_args, **task_kwargs):
        """
        Erstellt ein Feedback-Fenster für die Berechnung.

        Args:
            root (Tk): Hauptfenster der Anwendung.
            task_function (callable): Die Funktion, die ausgeführt wird.
            *task_args: Argumente für die Aufgabe.
            **task_kwargs: Schlüsselwortargumente für die Aufgabe.
        """
        self.root = root
        self.task_function = task_function
        self.task_args = task_args
        self.task_kwargs = task_kwargs

        self.progress_window = None
        self.progress_bar = None
        self.progress_label = None
        self.progress_details = None

    def show_progress_window(self):
        """
        Zeigt ein Fortschrittsfenster an.
        """
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Berechnung läuft...")
        self.progress_window.geometry("600x300")

        self.progress_label = tk.Label(
            self.progress_window, text="Berechnung wird gestartet...", font=("Arial", 12)
        )
        self.progress_label.pack(pady=20)

        self.progress_bar = ttk.Progressbar(
            self.progress_window, orient="horizontal", length=300, mode="determinate"
        )
        self.progress_bar.pack(pady=20)

        self.progress_details = tk.Text(self.progress_window, height=5, state="disabled")
        self.progress_details.pack(pady=10, padx=10)

        self.countdown_label = tk.Label(
            self.progress_window, text="", font=("Arial", 10, "italic"), fg="gray"
        )
        self.countdown_label.pack(pady=5)

        self.progress_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Fenster kann nicht geschlossen werden

    def update_progress(self, progress, total, message):
        """
        Aktualisiert den Fortschritt.

        Args:
            progress (int): Anzahl abgeschlossener Schritte.
            total (int): Gesamtanzahl der Schritte.
            message (str): Fortschrittsnachricht.
        """
        if self.progress_bar:
            self.progress_bar["maximum"] = total
            self.progress_bar["value"] = progress

        if self.progress_label:
            self.progress_label.config(text=f"{progress}/{total} Schritte abgeschlossen")

        if self.progress_details:
            self.progress_details.config(state="normal")
            self.progress_details.insert("end", f"{message}\n")
            self.progress_details.see("end")
            self.progress_details.config(state="disabled")

    def run_countdown(self, countdown_time):
        """
        Führt einen Countdown aus, bevor das Fenster geschlossen wird.

        Args:
            countdown_time (int): Zeit in Sekunden, bevor das Fenster geschlossen wird.
        """
        for remaining in range(countdown_time, 0, -1):
            self.countdown_label.config(
                text=f"Das Fenster schließt in {remaining} Sekunden..."
            )
            time.sleep(1)  # Warte 1 Sekunde
        self.progress_window.destroy()  # Schließe das Fenster nach dem Countdown

    def run_task_in_thread(self):
        """
        Führt die Aufgabe in einem separaten Thread aus.
        """
        def task_wrapper():
            try:
                # Führt die übergebene Funktion aus und übergibt die Aktualisierungsfunktion
                self.task_function(self.update_progress, *self.task_args, **self.task_kwargs)
            except Exception as e:
                self.update_progress(0, 1, f"Fehler: {str(e)}")
            finally:
                # Starte den Countdown-Timer nach Abschluss
                self.run_countdown(3)  # Zeige Countdown für 3 Sekunden

        threading.Thread(target=task_wrapper, daemon=True).start()

    def start(self):
        """
        Startet das Feedback-Fenster und die Berechnung.
        """
        self.show_progress_window()
        self.run_task_in_thread()
