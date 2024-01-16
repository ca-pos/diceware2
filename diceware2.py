from ast import main
import sys
#from typing import Optional
from PySide6.QtCore import Qt, QSize

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QLabel, QGroupBox, QLineEdit, QListWidget, QGridLayout

h_size_max = 400
main_size = QSize(h_size_max,400)
    
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setUI()

    def setUI(self):

        ### Constantes de tailles des widgets
        ##
        h_window = h_size_max - 16
        g1g2_size = QSize(190, 90)
        g3_size = QSize(h_window, 50)
        phrase_size = QSize(h_window, 80)
        ### Style de background
        ##
        # création d'un container permettant l'application d'un style
        container = QWidget(self)
        container.setFixedSize(main_size)
        container.setStyleSheet("background-color: #bbc")
        # Le main layout a container comme parent
        main_layout = QGridLayout(container)

        ### Groupe 1. Choix de la liste (boutons) : diceware (mots) ou wordlist(mots    et non mots)
        ###
        gbox1_layout = QVBoxLayout()    # création layout pour groupe de boutons
        main_layout.setSpacing(5)
        group_1 = QGroupBox("Composition de la phrase") # création du groupe
        group_1.setFixedSize(g1g2_size)
        group_1.setLayout(gbox1_layout) # et application du layout au groupe
        # création des boutons
        btn_l1 = QRadioButton("Mots uniquement")    # choix de diceware
        btn_l2 = QRadioButton("Mots et non mots")   # choix de wordlist
        # ajout des boutons au layout du groupe 1
        gbox1_layout.addWidget(btn_l1)
        gbox1_layout.addWidget(btn_l2)

        ### Groupe 2. Nombre de mots de la phrase secrète (par défaut 7)
        ###
        # groupe de boutons : nombre de mots
        gbox2_layout = QHBoxLayout()    # layout pour le groupe de boutons
        group_2 = QGroupBox("Nombre de mots")   # groupe de boutons
        group_2.setFixedSize(g1g2_size)
        group_2.setLayout(gbox2_layout) # application du layout
        btn_nb_mots = list()    # liste des boutons (créés sans label)
        lbl_nb_mots = list()    # liste des labels à placer sous les boutons
        lyt_nb_mots = list()    # liste des layouts pour placer boutons et labels
        for i in range(7):  # création de 7 boutons
            btn = QRadioButton("")  # création d'un bouton sans label
            btn_nb_mots.append(btn) # le sauvegarder dans une liste
            if i == 3: # 7 mots, valeur par défaut
                btn.setChecked(True)
            btn.setFixedSize(15,20)
            lbl = QLabel(str(i+4))  # création du label (4 à 10)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)  # centrer le label
            lbl.setFixedSize(15,15)
            lbl_nb_mots.append(lbl) # le sauvegarder dans une liste
            lyt = QVBoxLayout() # création d'un layout pour construire le bouton
            lyt.setSpacing(0)   # pas d'espace entre les widgets du layout
            lyt_nb_mots.append(lyt) # le sauvegarder dans une liste
            # ajout du bouton et du label au layout (construction du bouton     aveclabel au dessous)
            lyt_nb_mots[i].addWidget(btn_nb_mots[i])
            lyt_nb_mots[i].addWidget(lbl_nb_mots[i])
            # ajout du bouton créé au layout du groupe de boutons (gbox2_layout)
            gbox2_layout.addLayout(lyt_nb_mots[i])

        ### Groupe 3. Caractère(s) de séparation entre les mots (par défaut,rien,   les mots sont collés les uns aux autres)
        ###
        choix_sep = QGroupBox() # permet un cadre autour du lineedit et du label
        choix_sep.setFixedSize(g3_size)
        lyt_choix_sep = QHBoxLayout()   # le lineedit et le label côte à côte
        choix_sep.setLayout(lyt_choix_sep)
        le_choix_sep = QLineEdit()
        le_choix_sep.setFixedSize(25, 25)
        le_choix_sep.setText("")    # séparateur par défaut
        sep_name = "[aucun]"        # aucun
        lbl_choix_sep = QLabel(f"Caractère(s) de séparation pour la sauvegarde  ({sep_name})")
        lyt_choix_sep.addWidget(lbl_choix_sep)
        lyt_choix_sep.addWidget(le_choix_sep)

        ### Groupe 4. Affichage de la phrase secrète générée dans une fenêtre
        ###
        texte = "sperme exil éveil ulcère tract rock partie étang pendulecornemuse"
        phrase = QListWidget()
        phrase.setFixedSize(phrase_size)
        phrase.addItem(texte)

        ### Groupe 5. Affichage de l'entropie et de son évaluation
        ###
        entropy_value = 113.48
        entropy_eval = 'Excellent'

        entropy_window = QWidget()
        entropy_layout = QHBoxLayout()
        entropy_layout.setSpacing(0)
        entropy_window.setLayout(entropy_layout)
        entropy_window.setFixedSize(QSize(h_window, 30))

        entropy = QLabel(f"Entropie = {entropy_value}")
        entropy.setMaximumWidth(110)
        entropy_class = QLabel(f"({entropy_eval})")
        entropy_window.setStyleSheet("background-color: #777")
        entropy_class.setStyleSheet("color: #0f0")
        entropy_layout.addWidget(entropy)
        entropy_layout.addWidget(entropy_class)

        ### Ajout des widgets au main layout
        ###
        main_layout.addWidget(group_1, 0, 0, 1, 1)  # composition phrase
        main_layout.addWidget(group_2, 0, 1, 1, 1)  # nb de mots de la phrase
        main_layout.addWidget(choix_sep, 1, 0, 1, 2)# séparateurs 
        main_layout.addWidget(phrase, 2, 0, 1, 2)   # affichage de la phrase
        main_layout.addWidget(entropy_window, 3, 0, 1, 2)

def main():
    app = QApplication(sys.argv)
    main_windows = MainWindow()
    main_windows.setFixedSize(main_size)
    main_windows.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
