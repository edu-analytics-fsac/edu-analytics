"""Classement des étudiants par moyenne."""
import pandas as pd


def rank_students(averages: pd.Series) -> pd.Series:
    """Rang de chaque étudiant (1 = meilleure moyenne).

    Les ex aequo ont le même rang et le suivant saute des rangs (1, 1, 3).
    Les moyennes manquantes ne sont pas classées (rang <NA>).
    La Series d'origine n'est jamais modifiée.
    """
    if not isinstance(averages, pd.Series):
        raise TypeError("Une Series pandas est attendue.")

    values = pd.to_numeric(averages, errors="coerce")
    return values.rank(ascending=False, method="min").astype("Int64")


def ranking_table(averages: pd.Series) -> pd.DataFrame:
    """Tableau trié par rang avec les colonnes student_id, average, rank.

    Les étudiants sans moyenne sont exclus. À rang égal, l'ordre suit l'index.
    """
    ranks = rank_students(averages)
    table = pd.DataFrame({
        "average": pd.to_numeric(averages, errors="coerce"),
        "rank": ranks,
    })
    table = table.dropna(subset=["rank"]).sort_index().sort_values("rank", kind="stable")
    table.index.name = "student_id"
    return table.reset_index()