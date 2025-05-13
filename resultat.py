import pandas as pd

# Création du dataframe pour stocker les résultats
resultats = pd.DataFrame(columns=["Nom", "Precision", "Accuracy", "Recall", "F1-Score", "Robustesse", "Complexite & Interpretabilité", "Note sur 5"])

# Ajout des données pour chaque modèle en se basant sur les informations de vos notebooks
# KNN (depuis Partie3_1KNN.ipynb)
resultats.loc[0] = ["KNN", 87.0, 88.0, 88.5, 88.0,2,1,3.75]

# Logistic Regression (depuis Partie3_2LG.ipynb)
resultats.loc[1] = ["Regression Logistique", 86.0, 87.0, 87.5, 86.5, 2, 2, 4.0]

# Random Forest (depuis Partie3_3.ipynb)
resultats.loc[2] = ["Random Forest", 88.0, 89.0, 88.5, 88.0,3,3,4.75 ]

# XGBoost (depuis Partie3_4.ipynb)
resultats.loc[3] = ["XGBoost", 89.0, 90.0, 89.0, 89.5, 3,2,4.5]

# Enregistrement dans le fichier CSV

resultats.to_csv("resultat.csv", index=False)

print("Fichier CSV créé avec succès !")