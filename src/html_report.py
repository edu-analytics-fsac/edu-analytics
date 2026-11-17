"""Génération d'un rapport HTML français à partir d'un fichier CSV."""

from html import escape
from pathlib import Path

import pandas as pd

from averages import course_averages, student_averages
from csv_import import load_students_csv
from data_quality import check_data_quality
from distribution_stats import distribution_stats
from ranking import ranking_table


def _valid_grades_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Retourne une copie contenant uniquement les notes valides."""
    valid_grades = pd.to_numeric(df["grade"], errors="coerce")
    valid = valid_grades.between(0, 20)
    result = df.loc[valid].copy()
    result["grade"] = valid_grades.loc[valid]
    return result


def _render_quality_report(report: dict) -> str:
    """Construit le tableau HTML des indicateurs de qualité."""
    rows = [
        ("Nombre de lignes", report["total_rows"]),
        ("Valeurs manquantes", report["total_missing_values"]),
        ("Lignes dupliquées", report["duplicate_rows"]),
        ("Doublons étudiant-matière", report["duplicate_student_courses"]),
        ("Étudiants dans plusieurs matières", report["students_in_multiple_courses"]),
        ("Notes invalides", report["invalid_grades"]),
        ("Âges invalides", report["invalid_age"]),
        ("Temps d'étude invalides", report["invalid_studytime"]),
        ("Absences invalides", report["invalid_absences"]),
        ("Sexes invalides", report["invalid_sex"]),
    ]
    if report["missing_columns"]:
        rows.append(("Colonnes manquantes", ", ".join(report["missing_columns"])))

    table_rows = "".join(
        f"<tr><th>{escape(str(label))}</th><td>{escape(str(value))}</td></tr>"
        for label, value in rows
    )
    return f"<table><tbody>{table_rows}</tbody></table>"


def _render_distribution(stats: dict) -> str:
    """Construit le tableau HTML des statistiques de notes."""
    labels = {
        "count": "Effectif",
        "mean": "Moyenne",
        "median": "Médiane",
        "std": "Écart-type",
        "q1": "Premier quartile (Q1)",
        "q3": "Troisième quartile (Q3)",
        "min": "Minimum",
        "max": "Maximum",
    }
    table_rows = "".join(
        (
            f"<tr><th>{escape(labels.get(key, key))}</th>"
            f"<td>{value:.2f}</td></tr>"
            if isinstance(value, float)
            else (
                f"<tr><th>{escape(labels.get(key, key))}</th>"
                f"<td>{escape(str(value))}</td></tr>"
            )
        )
        for key, value in stats.items()
    )
    return f"<table><tbody>{table_rows}</tbody></table>"


def _render_table(df: pd.DataFrame, index: bool = False) -> str:
    """Convertit un DataFrame en tableau HTML sûr et lisible."""
    return df.to_html(
        index=index,
        border=0,
        classes="data-table",
        na_rep="-",
        escape=True,
    )


def generate_html_report(csv_path: str | Path) -> str:
    """Génère et retourne le code HTML du rapport pour un fichier CSV.

    Les notes hors de l'intervalle [0, 20] et les notes non numériques sont
    signalées dans la qualité des données puis exclues des statistiques.
    """
    df = load_students_csv(csv_path)
    quality = check_data_quality(df)
    valid_df = _valid_grades_dataframe(df)

    course_table = course_averages(valid_df).rename("Moyenne").reset_index()
    course_table.columns = ["Matière", "Moyenne"]

    top_students = ranking_table(student_averages(valid_df)).head(10)
    top_students.columns = ["Étudiant", "Moyenne", "Rang"]

    stats = distribution_stats(valid_df)

    source_name = escape(Path(csv_path).name)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Rapport EduAnalytics</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2rem auto; max-width: 1100px;
               color: #1f2937; line-height: 1.5; }}
        h1, h2 {{ color: #123b5d; }}
        section {{ margin: 2rem 0; }}
        table {{ border-collapse: collapse; margin-top: 1rem; width: 100%; }}
        th, td {{ border: 1px solid #d1d5db; padding: .55rem .7rem; text-align: left; }}
        th {{ background: #e8f1f8; }}
        .data-table th {{ background: #f3f4f6; }}
    </style>
</head>
<body>
    <h1>Rapport EduAnalytics</h1>
    <p>Source : <strong>{source_name}</strong></p>

    <section>
        <h2>Qualité des données</h2>
        {_render_quality_report(quality)}
    </section>

    <section>
        <h2>Moyennes par matière</h2>
        {_render_table(course_table)}
    </section>

    <section>
        <h2>Classement - top 10</h2>
        {_render_table(top_students)}
    </section>

    <section>
        <h2>Distribution des notes valides</h2>
        {_render_distribution(stats)}
    </section>
</body>
</html>
"""