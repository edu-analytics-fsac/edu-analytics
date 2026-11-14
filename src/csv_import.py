"""Import de fichiers CSV de notes dans un DataFrame pandas."""
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = ["student", "course", "grade"]


def load_students_csv(path: str | Path) -> pd.DataFrame:
    """Lit un CSV et retourne un DataFrame avec les colonnes student, course, grade.

    Lève FileNotFoundError si le fichier n'existe pas,
    et ValueError si le CSV est vide (en-tête seulement) ou mal formé.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError(f"Le fichier CSV est vide (en-tête seulement) : {file_path}")

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV : {missing}")

    return df[REQUIRED_COLUMNS]