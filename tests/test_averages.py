"""Tests pour src/averages.py."""
from pathlib import Path

import pandas as pd
import pytest

from averages import DECIMALS, course_averages, student_averages
from csv_import import load_students_csv

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "students.csv"

# Petit jeu contrôlé : les moyennes attendues se vérifient à la main.
DF = pd.DataFrame({
    "student_id": ["A", "A", "B", "B"],
    "course": ["Math", "Physics", "Math", "Physics"],
    "grade": [10, 20, 12, 14],
})


# --- Tests sur le vrai dataset (data/sample/students.csv) ---

def test_real_dataset_course_averages():
    df = load_students_csv(SAMPLE)
    result = course_averages(df)

    valid = df[pd.to_numeric(df["grade"], errors="coerce").between(0, 20)]
    expected = valid.groupby(valid["course"].str.strip())["grade"].mean().round(DECIMALS)

    assert not result.empty
    assert result.between(0, 20).all()
    pd.testing.assert_series_equal(
        result, expected, check_names=False, check_dtype=False, check_index_type=False
    )


def test_real_dataset_student_averages():
    df = load_students_csv(SAMPLE)
    result = student_averages(df)

    assert not result.empty
    assert result.index.is_unique
    assert result.dropna().between(0, 20).all()


# --- Tests sur des données contrôlées (cas limites impossibles à forcer sur le vrai fichier) ---

def test_student_averages():
    assert student_averages(DF).to_dict() == {"A": 15.0, "B": 13.0}


def test_course_averages():
    assert course_averages(DF).to_dict() == {"Math": 11.0, "Physics": 17.0}


def test_non_numeric_grades_are_ignored():
    df = pd.DataFrame({
        "student_id": ["A", "A", "A", "A"],
        "course": ["Math"] * 4,
        "grade": [10, "abc", None, 20],
    })
    assert student_averages(df)["A"] == 15.0


def test_empty_dataframe():
    df = pd.DataFrame(columns=["student_id", "course", "grade"])
    assert student_averages(df).empty
    assert course_averages(df).empty


def test_missing_column_raises():
    df = pd.DataFrame({"student_id": ["A"], "course": ["Math"]})
    with pytest.raises(ValueError, match="Colonnes manquantes"):
        student_averages(df)


def test_not_a_dataframe_raises():
    with pytest.raises(TypeError):
        course_averages([1, 2, 3])


def test_original_data_unchanged():
    df = DF.copy(deep=True)
    student_averages(df)
    pd.testing.assert_frame_equal(df, DF)


def test_averages_are_rounded_to_two_decimals():
    df = pd.DataFrame({
        "student_id": ["A", "A", "A"],
        "course": ["Math"] * 3,
        "grade": [10, 11, 11],
    })
    assert student_averages(df)["A"] == 10.67


def test_outliers_and_spaces_are_ignored():
    df = pd.DataFrame({
        "student_id": ["A", "A", "B"],
        "course": ["Math", "Math ", "Math"],
        "grade": [10, 99, -5],
    })
    assert course_averages(df).to_dict() == {"Math": 10.0}
    assert student_averages(df).dropna().to_dict() == {"A": 10.0}