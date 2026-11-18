"""
Classe Database Interrogation
:author: usinelogicielle

:version: 0.1

:date: 2022/09/02
"""


class DatabaseInterrogation:
    def get_username(self):
        """
        Méthode permettant de récupérer le token d'accès à l'API de test
        """
        username = ""
        try:
            while username == "":
                username = input("Entrez votre username (pour accéder à test): ")
        except Exception:
            print("Erreur: Accès non valide veuillez reessayer")

