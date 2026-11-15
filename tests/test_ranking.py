"""Tests pour src/ranking.py."""
from pathlib import Path

import pandas as pd
import pytest

from csv_import import load_students_csv
from ranking import rank_students, ranking_table

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample" / "students.csv"


# --- Tests sur le vrai dataset (data/sample/students.csv) ---

def test_real_dataset_ranking():
    df = load_students_csv(SAMPLE)
    averages = df.groupby("student_id")["grade"].mean()
    ranks = rank_students(averages)

    assert len(ranks) == len(averages)
    assert ranks.min() == 1
    assert ranks.max() <= len(averages)
    assert ranks[averages.idxmax()] == 1

    # Plus la moyenne est haute, plus le rang est petit (ou égal en cas d'ex aequo).
    valid = averages.dropna()
    ordered = ranks[valid.sort_values(ascending=False).index]
    assert ordered.is_monotonic_increasing


def test_real_dataset_ranking_table():
    df = load_students_csv(SAMPLE)
    averages = df.groupby("student_id")["grade"].mean()
    table = ranking_table(averages)

    assert list(table.columns) == ["student_id", "average", "rank"]
    assert table["rank"].is_monotonic_increasing
    assert table.loc[0, "rank"] == 1


# --- Tests sur des données contrôlées ---

def test_basic_ranking():
    result = rank_students(pd.Series({"A": 15.0, "B": 12.0, "C": 18.0}))
    assert result.to_dict() == {"A": 2, "B": 3, "C": 1}


def test_ties_share_the_same_rank():
    result = rank_students(pd.Series({"A": 15.0, "B": 15.0, "C": 10.0}))
    assert result.to_dict() == {"A": 1, "B": 1, "C": 3}


def test_missing_average_is_not_ranked():
    result = rank_students(pd.Series({"A": 15.0, "B": None, "C": 10.0}))
    assert result["A"] == 1
    assert result["C"] == 2
    assert pd.isna(result["B"])


def test_empty_series():
    assert rank_students(pd.Series(dtype=float)).empty


def test_not_a_series_raises():
    with pytest.raises(TypeError):
        rank_students([15, 12, 18])


def test_original_series_unchanged():
    s = pd.Series({"A": 15.0, "B": 12.0})
    original = s.copy(deep=True)
    rank_students(s)
    pd.testing.assert_series_equal(s, original)


def test_ranking_table_is_sorted_and_drops_missing():
    table = ranking_table(pd.Series({"A": 10.0, "B": 18.0, "C": None, "D": 18.0}))
    assert table["student_id"].tolist() == ["B", "D", "A"]
    assert table["rank"].tolist() == [1, 1, 3]

def test_single_student():
    result = rank_students(pd.Series({"A": 14.0}))
    assert result.to_dict() == {"A": 1}