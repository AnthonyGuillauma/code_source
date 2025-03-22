"""
Module qui contient les classes pour représenter un fichier log Apache.
"""


class FichierLogApache:
    """
    Représente un fichier de log Apache.
    """

    def __init__(self, chemin):
        self.chemin = chemin
        self.entrees = []

    def ajoute_entree(self, entree):
        """
        Ajoute une entrée à la liste des entrées du fichier.
        Args:
            entree (EntreeLogApache): L'entrée à ajouter.
        Returns:
            None
        """
        self.entrees.append(entree)