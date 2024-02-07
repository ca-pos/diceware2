import sys
from math import log2
import secrets

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QLabel, QGroupBox, QLineEdit, QListWidget, QGridLayout, QFileDialog, QDialog, QPushButton, QDialogButtonBox, QTextEdit, QSizePolicy

h_size_max = 420
main_size = QSize(h_size_max,380)
    
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setUI()
#--------------------------------------------------------------------------------
    def declare_variables(self):

        ### Constantes de tailles des widgets
        ##
        self.h_window = h_size_max-16
        self.g1g2_size = QSize(200, 78)
        self.g3_size = QSize(self.h_window, 70)
        self.phrase_size = QSize(self.h_window, 60)
        self.bg_color = "#89b"
        self.frame_color = "#ff3"
        self.btn_nb_mots = list() # liste boutons (créés sans label)
        self.lbl_nb_mots = list() # liste labels à placer sous les boutons
        self.lyt_nb_mots = list() # liste layouts pour placer boutons et labels
        self.new_phrase = list()
        self.phrase_saved = False
        self.entropy_value = 0
        self.entropy_eval = ''
        #paramètres par défaut
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
        # générer une phrase avec les paramètres par défaut dès le démarrage
        self.generate_phrase()
        self.entropy_value = self.compute_entropy()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def create_actions(self):
        ### Menu action
        #
        # Fichier
        msg = "Créer une nouvelle phrase secrète"
        self.act_nouvelle = CAction( "&Nouvelle", "new", "N", msg)
        self.act_nouvelle.triggered.connect(self.on_new)

        msg = "Enregister dans un fichier"
        self.act_enregistrer = CAction("&Enregistrer", "save", "S", msg)
        self.act_enregistrer.triggered.connect(self.on_save)

        msg = "Quitter"
        self.act_quitter =CAction("&Quitter", "exit", "Q", msg)
        self.act_quitter.triggered.connect(self.closeEvent)

        # Aide
        msg = "Licence"
        self.act_show_licence = CAction("&Licence GPL (Français)", "open-source", "L", msg)
        self.act_show_licence.triggered.connect(self.show_licence)
        msg = "Readme"
        self.act_show_readme = CAction("&Readme", "readme", "R", msg)
        self.act_show_readme.triggered.connect(self.show_readme)
        msg = "Documentation"
        self.act_show_documentation = CAction("&Documentation", "help", "D", msg)
        self.act_show_documentation.triggered.connect(self.show_documentation)
        msg = "À Propos"
        self.act_show_about = CAction("À &Propos", "about", "P", msg)
        self.act_show_about.triggered.connect(self.show_about)
        # A E F L N P Q R
#--------------------------------------------------------------------------------
    def show_about(self):
        text = self.read_file_text("about.html")
        size = QSize(200, 40)
        self.show_info("À Propos", text, size)
#--------------------------------------------------------------------------------
    def show_documentation(self):
        text = self.read_file_text("documentation.html")
        self.show_info("Documentation", text)
#--------------------------------------------------------------------------------
    def show_readme(self):
        text = self.read_file_text("README.html")
        size = QSize(300, 350)
        self.show_info("Readme", text, size)
#--------------------------------------------------------------------------------
    def show_licence(self):
        text = self.read_file_text("gpl.inc")
        self.show_info("Licence Publique GNU", text)
#--------------------------------------------------------------------------------
    def show_info(self, title:str, text:str, size = QSize(800, 400)):
        self.info_window = QWidget()
        self.info_window.setMinimumSize(size)
        self.info_window.setWindowTitle(title)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        btn = QPushButton("Fermer")
        btn.setFixedSize(100, 25)
        btn.clicked.connect(self.close_info_window)
        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        text_edit.setHtml(text)
        self.info_window.setLayout(layout)
        self.info_window.show()
#--------------------------------------------------------------------------------
    def read_file_text(self, filename):
        text = str()
        with open(filename, "r") as f:
            line = f.readline()
            while line:
                text += line
                line = f.readline()
        return text
#--------------------------------------------------------------------------------
    def close_info_window(self):
        self.info_window.close()
#--------------------------------------------------------------------------------
    def on_new(self):
        self.generate_phrase()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def on_save(self):
        dialog = QFileDialog(self)
        dialog.setDirectory("/home/camille")

        if dialog.exec():
            file =dialog.selectedFiles()
            try:
                open(file[0])
            except(FileNotFoundError):
                self.save_ok(file[0])
            else:
                self.file_exists(file[0])
#--------------------------------------------------------------------------------
    def file_exists(self, file):
        choix = CDialog(message='Le fichier existe, voulez-vous le remplacer ?')
        choix.exec()
        if choix.retStatus:
            self.save_ok(file)
#--------------------------------------------------------------------------------
    def save_ok(self, file):
        phrase = self.compose_phrase()
        with open(file, "w") as f:
            f.write(phrase)
        self.phrase_saved = True
#--------------------------------------------------------------------------------
    def closeEvent(self, event):
        if self.phrase_saved:
            quit()
        choix = CDialog("La phrase secrète n'est pas sauvegardée\nQuitter quand même ?")
        choix.exec()
        if choix.retStatus:
            quit()
        elif not isinstance(event, bool):
            event.ignore()
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
        help.addAction(self.act_show_licence)
        help.addAction(self.act_show_readme)
        help.addAction(self.act_show_documentation)
        help.addAction(self.act_show_about)
#--------------------------------------------------------------------------------
    def create_statusbar(self):
        status_bar = self.statusBar()
        status_bar.showMessage("Générateur de phrases secrètes")
#--------------------------------------------------------------------------------
    def create_groups(self):
        # Groupe 1. Composition de la phrase (mots ou mots/non mots)
        self.group_1 = QGroupBox( "Composition de la phrase")
        self.group_1.setObjectName("GroupBox1")
        self.group_1.setFixedSize(self.g1g2_size)
        self.group_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.group_1.setStyleSheet('margin: 0px')

        # Groupe 2. Nombre de mots de la phrase
        self.group_2 = QGroupBox("Nombre de mots")
        self.group_2.setObjectName("GroupBox2")
        self.group_2.setFixedSize(self.g1g2_size)
        self.group_2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.group_2.setStyleSheet('margin: 0px')

        # Groupe 3. Choisir les caratères de séparation
        self.choix_sep = QGroupBox() # cadre autour du lineedit et du label
        self.choix_sep.setObjectName("GBChoixSep")
        self.choix_sep.setFixedSize(self.g3_size)
        self.choix_sep.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.choix_sep.setStyleSheet('margin: 0px; padding: 0px')

        # Groupe 4. Affichage de la phrase secrète (pas de goupe)

#--------------------------------------------------------------------------------
    def create_layouts(self):
        ### Style de background (main layout)
        #
        # création d'un container permettant l'application d'un style
        container = QWidget(self)
        container.setFixedSize(main_size)
        container.setStyleSheet(f"background-color: {self.bg_color}; ")
        # Le main layout a container comme parent
        self.main_layout = QGridLayout(container)
        self.main_layout.setSpacing(0)

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
        self.entropy_window.setObjectName("QWidgetEntropy")
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
        self.lbl_choix_sep = QLabel(f"Caractère(s) de séparation pour la sauvegarde  ({self.sep_name})")
        # ajout du label et du lineedit au layout
        self.lyt_choix_sep.addWidget(self.lbl_choix_sep)
        self.lyt_choix_sep.addWidget(le_choix_sep)

        ### Groupe 4. Affichage de la phrase
        #
        self.phrase = QListWidget()
        self.phrase.setFixedSize(self.phrase_size)
        self.phrase.setStyleSheet(f"border: 3px solid {self.frame_color}; border-radius: 6px; margin: 0px; padding: 0px")

        ### Groupe 5. Affichage de l'entropie et de son évaluation
        #
        # entropie_window = QWidget() a été créé dans la section layout
        # afin de pouvoir lui assigner un layout
        self.entropy_window.setFixedSize(QSize(self.h_window, 50))
        self.entropy_window.setStyleSheet("background-color: #779; margin: 0px; padding: 0px")
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
        #print(">>>", self.nb_words)
        self.generate_phrase()
        self.entropy_value = self.compute_entropy()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def display_phrase(self):
        """efface la phrase précédente dans la fenêtre "phrase" puis affiche "phrase" """
        self.phrase.clear()
        phrase = self.compose_phrase()
        self.phrase.addItem(phrase)
#--------------------------------------------------------------------------------
    def compose_phrase(self):
        phrase = str()
        length = len(self.new_phrase)
        for i in range(0, length):
            phrase += self.new_phrase[i]
            if not i == length-1:
                phrase += self.sep_char
        return phrase
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
        self.entropy_value = self.compute_entropy()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def list2(self):
        self.list = "l2.txt"
        self.list_only_words = False
        self.generate_phrase()
        self.entropy_value = self.compute_entropy()
        self.display_phrase()
#--------------------------------------------------------------------------------
    def compute_entropy(self):
        self.entropy_value = log2(pow(self.vocabulary_size, self.nb_words))
        if self.entropy_value < 50:
            entropy_eval = 'Faible'
        elif self.entropy_value < 70:
            entropy_eval= 'Moyen'
        elif self.entropy_value < 110:
            entropy_eval = 'Fort'
        else:
            entropy_eval = 'Très fort'
        val = '{:.2f}'.format(self.entropy_value)
        self.entropy.setText(f'Entropie  = {val}')
        self.entropy_class.setText('('+entropy_eval+')')
#--------------------------------------------------------------------------------
    def sep_changed(self, new_sep):
        if new_sep.isprintable():
            old_sep = self.sep_char
            self.sep_char = new_sep
            if new_sep == " ":
                self.sep_name = "[espace]"
            elif new_sep == "":
                self.sep_name = "[aucun]"
            else:
                self.sep_name = new_sep
            self.lbl_choix_sep.setText(f"Caractère(s) de séparation pour la sauvegarde  ({self.sep_name})")
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
        self.phrase_saved = False
#--------------------------------------------------------------------------------
    def read_words_list(self):
        word_list = list()
        with open( self.list, "r") as file:
            lines = file.readlines()
        for line in lines:
            word_list.append(line.replace("\n", ""))
        self.vocabulary_size = len(word_list)
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
class CDialog(QDialog):
    def __init__(self, message = "") -> None:
        super().__init__()
        self.retStatus = False  # évite une erreur si fermeture par la croix
        btn_yes = QPushButton("Oui")
        btn_yes.setObjectName("BtnYes")
        btn_yes.clicked.connect(self.ok)
        btn_no = QPushButton("Annuler")
        btn_no.setObjectName("BtnNo")
        btn_no.clicked.connect(self.cancel)
        buttons = QDialogButtonBox()
        buttons.addButton(btn_yes, QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton(btn_no, QDialogButtonBox.ButtonRole.RejectRole)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        layout.addWidget(buttons)
        self.setLayout(layout)
#--------------------------------------------------------------------------------
    def ok(self):
        self.retStatus = True
        self.close()
#--------------------------------------------------------------------------------
    def cancel(self):
        self.retStatus = False
        self.close()
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
    main_window = MainWindow()
    main_window.setFixedSize(main_size)
    main_window.setWindowTitle("Générateur de phrases secrètes")

    ### La section de code ci-dessous destinée à inclure le fichier qss dans le
    #   code marche à peu près mais le résultat n'est pas tout à fait le même que
    #   pour l'appel depuis la ligne de commande. À voir ultérieurement
    #
    # f = QFile("./style.qss")
    # f.open(QIODevice.ReadOnly)
    # app.setStyleSheet(QTextStream(f).readAll())

    main_window.show()
    sys.exit(app.exec())
#################################################################################
if __name__ == '__main__':
    main()
