
import pandas as pd

# Charger les deux fichiers
math_df = pd.read_csv("data/raw/student-mat.csv", sep=";")
portuguese_df = pd.read_csv("data/raw/student-por.csv", sep=";")

# Afficher les informations générales
print("=== MATHEMATICS ===")
print("Dimensions :", math_df.shape)
print("Colonnes :", math_df.columns.tolist())
print(math_df.head())

print("\n=== PORTUGUESE ===")
print("Dimensions :", portuguese_df.shape)
print("Colonnes :", portuguese_df.columns.tolist())
print(portuguese_df.head())

# Vérifier les valeurs manquantes
print("\nValeurs manquantes en mathématiques :")
print(math_df.isnull().sum().sum())

print("\nValeurs manquantes en portugais :")
print(portuguese_df.isnull().sum().sum())
