"""Tests pour src/csv_import.py."""
from pathlib import Path
import pytest
import pandas as pd

from csv_import import load_students_csv

# Chemin vers le fichier d'exemple
SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "students.csv"


def test_load_sample_csv_returns_dataframe():
    """Vérifie que le fichier d'exemple est bien lu et contient les bonnes colonnes."""
    df = load_students_csv(SAMPLE)
    
    assert isinstance(df, pd.DataFrame)
    # On vérifie nos nouvelles colonnes
    assert "student_id" in df.columns
    assert "course" in df.columns
    assert "grade" in df.columns
    assert len(df) > 0


def test_missing_file_raises():
    """Vérifie qu'une erreur est levée si le fichier n'existe pas."""
    with pytest.raises(FileNotFoundError):
        load_students_csv("chemin/vers/un/fichier/inexistant.csv")


def test_empty_csv_raises(tmp_path):
    """Vérifie qu'une erreur est levée si le CSV est vide (en-tête seulement)."""
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("student_id,course,grade\n")
    
    with pytest.raises(ValueError):
        load_students_csv(empty_file)

def test_missing_expected_column_raises(tmp_path):
    """Vérifie qu'une erreur est levée si une colonne attendue manque."""
    bad_file = tmp_path / "bad.csv"
    # On crée un CSV auquel il manque la colonne 'grade'
    bad_file.write_text("student_id,course\nMAT001,Mathematics\n")
    
    with pytest.raises(ValueError, match="Colonnes manquantes"):
        load_students_csv(bad_file)