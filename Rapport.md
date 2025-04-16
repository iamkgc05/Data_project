# Rapport du projet de Data IA par OKINDA Carlos Emmanuel

## Plan du Rapport

1. Introduction + Présentation des données et du Nettoyage
2. Analyse et exploration des données + Visualisation
3. Presentation des modeles prédictifs
   - Nom et Justification du choix du modele
   - Presentation du modele et des resultats obtenus
   - Evaluation du modèle
4. Comparaison générale des modeles
5. Conclusion

## Introduction

Le but de ce projet est de prédire si un patient est susceptible d'avoir une crise cardiaque ou non.

## Présentation des données et du Nettoyage

### Présentation des données

Pour ce projet, j'ai utiliser un jeu de données nommées "heart_dicease.csv" qui contient des informations sur les patients et si ils ont eu ou non une crise cardiaque.

Les colonnes de notre jeu de données sont les suivantes :

- Age : l'âge de l'individu
- Sex : Le sexe du patient (M: Homme, F: Femme)
- ChestPainType : le type de douleur thoracique (TA: Angine typique, ATA: Angine atypique, ASY: Asymptomatique, NAP: Non angine)
- RestingBP : La pression sanguine au repos (mm Hg)
- Cholesterol : Le taux de cholestérol (mg/dl)
- FastingBS : Le taux de sucre dans le sang à jeun (0: Normal, 1: si supérieur à 120 mg/dl)
- RestingECG : L'électrocardiogramme au repos (Normal: Normal, ST: Anomalie de l'élévation du segment ST, LVH: Hypertrophie ventriculaire gauche)
  -MaxHR : Le rythme cardiaque maximum (bpm)
- ExerciceAngina : Angine induite par l'exercice (Y: Oui, N: Non)
- Oldpeak : Dépression ST induite par l'exercice par rapport au repos (en valeur numérique)
- ST_Slope : La pente du segment ST de l'exercice (Up: Montant, Flat: Plat, Down: Descendant)
- HeartDisease : Maladie cardiaque (1: Oui, 0: Non)

> [!NOTE]
>
> Voici mes notes

Avant de passer au nettoyage je pourrait d'abord explorer mes données pour directement expliquer les colonnes et les comprendre. Mais j'ai decider de réaliser un nettoyage avant de passer à l'exploration.
