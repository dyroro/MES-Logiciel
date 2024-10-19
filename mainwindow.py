import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
# Importer la fonction de l'algorithme de Johnson depuis le fichier externe
from johnson_algorithm import johnson_algorithm
# Importer le fichier de ressources compilé
import resources_rc  # C'est le fichier généré à partir de data.qrc

# Charger l'interface utilisateur à partir du fichier .ui
class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        # Charger le fichier appui.ui
        uic.loadUi("appui.ui", self)
# Connect the buttons to their respective functions
        self.actionNouveau.triggered.connect(self.new_file)
        self.actionopen_2.triggered.connect(self.open_file)
        self.actionEnregistrer.triggered.connect(self.save_file)
# Connecter le bouton "Create" à la fonction qui configure la table
        self.create.clicked.connect(self.create_table)  # Bouton pour créer la table
# Connecter le bouton "Calculate" pour exécuter l'algorithme de Johnson
        self.calcule.clicked.connect(self.calcule_johnson)
    def new_file(self):
        # Functionality for creating a new file
        response = QMessageBox.question(self,"New File","Are you sure you want to create a new file?",QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            self.lineEdit.clear()  # Clear the input text field, for example
            self.table.clear()     #clear the table

    def open_file(self):
        # Fonctionnalité pour ouvrir un fichier avec une extension spécifique
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir Fichier", "","Text Files (.txt);;Custom Files (.custom);;Tous les fichiers (*)")
        if file_name:
            with open(file_name, 'r') as file:
                lines = file.readlines()

                # Vérifiez qu'il y a suffisamment de lignes dans le fichier
                if len(lines) < 3:
                    QMessageBox.warning(self, "Erreur", "Le fichier doit contenir au moins 3 lignes.")
                    return

                # Lire les délais pour M1 et M2
                M1 = list(map(int, lines[1].strip().split()))  # Convertir la première ligne en liste d'entiers
                M2 = list(map(int, lines[2].strip().split()))  # Convertir la deuxième ligne en liste d'entiers

                # Vérifiez que M1 et M2 ont la même longueur
                if len(M1) != len(M2):
                    QMessageBox.warning(self, "Erreur", "Les lignes pour M1 et M2 doivent avoir la même longueur.")
                    return

                # Afficher les délais dans la table
                self.table.setColumnCount(len(M1))
                self.table.setRowCount(2)  # 2 lignes pour M1 et M2

                for col, value in enumerate(M1):
                    self.table.setItem(0, col, QtWidgets.QTableWidgetItem(str(value)))  # Ligne M1

                for col, value in enumerate(M2):
                    self.table.setItem(1, col, QtWidgets.QTableWidgetItem(str(value)))  # Ligne M2

                # Lire et afficher la solution dans textEdit
                solution = lines[4].strip()  # Lire la troisième ligne pour la solution
                self.textEdit.setPlainText(solution)  # Afficher la solution dans textEdit
                

                QMessageBox.information(self, "Fichier Ouvert", "Les données ont été chargées avec succès.")

    def save_file(self):
        # Fonctionnalité pour enregistrer un fichier avec une extension
        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer Fichier", "", "Text Files (.txt);;Custom Files (.custom);;Tous les fichiers (*)")
        if file_name:
            # Ajouter l'extension .txt si aucune extension n'est fournie
            if not (file_name.endswith('.txt') or file_name.endswith('.custom')):
                file_name += ".txt"  # ou ".custom" si vous préférez

            # Récupérer le contenu de la table
            tableau = ""
            for row in range(self.table.rowCount()):
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    tableau += (item.text() if item else '') + "\t"  # Ajouter un tabulateur pour séparer les valeurs
                tableau += "\n"  # Passer à la ligne suivante pour chaque ligne de la table

            # Écrire dans le fichier
            with open(file_name, 'w') as file:
                content = self.lineEdit.text()
                solution = self.textEdit.toPlainText()
                file.write(content)
                file.write("\n")
                file.write(tableau)
                file.write("\n")
                file.write(solution)

            QMessageBox.information(self, "Fichier Enregistré", "Votre fichier a été enregistré avec succès.")


    def create_table(self):
        """Créer et configurer la table lorsque le bouton 'Create' est cliqué."""
        try:
            # Récupérer le nombre de colonnes à partir de lineEdit
            num_columns = int(self.lineEdit.text())  # Convertir en entier
            if num_columns <= 0:
                raise ValueError("Le nombre de colonnes doit être positif.")

            # Fixer le nombre de colonnes et ajouter 2 lignes pour M1 et M2
            self.table.setColumnCount(num_columns)
            self.table.setRowCount(2)  # 2 lignes pour M1 et M2

            # Optionnel : Effacer les anciennes données du tableau
            self.table.clear()

            QMessageBox.information(self, "Table Configurée",f"Table configurée avec {num_columns} colonnes et 2 lignes.")

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un nombre valide pour le nombre de colonnes.")

    def calcule_johnson(self):
        """Récupérer les données de la table, exécuter l'algorithme de Johnson et afficher le résultat."""
        # Récupérer les valeurs de M1 et M2 depuis la table
        M1 = []
        M2 = []
        num_columns = self.table.columnCount()

        for col in range(num_columns):
            # Récupérer les valeurs de M1 (ligne 1)
            item_m1 = self.table.item(0, col)
            if item_m1 is not None:
                M1.append(int(item_m1.text()))  # Convertir en entier
            else:
                M1.append(0)

            # Récupérer les valeurs de M2 (ligne 2)
            item_m2 = self.table.item(1, col)
            if item_m2 is not None:
                M2.append(int(item_m2.text()))  # Convertir en entier
            else:
                M2.append(0)

        # Appeler l'algorithme de Johnson à partir du fichier importé
        SIGMA = johnson_algorithm(M1, M2)

        # Afficher le résultat dans le QTextEdit
        result = "Ordre optimal des tâches : [" + ", ".join(f'J{i }' for i in SIGMA) + "]"
        self.textEdit.setPlainText(result)

# Lancer l'application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())