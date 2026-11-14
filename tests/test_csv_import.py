"""Tests pour src/csv_import.py."""
from pathlib import Path
import pytest
import pandas as pd

from csv_import import load_students_csv

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "students.csv"


def test_load_sample_csv_returns_dataframe():
    df = load_students_csv(SAMPLE)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["student", "course", "grade"]
    assert len(df) > 0


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_students_csv("chemin/inexistant.csv")


def test_empty_csv_raises(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text("student,course,grade\n")
    with pytest.raises(ValueError):
        load_students_csv(empty)
        