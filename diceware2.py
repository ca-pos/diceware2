#from ast import main
#from typing import Optional
from cmath import phase
import sys
#from tarfile import NUL
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QLabel, QGroupBox, QLineEdit, QListWidget, QGridLayout, QButtonGroup

import secrets

h_size_max = 400
main_size = QSize(h_size_max,400)
    
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setUI()
#--------------------------------------------------------------------------------
    def declare_variables(self):
        ### Constantes de tailles des widgets
        ##
        #self.h_window = h_size_max - 16

        self.h_window = h_size_max-16
        self.g1g2_size = QSize(190, 90)
        self.g3_size = QSize(self.h_window, 50)
        self.phrase_size = QSize(self.h_window, 80)

        self.bg_color = "#abc"

        self.btn_nb_mots = list() # liste boutons (créés sans label)
        self.lbl_nb_mots = list() # liste labels à placer sous les boutons
        self.lyt_nb_mots = list() # liste layouts pour placer boutons et labels

        self.new_phrase = list()

        self.entropy_value = 113.48
        self.entropy_eval = 'Excellent'

        self.list = "l1.txt"
        self.list_only_words = True

        self.nb_words = 7
        self.sep_char = " "
#--------------------------------------------------------------------------------
    def setUI(self):
        self.declare_variables()
        self.create_groups()
        self.create_layouts()
        self.create_widgets()
        self.create_btn_words_number()
        self.add_widgets_to_main_layout()
        self.create_actions()
        self.create_menubar()
        self.create_statusbar()
        self.generate_phrase()
        self.display_phrase()
#        self.phrase.addItem(self.new_phrase)
#--------------------------------------------------------------------------------
    def create_actions(self):
        ### Menu action#
        #
        msg = "Créer une nouvelle phrase secrète"
        self.act_nouvelle = CAction( "&Nouvelle", "new", "N", msg)
        self.act_nouvelle.triggered.connect(self.on_new)

        msg = "Enregister dans un fichier"
        self.act_enregistrer = CAction("&Enregistrer", "save", "S", msg)
        self.act_enregistrer.triggered.connect(self.on_save)

        msg = "Quitter"
        self.act_quitter =CAction("&Quitter", "exit", "Q", msg)
        self.act_quitter.triggered.connect(self.on_quit)
#--------------------------------------------------------------------------------
    def on_new(self):
        self.generate_phrase()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def on_save(self):
        print("EEE")
#--------------------------------------------------------------------------------
    def on_quit(self):
        print("QQQ")
#--------------------------------------------------------------------------------
    def create_menubar(self):
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet(f"background-color: {self.bg_color}")
        # Fichier
        file = menu_bar.addMenu("&Fichier")
        file.addAction(self.act_nouvelle)
        file.addAction(self.act_enregistrer)
        file.addAction(self.act_quitter)
        # Aide
        help = menu_bar.addMenu("&Aide")
#--------------------------------------------------------------------------------
    def create_statusbar(self):
        status_bar = self.statusBar()
        status_bar.showMessage("Générateur de phrases secrètes")
#--------------------------------------------------------------------------------
    def create_groups(self):
        # Groupe 1. Composition de la phrase (mots ou mots/non mots)
        self.group_1 = QGroupBox( "Composition de la phrase")
        self.group_1.setFixedSize(self.g1g2_size)

        # Groupe 2. Nombre de mots de la phrase
        self.group_2 = QGroupBox("Nombre de mots")
        self.group_2.setFixedSize(self.g1g2_size)

        # Groupe 3. Choisir les caratères de séparation
        self.choix_sep = QGroupBox() # cadre autour du lineedit et du label
        self.choix_sep.setFixedSize(self.g3_size)

        # Groupe 4. Affichage de la phrase secrète (pas de goupe)

#--------------------------------------------------------------------------------
    def create_layouts(self):
        ### Style de background (main layout)
        #
        # création d'un container permettant l'application d'un style
        self.container = QWidget(self)
        self.container.setFixedSize(main_size)
        self.container.setStyleSheet(f"background-color: {self.bg_color}")
        # Le main layout a container comme parent
        self.main_layout = QGridLayout(self.container)
        self.main_layout.setSpacing(5)

        ### Groupe 1. Composition de la phrase (mots ou mots/non mots)
        #
        self.gbox1_layout = QVBoxLayout()
        self.group_1.setLayout(self.gbox1_layout) # application du layout

        ### Groupe 2. Nombre de mots
        #
        self.gbox2_layout = QHBoxLayout()
        self.group_2.setLayout(self.gbox2_layout) # application du layout
        
        ### Groupe 3. Choix séparateurs (lineedit et label côte à côte)
        #
        self.lyt_choix_sep = QHBoxLayout()
        self.choix_sep.setLayout(self.lyt_choix_sep)
        
        ### Groupe 4. Affichage de la phrase secrète générée dans une fenêtre
        # (pas de layout spécifique)
        #

        ### Groupe 5. Affichage de l'entropie et de son évaluation
        self.entropy_layout = QHBoxLayout()
        self.entropy_layout.setSpacing(0)
        # ce widget doit être créé ici pour pouvoir y assigner le layout !
        self.entropy_window = QWidget() 
        self.entropy_window.setLayout(self.entropy_layout)
#--------------------------------------------------------------------------------
    def create_widgets(self):
        self.texte = ""
    
        ### Groupe 1. Composition de la phrase, création des boutons du groupe 1 
        #
        btn_l1 = QRadioButton("Mots uniquement")    # choix de diceware
        btn_l1.setChecked(True)
        btn_l1.clicked.connect(self.list1)
        btn_l2 = QRadioButton("Mots et non mots")   # choix de wordlist
        btn_l2.clicked.connect(self.list2)
        # ajout des boutons au layout du groupe 1
        self.gbox1_layout.addWidget(btn_l1)
        self.gbox1_layout.addWidget(btn_l2)

        ### Groupe 3. lineedit & label du groupe
        #
        le_choix_sep = QLineEdit()
        le_choix_sep.setFixedSize(25, 25)
        le_choix_sep.setText(" ")    # séparateur par défaut
        le_choix_sep.textChanged.connect(self.sep_changed)
        self.sep_name = "[espace]"   # espace
        lbl_choix_sep = QLabel(f"Caractère(s) de séparation pour la sauvegarde  ({self.sep_name})")
        # ajout du label et du lineedit au layout
        self.lyt_choix_sep.addWidget(lbl_choix_sep)
        self.lyt_choix_sep.addWidget(le_choix_sep)

        ### Groupe 4. Affichage de la phrase
        #
        self.phrase = QListWidget()
        self.phrase.setFixedSize(self.phrase_size)
        #self.phrase.addItem(self.texte)

        ### Groupe 5. Affichage de l'entropie et de son évaluation
        #
        # entropie_window = QWidget() a été créé dans la section layout
        # afin de pouvoir lui assigner un layout
        self.entropy_window.setFixedSize(QSize(self.h_window, 30))
        self.entropy_window.setStyleSheet("background-color: #779")
        # valeur numérique de l'entropie en bits
        self.entropy = QLabel(f"Entropie = {self.entropy_value}")
        self.entropy.setMaximumWidth(110)
        # évaluation de la phrase (faible, moyen, etc.)
        self.entropy_class = QLabel(f"({self.entropy_eval})")
        self.entropy_class.setStyleSheet("color: #0f0")
        # ajout des deux widgets au layout
        self.entropy_layout.addWidget(self.entropy)
        self.entropy_layout.addWidget(self.entropy_class)
#--------------------------------------------------------------------------------
    def create_btn_words_number(self):
        ### Groupe 2. Nombre de mots de la phrase secrète (par défaut 7)
        ###
        for i in range(7):  # création de 7 boutons
            btn = QRadioButton("")  # création d'un bouton sans label
            btn.clicked.connect(self.on_btn)
            btn.value = i+4
            self.btn_nb_mots.append(btn) # le sauvegarder dans une liste
            if i == 3: # 7 mots, valeur par défaut
                btn.setChecked(True)
            btn.setFixedSize(15,20)
            lbl = QLabel(str(i+4))  # création du label (4 à 10)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)  # centrer lelabel
            lbl.setFixedSize(15,15)
            self.lbl_nb_mots.append(lbl) # le sauvegarder dans une liste
            lyt = QVBoxLayout() # création d'un layout pour construire lebouton
            lyt.setSpacing(0)   # pas d'espace entre les widgets du layout
            self.lyt_nb_mots.append(lyt) # le sauvegarder dans une liste
            # ajout du bouton et du label au layout 
            # (construction du bouton avec label au dessous)
            self.lyt_nb_mots[i].addWidget(self.btn_nb_mots[i])
            self.lyt_nb_mots[i].addWidget(self.lbl_nb_mots[i])
            # ajout du bouton créé au layout du groupe de boutons(gbox2_layout)
            self.gbox2_layout.addLayout(self.lyt_nb_mots[i])
    def on_btn(self):
        self.nb_words = self.sender().value
        self.generate_phrase()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def display_phrase(self):
        """efface la phrase précédente dans la fenêtre "phrase" puis affiche "phrase" """
        self.phrase.clear()
        phrase = str()
        length = len(self.new_phrase)
        for i in range(0, length):
            phrase += self.new_phrase[i]
            if not i == length-1:
                phrase += self.sep_char
        self.phrase.addItem(phrase)
#--------------------------------------------------------------------------------
    def add_widgets_to_main_layout(self):
        ### Groupe 1. Composition phrase
        self.main_layout.addWidget(self.group_1, 0, 0, 1, 1)

        ### Groupe 2. Nombre de mots de la phrase
        self.main_layout.addWidget(self.group_2, 0, 1, 1, 1) 

        ### Groupe 3. Choix des séparateurs
        self.main_layout.addWidget(self.choix_sep, 1, 0, 1, 2)

        ### Groupe 4. Affichage de la phrase
        self.main_layout.addWidget(self.phrase, 2, 0, 1, 2) 

        ### Groupe 5. Affichage de l'entropie
        self.main_layout.addWidget(self.entropy_window, 3, 0, 1, 2)   
#--------------------------------------------------------------------------------
    def list1(self):
        self.list = "l1.txt"
        self.list_only_words = True
        self.generate_phrase()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def list2(self):
        self.list = "l2.txt"
        self.list_only_words = False
        self.generate_phrase()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def sep_changed(self, new_sep):
        if new_sep.isprintable():
            old_sep = self.sep_char
            self.sep_char = new_sep
            #tmp = self.new_phrase.replace(old_sep, new_sep)
            #print(old_sep, new_sep, self.new_phrase, tmp)
            self.display_phrase()
#--------------------------------------------------------------------------------
    def generate_phrase(self):
        word_list = self.read_words_list()
        phrase_list = list()
        if self.list_only_words:
            for i in range(0, self.nb_words):
                rand = secrets.randbelow(len(word_list))
                phrase_list.append(word_list[rand])
        else:
            for i in range(0, self.nb_words):
                index = self.roll_dices()
                phrase_list.append(word_list[index][5:].replace(" ", ""))
        self.new_phrase = phrase_list
#--------------------------------------------------------------------------------
    def read_words_list(self):
        word_list = list()
        with open( self.list, "r") as file:
            lines = file.readlines()
        for line in lines:
            word_list.append(line.replace("\n", ""))
        return word_list
#--------------------------------------------------------------------------------
    def roll_dices(self):
        index = 0
        for i in range(0,5):    # 5 lancers de dés
            rand = secrets.randbelow(6)
            # calcul de l'index (multiples des puissances de 6)
            index += pow(6, i)*rand 
        return index
#################################################################################
class CAction(QAction):
    action = dict()
    def __init__(self, text, icon, shortcut, msg = ""):
        super().__init__(text)

        self.setShortcut("Ctrl+" + shortcut)
        self.setIcon(QIcon("icons/" + icon + ".png"))
        self.setStatusTip(msg)
#################################################################################
def main():
    app = QApplication(sys.argv)
    main_windows = MainWindow()
    main_windows.setFixedSize(main_size)
    main_windows.show()
    sys.exit(app.exec())
#################################################################################
if __name__ == '__main__':
    main()
