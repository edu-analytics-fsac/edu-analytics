"""Calcul des moyennes de notes par étudiant et par matière."""
import pandas as pd


def _average_by(df: pd.DataFrame, key: str) -> pd.Series:
    """Moyenne de la colonne 'grade' regroupée par la colonne 'key'.

    Sont ignorées : les notes non numériques, manquantes ou hors de 0 à 20,
    ainsi que les clés vides. Les espaces autour des clés sont supprimés.
    Le DataFrame d'origine n'est jamais modifié.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Un DataFrame pandas est attendu.")

    missing = [c for c in (key, "grade") if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes : {missing}")

    grades = pd.to_numeric(df["grade"], errors="coerce")
    grades = grades.where(grades.between(0, 20))  # notes hors 0-20 ignorées

    keys = df[key].astype("string").str.strip()
    keys = keys.mask(keys == "")  # clés vides ignorées
    result = grades.groupby(keys).mean().round(2)
    result.name = "average"
    return result


def student_averages(df: pd.DataFrame) -> pd.Series:
    """Moyenne des notes par étudiant (index : student_id)."""
    return _average_by(df, "student_id")


def course_averages(df: pd.DataFrame) -> pd.Series:
    """Moyenne des notes par matière (index : course)."""
    return _average_by(df, "course")