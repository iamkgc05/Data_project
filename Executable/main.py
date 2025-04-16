import sys
import os
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, 
                             QGroupBox, QScrollArea, QGridLayout, QMessageBox,
                             QProgressBar, QSlider, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap

# Chemin du fichier de données
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'heart_disease_by_ceo.csv')

# Importation des modèles (les chemins doivent être correctement configurés)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from KNN import realiser_knn
    knn_available = True
except ImportError:
    knn_available = False
    print("Module KNN non disponible")

try:
    from RF import realiser_rf
    rf_available = True
except ImportError:
    rf_available = False
    print("Module RF non disponible")

try:
    from LG import realiser_lg
    lg_available = True
except ImportError:
    lg_available = False
    print("Module LG non disponible")

try:
    from XGB import realiser_xgb
    xgb_available = True
except ImportError:
    xgb_available = False
    print("Module XGB non disponible")

class CardioPredictor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prédicteur de Maladie Cardiaque")
        self.setMinimumSize(800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Titre
        title_label = QLabel("Prédicteur de Maladie Cardiaque")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Conteneur scrollable pour les entrées
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        scroll_area.setWidget(input_widget)
        main_layout.addWidget(scroll_area)
        
        # Variables à collecter
        self.user_inputs = {}
        
        # Groupe pour les informations démographiques
        demo_group = QGroupBox("Informations démographiques")
        demo_layout = QGridLayout()
        demo_group.setLayout(demo_layout)
        
        # Âge
        demo_layout.addWidget(QLabel("Âge:"), 0, 0)
        self.age_input = QSpinBox()
        self.age_input.setRange(20, 100)
        self.age_input.setValue(40)
        demo_layout.addWidget(self.age_input, 0, 1)
        
        # Sexe
        demo_layout.addWidget(QLabel("Sexe:"), 1, 0)
        self.sex_layout = QHBoxLayout()
        self.male_checkbox = QCheckBox("Homme")
        self.female_checkbox = QCheckBox("Femme")
        self.male_checkbox.setChecked(True)
        self.sex_layout.addWidget(self.male_checkbox)
        self.sex_layout.addWidget(self.female_checkbox)
        demo_layout.addLayout(self.sex_layout, 1, 1)
        
        # Connecter les checkboxes pour qu'ils soient mutuellement exclusifs
        self.male_checkbox.toggled.connect(lambda checked: self.female_checkbox.setChecked(not checked))
        self.female_checkbox.toggled.connect(lambda checked: self.male_checkbox.setChecked(not checked))
        
        input_layout.addWidget(demo_group)
        
        # Groupe pour les données médicales
        medical_group = QGroupBox("Données médicales")
        medical_layout = QGridLayout()
        medical_group.setLayout(medical_layout)
        
        # RestingBP
        medical_layout.addWidget(QLabel("Pression artérielle au repos (mm Hg):"), 0, 0)
        self.resting_bp_input = QSpinBox()
        self.resting_bp_input.setRange(80, 220)
        self.resting_bp_input.setValue(120)
        medical_layout.addWidget(self.resting_bp_input, 0, 1)
        
        # Cholesterol
        medical_layout.addWidget(QLabel("Cholestérol (mg/dl):"), 1, 0)
        self.cholesterol_input = QSpinBox()
        self.cholesterol_input.setRange(100, 600)
        self.cholesterol_input.setValue(200)
        medical_layout.addWidget(self.cholesterol_input, 1, 1)
        
        # FastingBS
        medical_layout.addWidget(QLabel("Glycémie à jeun > 120 mg/dl:"), 2, 0)
        self.fbs_layout = QHBoxLayout()
        self.fbs_yes = QCheckBox("Oui")
        self.fbs_no = QCheckBox("Non")
        self.fbs_no.setChecked(True)
        self.fbs_layout.addWidget(self.fbs_yes)
        self.fbs_layout.addWidget(self.fbs_no)
        medical_layout.addLayout(self.fbs_layout, 2, 1)
        
        # Connecter les checkboxes pour qu'ils soient mutuellement exclusifs
        self.fbs_yes.toggled.connect(lambda checked: self.fbs_no.setChecked(not checked))
        self.fbs_no.toggled.connect(lambda checked: self.fbs_yes.setChecked(not checked))
        
        # MaxHR
        medical_layout.addWidget(QLabel("Fréquence cardiaque maximale:"), 3, 0)
        self.max_hr_input = QSpinBox()
        self.max_hr_input.setRange(60, 220)
        self.max_hr_input.setValue(150)
        medical_layout.addWidget(self.max_hr_input, 3, 1)
        
        # Oldpeak
        medical_layout.addWidget(QLabel("Oldpeak (dépression ST):"), 4, 0)
        self.oldpeak_input = QDoubleSpinBox()
        self.oldpeak_input.setRange(0, 10)
        self.oldpeak_input.setSingleStep(0.1)
        self.oldpeak_input.setValue(0.0)
        medical_layout.addWidget(self.oldpeak_input, 4, 1)
        
        # ExerciseAngina
        medical_layout.addWidget(QLabel("Angine induite par l'exercice:"), 5, 0)
        self.exercise_angina_layout = QHBoxLayout()
        self.angina_yes = QCheckBox("Oui")
        self.angina_no = QCheckBox("Non")
        self.angina_no.setChecked(True)
        self.exercise_angina_layout.addWidget(self.angina_yes)
        self.exercise_angina_layout.addWidget(self.angina_no)
        medical_layout.addLayout(self.exercise_angina_layout, 5, 1)
        
        # Connecter les checkboxes pour qu'ils soient mutuellement exclusifs
        self.angina_yes.toggled.connect(lambda checked: self.angina_no.setChecked(not checked))
        self.angina_no.toggled.connect(lambda checked: self.angina_yes.setChecked(not checked))
        
        input_layout.addWidget(medical_group)
        
        # Groupe pour les types de douleur thoracique
        chest_pain_group = QGroupBox("Type de douleur thoracique")
        chest_pain_layout = QVBoxLayout()
        chest_pain_group.setLayout(chest_pain_layout)
        
        self.asy_pain = QCheckBox("ASY (Asymptomatique)")
        self.ata_pain = QCheckBox("ATA (Angine atypique)")
        self.nap_pain = QCheckBox("NAP (Douleur non angineuse)")
        self.ta_pain = QCheckBox("TA (Angine typique)")
        
        self.asy_pain.setChecked(True)
        
        chest_pain_layout.addWidget(self.asy_pain)
        chest_pain_layout.addWidget(self.ata_pain)
        chest_pain_layout.addWidget(self.nap_pain)
        chest_pain_layout.addWidget(self.ta_pain)
        
        # Connecter pour exclusivité mutuelle
        self.chest_pain_checkboxes = [self.asy_pain, self.ata_pain, self.nap_pain, self.ta_pain]
        for cb in self.chest_pain_checkboxes:
            cb.toggled.connect(self.ensure_one_chest_pain_selected)
        
        input_layout.addWidget(chest_pain_group)
        
        # Groupe pour la pente ST
        st_slope_group = QGroupBox("Pente du segment ST")
        st_slope_layout = QVBoxLayout()
        st_slope_group.setLayout(st_slope_layout)
        
        self.up_slope = QCheckBox("UP (Montant)")
        self.flat_slope = QCheckBox("Flat (Plat)")
        self.down_slope = QCheckBox("Down (Descendant)")
        
        self.up_slope.setChecked(True)
        
        st_slope_layout.addWidget(self.up_slope)
        st_slope_layout.addWidget(self.flat_slope)
        st_slope_layout.addWidget(self.down_slope)
        
        # Connecter pour exclusivité mutuelle
        self.st_slope_checkboxes = [self.up_slope, self.flat_slope, self.down_slope]
        for cb in self.st_slope_checkboxes:
            cb.toggled.connect(self.ensure_one_st_slope_selected)
        
        input_layout.addWidget(st_slope_group)
        
        # Groupe pour les résultats ECG au repos
        ecg_group = QGroupBox("Résultats ECG au repos")
        ecg_layout = QVBoxLayout()
        ecg_group.setLayout(ecg_layout)
        
        self.normal_ecg = QCheckBox("Normal")
        self.st_ecg = QCheckBox("Anomalie onde ST-T")
        self.lvh_ecg = QCheckBox("Hypertrophie ventriculaire gauche")
        
        self.normal_ecg.setChecked(True)
        
        ecg_layout.addWidget(self.normal_ecg)
        ecg_layout.addWidget(self.st_ecg)
        ecg_layout.addWidget(self.lvh_ecg)
        
        # Connecter pour exclusivité mutuelle
        self.ecg_checkboxes = [self.normal_ecg, self.st_ecg, self.lvh_ecg]
        for cb in self.ecg_checkboxes:
            cb.toggled.connect(self.ensure_one_ecg_selected)
        
        input_layout.addWidget(ecg_group)
        
        # Bouton de prédiction
        predict_button = QPushButton("Prédire")
        predict_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        predict_button.clicked.connect(self.run_prediction)
        main_layout.addWidget(predict_button)
        
        # Zone de résultats
        results_group = QGroupBox("Résultats")
        self.results_layout = QVBoxLayout()
        results_group.setLayout(self.results_layout)
        
        self.results_label = QLabel("Cliquez sur 'Prédire' pour obtenir les résultats")
        self.results_label.setAlignment(Qt.AlignCenter)
        self.results_layout.addWidget(self.results_label)
        
        main_layout.addWidget(results_group)
    
    def ensure_one_chest_pain_selected(self):
        """S'assure qu'un seul type de douleur thoracique est sélectionné"""
        sender = self.sender()
        if sender.isChecked():
            for cb in self.chest_pain_checkboxes:
                if cb != sender:
                    cb.setChecked(False)
        else:
            # S'assurer qu'au moins un est sélectionné
            if not any(cb.isChecked() for cb in self.chest_pain_checkboxes):
                sender.setChecked(True)
    
    def ensure_one_st_slope_selected(self):
        """S'assure qu'un seul type de pente ST est sélectionné"""
        sender = self.sender()
        if sender.isChecked():
            for cb in self.st_slope_checkboxes:
                if cb != sender:
                    cb.setChecked(False)
        else:
            # S'assurer qu'au moins un est sélectionné
            if not any(cb.isChecked() for cb in self.st_slope_checkboxes):
                sender.setChecked(True)
    
    def ensure_one_ecg_selected(self):
        """S'assure qu'un seul type d'ECG est sélectionné"""
        sender = self.sender()
        if sender.isChecked():
            for cb in self.ecg_checkboxes:
                if cb != sender:
                    cb.setChecked(False)
        else:
            # S'assurer qu'au moins un est sélectionné
            if not any(cb.isChecked() for cb in self.ecg_checkboxes):
                sender.setChecked(True)
    
    def collect_user_inputs(self):
        """Collecte toutes les entrées utilisateur et les prépare pour l'analyse"""
        user_data = []
        
        # Âge
        age = self.age_input.value()
        
        # Sexe (1 = homme, 0 = femme)
        sex = 1 if self.male_checkbox.isChecked() else 0
        
        # Pression artérielle
        resting_bp = self.resting_bp_input.value()
        
        # Cholestérol
        cholesterol = self.cholesterol_input.value()
        
        # Glycémie à jeun (1 = > 120 mg/dl, 0 = <= 120 mg/dl)
        fasting_bs = 1 if self.fbs_yes.isChecked() else 0
        
        # Fréquence cardiaque max
        max_hr = self.max_hr_input.value()
        
        # Oldpeak
        oldpeak = self.oldpeak_input.value()
        
        # Angine induite par l'exercice (1 = oui, 0 = non)
        exercise_angina = 1 if self.angina_yes.isChecked() else 0
        
        # Type de douleur thoracique (one-hot encoding)
        asy_pain = 1 if self.asy_pain.isChecked() else 0
        ata_pain = 1 if self.ata_pain.isChecked() else 0
        nap_pain = 1 if self.nap_pain.isChecked() else 0
        ta_pain = 1 if self.ta_pain.isChecked() else 0
        
        # Pente ST (one-hot encoding)
        up_slope = 1 if self.up_slope.isChecked() else 0
        flat_slope = 1 if self.flat_slope.isChecked() else 0
        down_slope = 1 if self.down_slope.isChecked() else 0
        
        # ECG au repos (one-hot encoding)
        normal_ecg = 1 if self.normal_ecg.isChecked() else 0
        st_ecg = 1 if self.st_ecg.isChecked() else 0
        lvh_ecg = 1 if self.lvh_ecg.isChecked() else 0
        
        # Construire le vecteur de caractéristiques dans l'ordre attendu par les modèles
        user_data = [
            [age, sex, resting_bp, cholesterol, fasting_bs, max_hr, exercise_angina, oldpeak,
             asy_pain, ata_pain, nap_pain, ta_pain, 
             normal_ecg, st_ecg, lvh_ecg,
             up_slope, flat_slope, down_slope]
        ]
        
        return user_data
    
    def run_prediction(self):
        """Exécute les prédictions pour tous les modèles disponibles"""
        try:
            # Collecter les données utilisateur
            user_data = self.collect_user_inputs()
            
            # Effacer les résultats précédents
            for i in reversed(range(self.results_layout.count())): 
                self.results_layout.itemAt(i).widget().setParent(None)
            
            # Ajouter un titre aux résultats
            results_title = QLabel("Probabilité de maladie cardiaque")
            results_title.setStyleSheet("font-weight: bold; font-size: 14px;")
            self.results_layout.addWidget(results_title)
            
            # Exécuter les prédictions pour chaque modèle
            results = {}
            
            if knn_available:
                try:
                    prob_malade, prob_non_malade = realiser_knn(user_data)
                    results["K-Nearest Neighbors"] = prob_malade
                except Exception as e:
                    print(f"Erreur avec KNN: {e}")
            
            if rf_available:
                try:
                    prob_malade, prob_non_malade = realiser_rf(user_data)
                    results["Random Forest"] = prob_malade
                except Exception as e:
                    print(f"Erreur avec RF: {e}")
            
            if lg_available:
                try:
                    prob_malade, prob_non_malade = realiser_lg(user_data)
                    results["Logistic Regression"] = prob_malade
                except Exception as e:
                    print(f"Erreur avec LG: {e}")
            
            if xgb_available:
                try:
                    prob_malade, prob_non_malade = realiser_xgb(user_data)
                    results["XGBoost"] = prob_malade
                except Exception as e:
                    print(f"Erreur avec XGB: {e}")
            
            # Afficher les résultats
            if results:
                for model_name, probability in results.items():
                    result_widget = QWidget()
                    result_layout = QHBoxLayout(result_widget)
                    
                    model_label = QLabel(f"{model_name}:")
                    result_layout.addWidget(model_label)
                    
                    progress_bar = QProgressBar()
                    progress_bar.setRange(0, 100)
                    progress_bar.setValue(int(probability))
                    progress_bar.setFormat("%.2f%%" % probability)
                    
                    # Ajuster la couleur en fonction du risque
                    if probability < 30:
                        progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")
                    elif probability < 70:
                        progress_bar.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
                    else:
                        progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
                    
                    result_layout.addWidget(progress_bar)
                    self.results_layout.addWidget(result_widget)
                
                # Ajouter un résumé
                avg_probability = sum(results.values()) / len(results)
                summary_label = QLabel(f"Moyenne de tous les modèles: {avg_probability:.2f}%")
                summary_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
                self.results_layout.addWidget(summary_label)
                
                recommendation = QLabel()
                if avg_probability < 30:
                    recommendation.setText("Recommandation: Risque faible - Consultez votre médecin pour un bilan de routine")
                    recommendation.setStyleSheet("color: green;")
                elif avg_probability < 70:
                    recommendation.setText("Recommandation: Risque modéré - Une consultation médicale est conseillée")
                    recommendation.setStyleSheet("color: orange;")
                else:
                    recommendation.setText("Recommandation: Risque élevé - Consultez rapidement un spécialiste")
                    recommendation.setStyleSheet("color: red;")
                
                self.results_layout.addWidget(recommendation)
            else:
                self.results_layout.addWidget(QLabel("Aucun modèle n'a pu fournir de prédiction"))
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardioPredictor()
    window.show()
    sys.exit(app.exec_())