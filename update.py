import os
import urllib.request
import zipfile

def download_and_extract_zip(url, output_dir):
    """
    Lädt eine ZIP-Datei von der angegebenen URL herunter und entpackt sie.
    
    Args:
        url (str): URL der ZIP-Datei.
        output_dir (str): Zielverzeichnis für die entpackten Dateien.
    """
    zip_path = "img.zip"

    try:
        # Lade die ZIP-Datei herunter
        print(f"Lade {url} herunter...")
        urllib.request.urlretrieve(url, zip_path)
        print("Download abgeschlossen.")

        # Entpacke die ZIP-Datei
        print(f"Entpacke {zip_path} nach {output_dir}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)
        print("Entpacken abgeschlossen.")

        # Entferne die ZIP-Datei nach dem Entpacken
        os.remove(zip_path)
        print("Temporäre Datei img.zip wurde entfernt.")

    except Exception as e:
        print(f"Fehler beim Herunterladen oder Entpacken: {e}")

if __name__ == "__main__":
    img_url = "https://github.com/blobb999/TitanWar-Combo-Helper/raw/main/img.zip"
    target_dir = "./"
    
    # Sicherstellen, dass das Zielverzeichnis existiert
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Lade und entpacke die ZIP-Datei
    download_and_extract_zip(img_url, target_dir)
