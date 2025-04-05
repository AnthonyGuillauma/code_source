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
            ExportationDossierParentException: Exportation impossible à cause de
                l'inexistance du dossier parent du fichier d'exportation.
        """
        # Vérification du type du paramètre
        if not isinstance(chemin_sortie, str):
            raise TypeError("Le chemin de sortie doit être une chaîne de caractère.")
        # Vérification du chemin d'exportation
        self.verification_exportation_possible(chemin_sortie)
        # Ajout du chemin d'exportation
        self._chemin_sortie = chemin_sortie

    def verification_exportation_possible(self, chemin_sortie: str) -> None:
        """
        Vérifie qu'une exportation est possible vers le chemin du fichier indiqué. Renvoie une
        exception expliquant le problème si elle n'est pas possible.

        Args:
            chemin_sortie (str): Le chemin du fichier d'exportation.

        Returns:
            None

        Raises:
            ExportationDossierParentException: Le dossier parent du fichier n'existe pas.
        """
        # Vérification du type du paramètre
        if not isinstance(chemin_sortie, str):
            raise TypeError("Le chemin de sortie doit être une chaîne de caractères.")
        # Vérification du chemin
        chemin_sortie_absolue = abspath(chemin_sortie)
        dossier_parent = dirname(chemin_sortie_absolue)
        if not isdir(dossier_parent):
            raise ExportationDossierParentException(f"Impossible d'exporter vers le "
                                       f"fichier {chemin_sortie}, son dossier parent "
                                       f"{dossier_parent} n'existe pas.")

    def export_vers_json(self, donnees: dict) -> None:
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
        # Vérification du type du paramètre
        if not isinstance(donnees, dict):
            raise TypeError("Les données à exporter doivent être sous une forme "
            "de dictionnaire.")
        # Exportation
        try:
            with open(self._chemin_sortie, 'w', encoding="utf-8") as fichier:
                dump(donnees, fichier, indent=4)
        except Exception as ex:
            raise ExportationException(str(ex)) from ex

class ExportationException(Exception):
    """
    Représente une erreur lors de l'exportation de données.
    """

class ExportationDossierParentException(ExportationException):
    """
    Représente une erreur lorsque une exportation est impossible
    lorsque le dossier parent du fichier d'exportation n'existe pas.
    """
