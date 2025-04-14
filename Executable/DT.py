import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv(r'C:\Users\User\OneDrive - Institut Catholique de Lille\Bureau\L3 SDN\S2\Projet Data\Data_project\heart_disease_by_ceo.csv', index_col=0)
test_size = 0.2
random_state = 42

def realiser_dt(patient):
    # Séparer les caractéristiques et la cible
    x = data.drop('HeartDisease', axis=1)
    y = data['HeartDisease']

    # Diviser les données en ensembles d'entraînement et de test
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)  

    # Normaliser les données
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    patient_scaled = scaler.transform(patient)

    # Créer le modèle Decision Tree
    dt = DecisionTreeClassifier(max_depth=5, random_state=random_state)
    dt.fit(x_train, y_train)

    # Obtenir les probabilités de prédiction
    probabilities = dt.predict_proba(patient_scaled)[0]
    
    # Calculer les pourcentages
    prob_non_malade = probabilities[0] * 100
    prob_malade = probabilities[1] * 100
    
    # Afficher les pourcentages
    print(f"DT | Patient : {prob_malade:.2f}% malade - {prob_non_malade:.2f}% non-malade")

    return prob_malade, prob_non_malade

if __name__ == "__main__":
    # Exemple de patient
    patient = [[40,0,140,289,0,172,0,0.0,0,1,0,0,1,0,0,1,0,0]] 
    realiser_dt(patient)