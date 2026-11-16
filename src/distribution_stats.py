"""Statistiques de distribution des notes (EduAnalytics)."""
from typing import Any, Dict, Union
import pandas as pd


def distribution_stats(
    data: Union[pd.DataFrame, pd.Series],
    column: str = "grade",
) -> Dict[str, Any]:
    """Calcule les statistiques de distribution d'une colonne de notes.

    Calcule la moyenne, la médiane, l'écart-type, les quartiles Q1 et Q3,
    ainsi que le minimum, le maximum et l'effectif.

    Args:
        data: DataFrame ou Series pandas contenant les notes.
        column: Nom de la colonne à analyser si un DataFrame est fourni
            (par défaut 'grade', avec repli automatique sur 'note').

    Returns:
        dict: Dictionnaire contenant count, mean, median, std, q1, q3, min, max.

    Raises:
        TypeError: Si l'entrée n'est ni un DataFrame ni une Series pandas.
        ValueError: Si le jeu de données est vide ou si la colonne est introuvable.
    """
    if not isinstance(data, (pd.DataFrame, pd.Series)):
        raise TypeError("Un DataFrame ou une Series pandas est attendu.")

    if isinstance(data, pd.DataFrame):
        target_col = column
        if target_col not in data.columns:
            if "note" in data.columns and target_col == "grade":
                target_col = "note"
            elif "grade" in data.columns and target_col == "note":
                target_col = "grade"
            else:
                raise ValueError(f"Colonne '{column}' introuvable dans le DataFrame.")

        serie = data[target_col]
        if serie.empty:
            raise ValueError(f"La colonne '{target_col}' est vide.")
    else:
        if data.empty:
            raise ValueError("La Series est vide.")
        serie = data
        target_col = "grade"

    grades = pd.to_numeric(serie, errors="coerce").dropna()
    if grades.empty:
        raise ValueError(f"La colonne '{target_col}' est vide ou ne contient aucune note valide.")

    std_val = 0.0 if len(grades) <= 1 or pd.isna(grades.std()) else float(grades.std())

    return {
        "count": int(grades.count()),
        "mean": float(grades.mean()),
        "median": float(grades.median()),
        "std": std_val,
        "q1": float(grades.quantile(0.25)),
        "q3": float(grades.quantile(0.75)),
        "min": float(grades.min()),
        "max": float(grades.max()),
    }
