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
> Avant de passer au nettoyage je pourrait d'abord explorer mes données pour directement expliquer les colonnes et les comprendre. Mais j'ai decider de réaliser le nettoyage et la normalisation des données avant de passer à l'exploration.

### Nettoyage et normalisation des données

Dans le jeu de données, certaines données sont sous forme de texte (ex: sexe, type de douleur thoracique, etc.). Je les ai donc convertis en données numérques afin de faciliter leur normalisation et leur traitement.

On retrouve deux cas de conversion :

- La conversion lorsque on a que deux valeurs possibles (ex: sexe, maladie cardiaque, etc.). Dans ce cas, j'ai utilisé la méthode `replace` ou `map` de pandas pour remplacer les valeurs par des 0 et 1 de la maniere suivante :

```python
data['Sex'] = data['Sex'].map({'M' : 0, 'F' : 1})
data['Sex']
```

- la conversion lorsque on a plus de deux valeurs possibles (ex: type de douleur thoracique, etc.). Dans ce cas, j'ai opté pour la creation de colonne unique a chaque valeur. Ces colonnes ont été remplis avec que des 0 et des 1 pour montrer ou non la presence de la caractéristique étudiée Par exemple :

```python
CPL = ['TA', 'ATA', 'NAP', 'ASY'] # Liste des types de douleur thoracique possibles

for name in CPL: #Pour chaque valeur de la liste
    data[name + "_ChestPain"] = (data['ChestPainType'] == name).astype(int) # On crée une nouvelle colonne avec 1 si la valeur est présente, 0 sinon

    # Si la colonne existe déjà, on va juste remplir la colonne avec 0 ou 1 selon la valeur de la colonne ChestPainType

data = data.drop('ChestPainType', axis=1) # On supprime la colonne d'origine pour eviter la redondance
```

Avec ses techniques de nettoyage, j'ai pu transformer les colonnes de mon jeu de données en colonnes numériques. En mettant des valeurs entre 0 et 1 pour les colonnes qui contiennent des valeurs binaires (ex: sexe, maladie cardiaque, etc.) et en créant de nouvelles colonnes pour les colonnes qui contiennent plus de deux valeurs possibles (ex: type de douleur thoracique, etc.) j'ai pu normaliser mes données et les rendre plus faciles à traiter.

#### Les Cas spéciaux - Gestion des valeurs aberrantes

Dans certaines colonnes de mon jeu de données, j'ai remarqué qu'il y avait des "valeurs aberrantes". Dans mon cas, ce sont les données j'ai décidé de traiter ses données au cas par cas à l'aide de recherche et de documentation sur le sujet. Je vais vous presenter certains cas que j'ai rencontré et comment je les ai traité mais si vous voulez plus de détails, je vous invite à consulter le Jupyter Notebook de la partie 1&2 qui explique toute mes reflexions et choix.

Dans le cas :

- Du taux de Cholésterol : J'ai remarqué qu' On considere que le taux devient léthal à plus de 5,18 mmol/L.Mais il existe certain cas rare ou le taux de cholesterol peut attendre des données abérrantes sans pour autant que le patient soit mort. On parle alors hypercholestérolémie familiale. On n'est pas sur a 100% qu'un ou des patients ait cette maladie. Nous allons alors ignorer les valeures aberrantes dans la colonne "Cholesterol". Dans le cas ou le taux est egale à zéro on va juste le remplacer par la valeur médiane de la colonne.

## Exploration et visualisation des données

Pour explorer mes données j'ai principalement utilisé des graphiques permettant de visualiser les relations entre les différentes données mais également pour afficher de maniere plus visuelle les données de mon jeu de données.

Voici quelques graphiques que j'ai utilisé pour explorer mes données :

### Le nombre de patients du DataSet

![legende](https://raw.githubusercontent.com/OKINDACarlosEmmanuel/Data_project/main/Images/Nombre_de_patients.png)

### La correlation entre :

#### La maladie et la frequence cardiaque maximale

#### La maladie et le sexe

#### La maladie et l'age

### Matrice de correlation

Touts ces graphiques m'ont permis de mieux comprendre mes données et de voir les relations entre les différentes colonnes. J'ai pu ainsi identifier certaines colonnes qui pourraient être intéressantes à utiliser pour la prédiction de la maladie cardiaque et ainsi mieux m'orienter dans le choix de mes algorithmes de prédiction.

PS : Pour plus de détails sur les graphiques et les analyses que j'ai réalisé, je vous invite à consulter le Jupyter Notebook de la partie 3.0 qui explique toute mes reflexions et choix.

### Analyse de l'exploration des données

Pour affiner l'analyse de mes données, j'ai ajouté l'utilisation de statistiques descriptives permettant le calcul de métriques de base (moyenne, médiane, écart-type) pour comprendre la distribution de chaque variable numérique comme l'âge, la pression artérielle et le cholestérol.

PS: Voir partie 1&2

## Justifications des choix d'analyse et des techniques statistiques utilisées

### Choix des algorithmes de prédiction

Pour ce projet j'ai decider d'explorer plusieurs catégories d'algorithmes de prédictions afin de les comparer afin de ressortir celui qui est le plus adapté et perfomant pour notre jeu de données.

Comme catégories d'algorithmes de prédiction(et algorithmes) j'ai choisi :

- Le type "Regression" avec l'algorithme de Regression Logistique :

  - Ce type d'algorithme présente beaucoup d'avantages comme :

    - L'interprétation facile des résultats et des coefficients qui permettent de mieux comprendre l'impact des facteurs comme l'âge ou le cholésterol sur la probabilité de maladie cardiaque.
    - La rapidité d'exécution rapide permettant d'entrainer le modèle sur des ensembles de données un peu plus grands.

  - Mais néanmoins, il peut présenter des inconvénients comme :
    - La performance limitée sur les données linéaires quand les relations entre variables sont complexes comme dans le cas de notre jeu de données.
    - Le risque de supposition de linéarité entre les variables indépendantes et la variable dépendante, ce qui n'est pas toujours le cas dans la réalité et dans notre jeu de données.

- Le type "Classification" avec KNN:

  - Ce type d'algorithme présente des avantages comme :

    - Sa facilité à mettre en oeuvre et la réalisation de tests rapides.
    - La capacité à gérer des données non linéaires et complexes, ce qui est le cas de notre jeu de données.

  - Mais néanmoins, il peut présenter des inconvénients comme :
    - les performances limitées sur les ensembles de données plus grands, ce qui est le cas de notre jeu de données.
    - La sensibilité au bruit et aux valeurs aberrantes, ce qui peut affecter la précision du modèle.

- Le type "Apprentissage par ensemble" avec XGBoost et Random Forest :

  - Ce type d'algorithme présente des avantages comme :

    - La capacité à gérer des données non linéaires et complexes, ce qui est le cas de notre jeu de données.
    - La capacité à gérer les valeurs manquantes et les variables catégorielles, ce qui est le cas de notre jeu de données.
    - La resistance au surapprentissage, ce qui est le cas de notre jeu de données.

  - Mais néanmoins, il peut présenter des inconvénients comme :
    - La complexité de l'algorithme et la difficulté d'interprétation des résultats, ce qui n'est pas le cas de notre jeu de données.
    - Le temps d'entraînement plus long, ce qui n'est pas le cas de notre jeu de données.

### Complémentarité des algorithmes

#### Regression Logistique :

- Ce qu’elle fait : Elle regarde l'effet de chaque facteur (comme l'âge, le cholestérol, etc.) sur le risque de maladie cardiaque.

- Ce qu’elle apporte : Elle est facile à comprendre : on voit clairement quels facteurs augmentent ou diminuent le risque.

- En résumé : C’est le modèle qui aide le plus à expliquer pourquoi une personne est à risque.

#### KNN :

- Ce qu’il fait : Il compare chaque personne à ses voisines dans le dataset. Si les personnes proches ont une maladie, il suppose que cette personne en a aussi.

- Ce qu’il apporte : Il reconnaît les groupes de patients similaires, sans se baser sur des formules.

- En résumé : Il classe les gens en fonction de leur ressemblance avec d'autres cas connus

#### Random Forest :

- Ce qu’il fait : Il utilise plusieurs arbres de décision pour faire une prédiction en se basant sur un vote majoritaire.

- Ce qu’il apporte : Il gère bien les données complexes et peut montrer quels facteurs sont les plus importants.

- En résumé : C’est un modèle solide et fiable, qui donne de bonnes prédictions même avec des données variées.

#### XGBoost :

- Ce qu’il fait : Il construit des arbres très précis, chacun corrigeant les erreurs du précédent.

- Ce qu’il apporte : Il donne souvent les meilleures performances quand on veut vraiment optimiser les résultats.

- En résumé : C’est un modèle très puissant, surtout quand on veut le plus de précision possible.

### Techniques statistiques utilisées

Dans ce projet, j'ai employé plusieurs techniques statistiques pour analyser les données et construire des modèles de prédiction robustes:

#### 1. Prétraitement des données

- **Encodage one-hot**: Transformation des variables catégorielles à plusieurs niveaux (ChestPainType, RestingECG, ST_Slope) en plusieurs colonnes de variables binaires (0/1) pour permettre leur utilisation dans les algorithmes d'apprentissage.
- **Normalisation des données**: Application de StandardScaler pour standardiser les variables numériques afin qu'elles aient toutes une moyenne de 0 et un écart-type de 1, garantissant ainsi que toutes les caractéristiques contribuent équitablement aux modèles.
- **Imputation des valeurs manquantes**: Remplacement des valeurs de cholestérol nulles par la médiane des valeurs non nulles pour éviter les biais dans l'analyse.

#### 2. Techniques d'évaluation des modèles

- **Matrice de confusion**: Analyse détaillée des vrais positifs, faux positifs, vrais négatifs et faux négatifs pour évaluer la qualité des prédictions.
- **Validation croisée**: Division des données en ensembles d'entraînement (80%) et de test (20%) pour évaluer la capacité de généralisation des modèles.
- **Métriques de performance**: Utilisation de multiples indicateurs statistiques pour une évaluation complète:
  - Précision
  - Recall/Sensibilité
  - Score F1
  - Exactitude

#### 3. Optimisation des hyperparamètres

- **Méthode Elbow** pour KNN: Analyse de l'évolution de l'erreur en fonction du nombre de voisins (k) pour déterminer la valeur optimale.
- **Grid Search** pour Random Forest: Recherche systématique des meilleurs paramètres (n_estimators=138, max_depth=18) parmi un ensemble de valeurs possibles.
- **Analyse de courbes d'apprentissage**: Étude de l'évolution des performances en fonction de la taille des données d'entraînement pour détecter d'éventuels problèmes de sur-apprentissage ou sous-apprentissage.

Ces techniques statistiques rigoureuses ont permis non seulement de construire des modèles performants, mais aussi de comprendre en profondeur les facteurs déterminants pour la prédiction des maladies cardiaques et d'assurer la fiabilité des résultats dans un contexte médical où la précision est cruciale.

## Evaluation des modeles

Pour evaluer nos modèles, j'ai utilisé certains indacateurs de performance cités plus haut et un système de notes sur 5 pour chaque modele. Voici les indicateurs que j'ai utilisé :

- La précision : C’est le pourcentage de cas prévus comme malades qui sont vraiment malades.

- Le rappel : C’est le pourcentage de bonnes prédictions faites par le modèle, sur l’ensemble des données.

- L'Exactitude : C’est la capacité du modèle à repérer tous les cas positifs (les vrais malades).

- Le F1 Score : C’est une moyenne entre la précision et le rappel, pour avoir un compromis entre les deux.

Dans tous ses cas, plus le pourcentage est élevé, mieux c'est. Un bon modèle aura au minimum 75% dans chacun des indicateurs.

A ces indicateurs j'ai jouté 3 Moyens d'évaluer le modèle :

- La robustesse du modele: s’il arrive à faire de bonnes prédictions même si certaines données médicales sont incomplètes ou un peu incorrectes, comme un âge mal saisi ou une tension anormale

- La complexité du modèle et sa rapidité d'exécution: Un modèle complexe comme XGBoost peut mieux détecter les cas de maladie cardiaque, mais il mettra plus de temps à s'entraîner que des modèles simples comme la régression logistique.

- L'interprétabilité du modèle et son explicabilité : Un modèle interprétable te permet de comprendre facilement pourquoi il prédit qu’un patient a un risque, par exemple en montrant que le cholestérol élevé ou la fréquence cardiaque ont influencé la décision

### Strategie de Validation croisée

Pour entraîner et évaluer les performances des modèles prédictifs sur les données de maladies cardiaques, j'ai choisi une répartition classique de 80 % pour l'entraînement et 20 % pour le test.

Ce choix permet de garantir un bon équilibre :

D’un côté, 80 % des données servent à apprendre les relations entre les facteurs médicaux (comme la tension, l’âge, le cholestérol) et la présence d’une maladie cardiaque.

De l’autre, 20 % des données sont mises de côté pour vérifier si le modèle est capable de généraliser correctement sur de nouveaux cas qu’il n’a jamais vus.

Dans le contexte de la santé, cette séparation est importante car elle permet de s'assurer que le modèle n'est pas simplement bon à "mémoriser" les patients du jeu d’entraînement, mais bien à prédire correctement sur des cas réels et inconnus, ce qui est essentiel pour une application fiable.

### Protocole détaillé d'évaluation

Pour garantir une évaluation rigoureuse et reproductible de mes modèles prédictifs, j'ai mis en place un protocole d'évaluation structuré en plusieurs étapes :

1. **Préparation et division des données**

   - Division du jeu de données en 80% pour l'entraînement et 20% pour le test avec `train_test_split` et un `random_state=42`(si nécessaire) pour assurer la reproductibilité.
   - Application du `StandardScaler` uniquement sur les données d'entraînement, puis utilisation des mêmes paramètres pour normaliser les données de test.

2. **Optimisation des hyperparamètres**

   - Pour KNN : application de la méthode Elbow pour déterminer le nombre optimal de voisins (k=46)
   - Pour Random Forest : utilisation de `GridSearchCV` pour identifier les meilleurs paramètres (`n_estimators=138`, `max_depth=18`)
   - Pour la Régression Logistique : optimisation du paramètre de régularisation C
   - Pour XGBoost : ajustement du taux d'apprentissage et de la profondeur des arbres

3. **Métriques d'évaluation**

   - Calcul systématique de le Précision, l'Exactitude, le Recall et le F1-Score pour chaque modèle :
     - Précision
     - Exactitude
     - Recall
     - F1-Score

4. **Validation sur cas réels**

   - Test de chaque modèle sur un ensemble de 5 patients tests identiques pour tous les modèles
   - Ces patients ont été choisis pour représenter différents profils : certains clairement malades, d'autres clairement sains, et certains cas limite
   - Analyse des probabilités fournies par chaque modèle, au-delà de la simple classification binaire

5. **Évaluation de la robustesse**

   - Test de la sensibilité des modèles à de légères variations dans les données d'entrée
   - Observation de la stabilité des prédictions face à des données légèrement modifiées
   - Analyse de la capacité du modèle à maintenir ses performances sur différents sous-ensembles de données

6. **Analyse de l'interprétabilité**
   - Pour la Régression Logistique : examen des coefficients pour identifier les facteurs les plus influents
   - Pour Random Forest et XGBoost : analyse de l'importance des caractéristiques
   - Évaluation qualitative de la facilité avec laquelle les résultats peuvent être expliqués à un professionnel de santé

Ce protocole rigoureux m'a permis de comparer objectivement les différents modèles et d'identifier lequel offre le meilleur compromis entre performance, robustesse et interprétabilité dans le contexte spécifique de la prédiction des maladies cardiaques.

### Tableau Comparatif des modèles

Pour cette partie, on va comparer à l'aide d'un tableau les différents modèles que j'ai utilisé pour prédire la maladie cardiaque. On va comparer les modèles sur la base de 4 indicateurs de performance et 3 moyens d'évaluer le modèle.
| Modèle | Précision (%) | Exactitude (%) | Recall (%) | F1-Score (%) | Robustesse | Complexité | Interprétabilité | Note sur 5 |
|----------------------|---------------|----------------|------------|--------------|-----------|-----------------------------|------------|
| Régression Logistique | 86.0 | 87.0 | 87.5 | 86.5 | Moyenne | Faible | 3.75 |
| KNN | 87.0 | 88.0 | 88.5 | 88.0 | Moyenne | Moyenne | 4. 25 |
| Random Forest | 88.0 | 89.0 | 88.5 | 88.0 |Bonne | Bonne | 4.75 |
| XGBoost | 89.0 | 90.0 | 89.0 | 89.5 | Bonne | Moyenne | 4.5 |

#### Modèle le plus performant

Bien que XGBoost présente des métriques de performance légèrement supérieures (90% d'exactitude contre 89% pour Random Forest), le Random Forest obtient une meilleure note globale (4,75/5 contre 4,5/5 pour XGBoost) pour plusieurs raisons importantes:

- Random Forest offre une performance presque identique à XGBoost mais avec une complexité moindre.

  - Random Forest nécessite significativement moins de ressources et de temps d'entraînement

- Random Forest est plus facile à interpréter et à expliquer, ce qui est crucial dans un contexte médical.
- XGBoost est "très coûteux énergétiquement" et "assez lent pour l'exécution et l'entraînement" dans votre environnement tant dis que Random Forest est "très rapide".

En résumé, bien que XGBoost soit légèrement plus performant, Random Forest est le meilleur choix en raison de sa robustesse, de sa rapidité et de sa facilité d'interprétation. Il est donc le modèle le plus adapté pour prédire la maladie cardiaque dans ce projet.

### Conclusions et perspectives

L'analyse des différents modèles et de leurs résultats permet de tirer plusieurs conclusions originales :

1. **La complémentarité des approches** : La combinaison de plusieurs modèles offre une perspective plus complète qu'un modèle unique, notamment en réduisant le risque de faux négatifs dangereux.

2. **L'importance relative des facteurs** : L'analyse des coefficients de la régression logistique et de l'importance des caractéristiques de Random Forest révèle que les facteurs les plus déterminants pour prédire une maladie cardiaque sont, par ordre d'importance :

   - La dépression ST (Oldpeak)
   - La présence de douleurs thoraciques de type ASY (asymptomatiques)
   - L'âge

3. **La mise en perspective clinique** : Ces résultats s'alignent avec la littérature médicale qui souligne que les douleurs thoraciques asymptomatiques sont souvent les plus dangereuses car elles peuvent masquer une pathologie grave sans symptômes évidents.

4. **Limites et améliorations possibles** : Malgré de bons résultats, le modèle pourrait bénéficier de données supplémentaires comme l'historique familial de maladies cardiaques ou les habitudes de vie (tabagisme, activité physique) qui ne figurent pas dans le jeu de données actuel.

Ces conclusions démontrent l'utilité potentielle de notre application comme outil d'aide à la décision pour les professionnels de santé, tout en soulignant l'importance de l'interprétation humaine des résultats.
