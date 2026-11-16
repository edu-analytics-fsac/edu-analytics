"""Tests pour src/distribution_stats.py."""
from pathlib import Path
import pandas as pd
import pytest

from distribution_stats import distribution_stats

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "students.csv"


def test_distribution_stats_known_values():
    """Cas simple avec des valeurs connues."""
    df = pd.DataFrame({"note": [10.0, 12.0, 14.0, 16.0, 18.0]})
    stats = distribution_stats(df, column="note")

    assert stats["count"] == 5
    assert stats["mean"] == 14.0
    assert stats["median"] == 14.0
    assert stats["q1"] == 12.0
    assert stats["q3"] == 16.0
    assert stats["min"] == 10.0
    assert stats["max"] == 18.0
    assert stats["std"] == pytest.approx(3.162277, rel=1e-3)


def test_distribution_stats_constant_values():
    """Cas de notes toutes identiques (écart-type nul)."""
    df = pd.DataFrame({"grade": [15.0, 15.0, 15.0, 15.0]})
    stats = distribution_stats(df)

    assert stats["count"] == 4
    assert stats["mean"] == 15.0
    assert stats["median"] == 15.0
    assert stats["std"] == 0.0
    assert stats["q1"] == 15.0
    assert stats["q3"] == 15.0
    assert stats["min"] == 15.0
    assert stats["max"] == 15.0


def test_distribution_stats_series_input():
    """Test avec une pandas Series directement."""
    s = pd.Series([10.0, 20.0])
    stats = distribution_stats(s)

    assert stats["count"] == 2
    assert stats["mean"] == 15.0
    assert stats["median"] == 15.0
    assert stats["min"] == 10.0
    assert stats["max"] == 20.0


def test_distribution_stats_real_sample():
    """Test sur l'échantillon réel data/sample/students.csv."""
    df = pd.read_csv(SAMPLE)
    stats = distribution_stats(df, column="grade")

    assert stats["count"] == len(df)
    assert 0 <= stats["min"] <= stats["q1"] <= stats["median"] <= stats["q3"] <= stats["max"] <= 20
    assert stats["std"] > 0


def test_distribution_stats_empty_raises():
    """Vérifie qu'un jeu de données vide lève une ValueError."""
    with pytest.raises(ValueError):
        distribution_stats(pd.DataFrame({"grade": []}))


def test_distribution_stats_invalid_type_raises():
    """Vérifie qu'un type inattendu lève une TypeError."""
    with pytest.raises(TypeError):
        distribution_stats([10, 12, 14])


def test_distribution_stats_missing_column_raises():
    """Vérifie qu'une colonne absente lève une ValueError."""
    df = pd.DataFrame({"autre_colonne": [10, 12]})
    with pytest.raises(ValueError):
        distribution_stats(df, column="inconnue")
