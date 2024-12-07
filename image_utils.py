#image_utils.py:

from PIL import Image, ImageTk
import os
from utils import load_image

def add_overlay(button, overlay_image):
    """
    Fügt einem Button ein Overlay hinzu.

    Args:
        button (Button): Der Tkinter-Button.
        overlay_image (ImageTk.PhotoImage): Das Overlay-Bild.
    """
    button.configure(image=overlay_image)
    button.overlay_image = overlay_image

def remove_overlay(button, img_path, size):
    """
    Entfernt das Overlay von einem Button und stellt das ursprüngliche Bild wieder her.

    Args:
        button (Button): Der Tkinter-Button.
        img_path (str): Pfad zum ursprünglichen Bild.
        size (tuple): Größe des Bildes.
    """
    try:
        photo = load_image(img_path, size)
        button.configure(image=photo)
        button.image = photo
    except Exception as e:
        print(f"Fehler beim Wiederherstellen des Bildes: {e}")

def combine_images(base_image_path, overlay_image_path, size):
    """
    Kombiniert ein Basisbild mit einem Overlay-Bild.
    
    Args:
        base_image_path (str): Pfad zum Basisbild.
        overlay_image_path (str): Pfad zum Overlay-Bild.
        size (tuple): Größe des Ausgabebilds (Breite, Höhe).

    Returns:
        ImageTk.PhotoImage: Kombiniertes Bild.
    """
    try:
        # Öffne das Basis- und Overlay-Bild
        base_image = Image.open(base_image_path).resize(size)
        overlay_image = Image.open(overlay_image_path).resize(size)

        # Kombiniere die Bilder (unter Berücksichtigung der Transparenz)
        combined_image = base_image.copy()
        combined_image.paste(overlay_image, (0, 0), overlay_image)

        # Konvertiere in ein tkinter-kompatibles Format
        return ImageTk.PhotoImage(combined_image)
    except Exception as e:
        print(f"Fehler beim Kombinieren der Bilder: {e}")
        return None
