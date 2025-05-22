import pandas as pd

# Charger les données existantes
try:
    resultats = pd.read_csv(r"c:\Users\User\OneDrive - Institut Catholique de Lille\Bureau\L3 SDN\S2\Projet Data\Data_project\resultat.csv")
except FileNotFoundError:
    # Si le fichier n'existe pas, recréer les données comme dans resultat.py
    resultats = pd.DataFrame(columns=["Nom", "Precision", "Accuracy", "Recall", "F1-Score", "Robustesse", "Complexite & Interpretabilité", "Note sur 5"])
    
    resultats.loc[0] = ["KNN", 87.0, 88.0, 88.5, 88.0, 2, 1, 3.75]
    resultats.loc[1] = ["Regression Logistique", 86.0, 87.0, 87.5, 86.5, 2, 2, 4.0]
    resultats.loc[2] = ["Random Forest", 88.0, 89.0, 88.5, 88.0, 3, 3, 4.75]
    resultats.loc[3] = ["XGBoost", 89.0, 90.0, 89.0, 89.5, 3, 2, 4.5]

# Créer le nouveau format
nouveau_format = []

# Pour chaque modèle, ajouter une ligne pour chaque critère
for _, row in resultats.iterrows():
    modele = row['Nom']
    
    # Ajouter chaque critère avec les bonnes échelles
    nouveau_format.append({'modèle': modele, 'critère': 'Precision', 'valeur': row['Precision']})
    nouveau_format.append({'modèle': modele, 'critère': 'Accuracy', 'valeur': row['Accuracy']})
    nouveau_format.append({'modèle': modele, 'critère': 'Recall', 'valeur': row['Recall']})
    nouveau_format.append({'modèle': modele, 'critère': 'F1-Score', 'valeur': row['F1-Score']})
    
    # Convertir Robustesse de 3 à 100
    robustesse_sur_100 = (row['Robustesse'] / 3) * 100
    nouveau_format.append({'modèle': modele, 'critère': 'Robustesse', 'valeur': robustesse_sur_100})
    
    # Convertir Complexité & Interprétabilité de 3 à 100
    complexite_sur_100 = (row['Complexite & Interpretabilité'] / 3) * 100
    nouveau_format.append({'modèle': modele, 'critère': 'Complexite & Interpretabilité', 'valeur': complexite_sur_100})
    
    # Convertir Note sur 5 à Note sur 100
    note_sur_100 = (row['Note sur 5'] / 5) * 100
    nouveau_format.append({'modèle': modele, 'critère': 'Note sur 100', 'valeur': note_sur_100})

# Créer le nouveau DataFrame et sauvegarder en CSV
nouveau_df = pd.DataFrame(nouveau_format)
nouveau_df.to_csv(r"c:\Users\User\OneDrive - Institut Catholique de Lille\Bureau\L3 SDN\S2\Projet Data\Data_project\resultats_long_format.csv", index=False)

print("Nouveau fichier CSV créé avec succès au format 'modèle - critère - valeur' avec les échelles converties!")