# EduAnalytics

Analyse des résultats étudiants : import CSV, qualité des données, moyennes, classement, statistiques de distribution, rapport HTML.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

Lancer les tests :

```bash
pytest
```

Analyser la qualité du jeu d'exemple :

```bash
python src/data_quality.py
```

Générer un rapport HTML :

```bash
PYTHONPATH=src python -c "from html_report import generate_html_report; open('rapport.html', 'w', encoding='utf-8').write(generate_html_report('data/sample/students.csv'))"
```

## Fonctionnalités

- csv-import : lecture d'un CSV en DataFrame (samrous6213 - Sara Amrous )
- data-quality : valeurs manquantes et doublons (Yassine-Baroudi)
- averages : moyennes par étudiant et par matière, arrondies à 2 décimales (badr-abba)
- ranking : classement des étudiants par moyenne, ex aequo gérés (RedaAgouzoul)
- distribution-stats : moyenne, médiane, écart-type, quartiles (Simo069)
- html-report : génération d'un rapport HTML (Oussama-Inchallah)
<!-- une ligne par fonctionnalité : nom, auteur -->

## Données

Les jeux de données complets ne sont pas versionnés. Un échantillon destiné aux tests est disponible dans `data/sample/students.csv`.

Le fichier CSV attendu contient au minimum les colonnes `student_id`, `course` et `grade`.
