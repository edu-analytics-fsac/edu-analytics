"""Import de fichiers CSV de notes dans un DataFrame pandas."""
from pathlib import Path
import pandas as pd

# On vérifie la présence des colonnes essentielles de notre dataset
REQUIRED_COLUMNS = ["student_id", "course", "grade"]


def load_students_csv(path: str | Path) -> pd.DataFrame:
    """Lit un CSV et retourne un DataFrame avec les données des étudiants.

    Lève FileNotFoundError si le fichier n'existe pas,
    et ValueError si le CSV est vide (en-tête seulement) ou s'il manque des colonnes.
    """
    file_path = Path(path)
    
    # 1. Vérifier si le fichier existe
    if not file_path.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    # 2. Lire le fichier
    df = pd.read_csv(file_path)

    # 3. Vérifier si le fichier est vide
    if df.empty:
        raise ValueError(f"Le fichier CSV est vide (en-tête seulement) : {file_path}")

    # 4. Vérifier si les colonnes requises sont présentes
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV : {missing}")

    # On retourne tout le DataFrame pour que l'équipe puisse utiliser 
    # les autres colonnes (school, sex, age, absences, etc.)
    return df