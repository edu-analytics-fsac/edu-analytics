"""Tests de génération du rapport HTML."""

from pathlib import Path

import pandas as pd

from html_report import generate_html_report


SAMPLE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "sample"
    / "students.csv"
)


def test_report_contains_expected_sections_and_top_ten():
    html = generate_html_report(SAMPLE)

    assert "<html lang=\"fr\">" in html
    assert "Qualité des données" in html
    assert "Moyennes par matière" in html
    assert "Classement - top 10" in html
    assert "Distribution des notes valides" in html
    ranking_section = html.split(
        "<h2>Classement - top 10</h2>", maxsplit=1
    )[1].split("</section>", maxsplit=1)[0]
    assert ranking_section.count("<tr>") == 10


def test_invalid_grades_are_excluded_from_report_statistics(tmp_path):
    csv_path = tmp_path / "students.csv"
    pd.DataFrame({
        "student_id": ["A", "B", "C"],
        "course": ["Math", "Math", "Math"],
        "grade": [10, 25, "inconnu"],
    }).to_csv(csv_path, index=False)

    html = generate_html_report(csv_path)

    assert "Notes invalides</th><td>2" in html
    assert "10.00" in html
    assert "17.50" not in html


def test_dynamic_html_values_are_escaped(tmp_path):
    csv_path = tmp_path / "students & test.csv"
    pd.DataFrame({
        "student_id": ["<script>alert('x')</script>"],
        "course": ['Math & "Sciences"'],
        "grade": [15],
    }).to_csv(csv_path, index=False)

    html = generate_html_report(csv_path)

    assert "<script>" not in html
    assert 'Math & "Sciences"' not in html
    assert 'Math &amp; "Sciences"' in html
    assert "alert('x')" in html
    assert "&lt;script&gt;" in html
    assert "students &amp; test.csv" in html