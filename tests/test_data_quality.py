
"""Tests de la validation de qualité des données."""

from pathlib import Path

import pandas as pd

from csv_import import load_students_csv
from data_quality import check_data_quality


SAMPLE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "sample"
    / "students.csv"
)


def test_real_dataset():
    """Vérifier l'intégration avec le CSV importé."""
    df = load_students_csv(SAMPLE)
    report = check_data_quality(df)

    assert report["total_rows"] == len(df)
    assert report["missing_columns"] == []


def test_missing_values():
    """Détecter les valeurs nulles et les chaînes vides."""
    df = pd.DataFrame({
        "student_id": ["MAT001", "MAT002"],
        "course": ["Mathematics", " "],
        "grade": [15, None],
    })

    report = check_data_quality(df)

    assert report["missing_values"]["course"] == 1
    assert report["missing_values"]["grade"] == 1
    assert report["invalid_grades"] == 0


def test_invalid_grades():
    """Détecter les notes hors limites ou non numériques."""
    df = pd.DataFrame({
        "student_id": ["A", "B", "C", "D", "E"],
        "course": ["Math"] * 5,
        "grade": [10, 25, -3, "abc", None],
    })

    report = check_data_quality(df)

    assert report["invalid_grades"] == 3


def test_duplicate_records():
    """Détecter les doublons étudiant-cours."""
    df = pd.DataFrame({
        "student_id": ["A", "A", "A"],
        "course": ["Math", "Math", "Physics"],
        "grade": [10, 11, 12],
    })

    report = check_data_quality(df)

    assert report["duplicate_student_courses"] == 1
    assert report["duplicate_rows"] == 0


def test_missing_required_column():
    """Détecter une colonne obligatoire absente."""
    df = pd.DataFrame({
        "student_id": ["A"],
        "course": ["Math"],
    })

    report = check_data_quality(df)

    assert report["missing_columns"] == ["grade"]


def test_empty_dataframe():
    """Gérer un DataFrame sans aucune ligne."""
    df = pd.DataFrame(
        columns=["student_id", "course", "grade"]
    )

    report = check_data_quality(df)

    assert report["total_rows"] == 0
    assert report["duplicate_rows"] == 0
    assert report["invalid_grades"] == 0


def test_original_data_unchanged():
    """Vérifier que les données ne sont pas modifiées."""
    df = pd.DataFrame({
        "student_id": ["A"],
        "course": ["Math"],
        "grade": [22],
    })

    original = df.copy(deep=True)

    check_data_quality(df)

    pd.testing.assert_frame_equal(df, original)

def test_invalid_age():
    """L'âge doit être entre 15 et 22."""
    df = pd.DataFrame({
        "age": [14, 15, 18, 22, 23, "abc", None]
    })

    report = check_data_quality(df)

    assert report["invalid_age"] == 3
    assert report["missing_values"]["age"] == 1


def test_student_multiple_courses():
    """Un identifiant ne doit pas appartenir à plusieurs cours."""
    df = pd.DataFrame({
        "student_id": ["A", "A", "B", "B"],
        "course": ["Math", "Physics", "Math", "Math"],
        "grade": [10, 12, 14, 15],
    })

    report = check_data_quality(df)

    # A appartient à deux cours différents
    assert report["students_in_multiple_courses"] == 1

    # B apparaît deux fois dans le même cours
    assert report["duplicate_student_courses"] == 1


def test_invalid_studytime():
    """Le temps d'étude ne doit pas être négatif."""
    df = pd.DataFrame({
        "studytime": [-2, 0, 3, "abc", None]
    })

    report = check_data_quality(df)

    assert report["invalid_studytime"] == 2
    assert report["missing_values"]["studytime"] == 1


def test_invalid_sex():
    """Le sexe doit être M ou F."""
    df = pd.DataFrame({
        "sex": ["M", "F", "X", "Male", None]
    })

    report = check_data_quality(df)

    assert report["invalid_sex"] == 2


def test_invalid_absences():
    """Les absences doivent être positives ou nulles."""
    df = pd.DataFrame({
        "absences": [-3, 0, 5, "unknown", None]
    })

    report = check_data_quality(df)

    assert report["invalid_absences"] == 2
    assert report["missing_values"]["absences"] == 1

def test_clean_dataframe():
    """Vérifie un DataFrame sans valeurs manquantes ni doublons."""

    df = pd.DataFrame({
        "student_id": ["MAT001", "MAT002", "MAT003"],
        "course": ["Mathematics", "Mathematics", "Mathematics"],
        "grade": [15, 12, 18],
    })

    report = check_data_quality(df)

    assert report["total_rows"] == 3
    assert report["total_missing_values"] == 0
    assert report["duplicate_rows"] == 0

def test_dirty_dataframe():
    """Vérifie un DataFrame avec une valeur manquante et un doublon."""

    df = pd.DataFrame({
        "student_id": ["MAT001", "MAT001", "MAT002"],
        "course": ["Mathematics", "Mathematics", "Mathematics"],
        "grade": [15, 15, None],
    })

    report = check_data_quality(df)

    assert report["total_rows"] == 3
    assert report["total_missing_values"] == 1
    assert report["duplicate_rows"] == 1
    
def test_dataframe_without_columns():
    """Vérifie un DataFrame sans lignes ni colonnes."""
    df = pd.DataFrame()

    report = check_data_quality(df)

    assert report["total_rows"] == 0
    assert report["no_columns"] is True
    assert report["missing_columns"] == [
        "student_id", "course", "grade"
    ]
    assert report["missing_values"] == {}
    assert report["duplicate_rows"] == 0