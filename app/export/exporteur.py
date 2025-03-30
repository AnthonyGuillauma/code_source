"""
Module pour l'exportation des données.
"""

from os.path import abspath, dirname, isdir
from json import dump


class Exporteur:
    """
    Représente un exporteur de données pour exporter des données
    vers un fichier de sortie.

    Attributes:
        _chemin_sortie (str): Le chemin du fichier vers lequel
                les données seront exportées.
    """

    def __init__(self, chemin_sortie: str):
        """
        Initialise un exporteur de données.

        Args:
            chemin_sortie (str): Le chemin du fichier vers lequel
                les données seront exportées.
        
        Raises:
            TypeError: Le chemin de sortie n'est pas une chaîne de caractère.
            ExportationException: Exportation impossible à cause de
                l'emplacement invalide du fichier de sortie.
        """
        if not isinstance(chemin_sortie, str):
            raise TypeError("Le chemin de sortie doit être une chaîne de caractère.")
        chemin_sortie_absolue = abspath(chemin_sortie)
        dossier_parent = dirname(chemin_sortie_absolue)
        if not isdir(dossier_parent):
            raise ExportationException(f"Impossible d'exporter vers le "
                                       f"fichier {chemin_sortie}, son dossier parent "
                                       f"{dossier_parent} n'existe pas.")
        self._chemin_sortie = chemin_sortie

    def export_vers_json(self, donnees: dict):
        """
        Export le dictionnaire fourni vers le :attr:`chemin de sortie`.

        Args:
            donnees (dict): Le dictionnaire qui contient les données.

        Returns:
            None

        Raises:
            TypeError: Le paramètre ``donnees`` n'est pas un dictionnaire.
            ExportationException: Une erreur lors de l'écriture dans le fichier JSON.
        """
        if not isinstance(donnees, dict):
            raise TypeError("Les données à exporter doivent être sous une forme "
            "de dictionnaire.")
        
        try:
            with open(self._chemin_sortie, 'w') as fichier:
                dump(donnees, fichier, indent=4)
        except Exception as ex:
            raise ExportationException(str(ex)) from ex

class ExportationException(Exception):
    """
    Représente une erreur lors de l'exportation de données.
    """
    
    def __init__(self, *args):
        super().__init__(*args)
