
"""Validation de la qualité des données étudiantes."""

import pandas as pd

from csv_import import REQUIRED_COLUMNS


def is_missing(series: pd.Series) -> pd.Series:
    """Détecte les valeurs nulles et les chaînes vides."""
    return (
        series.isna()
        | series.astype("string").str.strip().eq("").fillna(False)
    )


def count_invalid_numeric(
    df: pd.DataFrame,
    column: str,
    minimum: float,
    maximum: float | None = None,
) -> int:
    """Compte les valeurs numériques invalides, hors valeurs manquantes."""
    if column not in df.columns:
        return 0

    values = df[column]
    missing = is_missing(values)
    numeric = pd.to_numeric(values, errors="coerce")

    invalid = numeric.isna() | (numeric < minimum)

    if maximum is not None:
        invalid = invalid | (numeric > maximum)

    # Les valeurs infinies ne sont pas valides.
    invalid = invalid | numeric.isin([float("inf"), float("-inf")])

    return int((~missing & invalid).sum())


def check_data_quality(df: pd.DataFrame) -> dict:
    """Analyse les données sans modifier le DataFrame original."""

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Un DataFrame pandas est attendu.")

    # 1. Colonnes obligatoires
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    # 2. Valeurs manquantes
    missing_values = {
        col: int(is_missing(df[col]).sum())
        for col in df.columns
    }

    # 3. Lignes identiques
    duplicate_rows = int(df.duplicated().sum())

    # 4. Doublons étudiant-cours et étudiants dans plusieurs cours
    duplicate_student_courses = 0
    students_in_multiple_courses = 0

    if {"student_id", "course"}.issubset(df.columns):
        valid = (
            ~is_missing(df["student_id"])
            & ~is_missing(df["course"])
        )

        records = df.loc[valid, ["student_id", "course"]].copy()

        # Supprimer les espaces superflus pour la comparaison
        records["student_id"] = (
            records["student_id"].astype(str).str.strip()
        )
        records["course"] = (
            records["course"].astype(str).str.strip()
        )

        duplicate_student_courses = int(
            records.duplicated(
                subset=["student_id", "course"]
            ).sum()
        )

        course_counts = (
            records.groupby("student_id")["course"].nunique()
        )

        students_in_multiple_courses = int(
            (course_counts > 1).sum()
        )

    # 5. Notes entre 0 et 20
    invalid_grades = count_invalid_numeric(
        df, "grade", 0, 20
    )

    # 6. Âge entre 15 et 22
    invalid_age = count_invalid_numeric(
        df, "age", 15, 22
    )

    # 7. Temps d'étude non négatif
    invalid_studytime = count_invalid_numeric(
        df, "studytime", 0
    )

    # 8. Absences non négatives
    invalid_absences = count_invalid_numeric(
        df, "absences", 0
    )

    # 9. Sexe M ou F
    invalid_sex = 0

    if "sex" in df.columns:
        values = df["sex"]
        missing = is_missing(values)

        invalid_sex = int(
            (~missing & ~values.isin(["M", "F"])).sum()
        )

    return {
        "total_rows": len(df),
        "total_missing_values": sum(missing_values.values()),
        "missing_columns": missing_columns,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "duplicate_student_courses": duplicate_student_courses,
        "students_in_multiple_courses": students_in_multiple_courses,
        "invalid_grades": invalid_grades,
        "invalid_age": invalid_age,
        "invalid_studytime": invalid_studytime,
        "invalid_absences": invalid_absences,
        "invalid_sex": invalid_sex,
        "no_columns": df.shape[1] == 0,
    }
def main():
    """Charge le dataset et affiche le rapport de qualité."""
    from pprint import pprint
    from csv_import import load_students_csv

    df = load_students_csv("data/sample/students.csv")

    report = check_data_quality(df)

    print("=== DATA QUALITY REPORT ===")
    pprint(report)


if __name__ == "__main__":
    main()