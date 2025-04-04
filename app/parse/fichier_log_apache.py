"""
Module qui contient la classe pour représenter un fichier log Apache.
"""

from dataclasses import dataclass, field
from parse.entree_log_apache import EntreeLogApache


@dataclass
class FichierLogApache:
    """
    Représente un fichier de log Apache.

    Attributes:
        chemin (str): Le chemin du fichier.
        entrees (list): La liste des entrées du fichier.
    """
    chemin: str
    entrees: list = field(default_factory=list)

    def __post_init__(self):
        """
        Vérifie le bon type des données de cette classe lors de l'initialisation de l'instance.

        Raises:
            TypeError: Une donnée n'est pas du bon type.
        """
        # Validation du chemin
        if not isinstance (self.chemin, str):
            raise TypeError("Le chemin du fichier doit être une chaîne de caractère.")
        if not isinstance (self.entrees, list):
            raise TypeError("La liste des entrées doit être une liste.")

    def ajoute_entree(self, entree: EntreeLogApache) -> None:
        """
        Ajoute une entrée à la liste des entrées du fichier.

        Args:
            entree (EntreeLogApache): L'entrée à ajouter.

        Returns:
            None

        Raises:
            TypeError: L'entrée ``entree`` n'est pas un objet :class:`EntreeLogApache`.
        """
        # Vérification du type du paramètre
        if not isinstance (entree, EntreeLogApache):
            raise TypeError("Les informations de l'entrée doivent être dans un objet"
                "EntreeLogApache.")

        # Récupération de l'entrée
        self.entrees.append(entree)
