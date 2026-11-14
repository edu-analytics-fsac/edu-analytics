
import pandas as pd
from pathlib import Path

# Dossiers
RAW_DIR = Path("data/raw")
SAMPLE_DIR = Path("data/sample")
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

# Charger les données originales
math_df = pd.read_csv(RAW_DIR / "student-mat.csv", sep=";")
portuguese_df = pd.read_csv(RAW_DIR / "student-por.csv", sep=";")

# Construire un échantillon de 100 étudiants par matière
math_sample = math_df.sample(n=100, random_state=42)
portuguese_sample = portuguese_df.sample(n=100, random_state=42)

# Sélectionner les colonnes utiles
columns = ["school", "sex", "age", "studytime", "absences", "G3"]

math_sample = math_sample[columns].copy()
portuguese_sample = portuguese_sample[columns].copy()

# Ajouter les identifiants techniques et les matières
math_sample.insert(
    0, "student_id",
    [f"MAT{i:03d}" for i in range(1, 101)]
)
math_sample.insert(1, "course", "Mathematics")

portuguese_sample.insert(
    0, "student_id",
    [f"POR{i:03d}" for i in range(1, 101)]
)
portuguese_sample.insert(1, "course", "Portuguese")

# Renommer G3 en grade
math_sample.rename(columns={"G3": "grade"}, inplace=True)
portuguese_sample.rename(columns={"G3": "grade"}, inplace=True)

# Fusionner les deux échantillons
students = pd.concat(
    [math_sample, portuguese_sample],
    ignore_index=True
)

# Exporter le résultat
output_path = SAMPLE_DIR / "students.csv"
students.to_csv(output_path, index=False)

print("Échantillon créé avec succès !")
print("Nombre de lignes :", len(students))
print("Nombre de colonnes :", len(students.columns))
print("Taille :", f"{output_path.stat().st_size / 1024:.2f} KB")
print("\nAperçu :")
print(students.head(10))
print("\nRépartition par matière :")
print(students["course"].value_counts())
