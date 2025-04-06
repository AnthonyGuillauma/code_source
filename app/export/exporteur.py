"""
Module pour l'exportation des données.
"""

from os.path import abspath, isdir, join
from json import dump
from altair import Chart, Text, Theta, Color, vconcat
from pandas import DataFrame


class Exporteur:
    """
    Représente un exporteur de données pour exporter des données
    vers un fichier de sortie.

    Attributes:
        _chemin_sortie (str): Le chemin du dossier vers lequel les données
            vont être exportées.
    """

    def __init__(self, chemin_sortie: str):
        # Vérification du paramètre
        if not isinstance(chemin_sortie, str):
            raise TypeError("Le chemin de sortie doit être une chaîne de caractères.")
        # Vérification du chemin
        chemin_sortie_absolue = abspath(chemin_sortie)
        if not isdir(chemin_sortie_absolue):
            raise ExportationDossierIntrouvableException(f"Impossible d'exporter vers le "
                                       f"dossier {chemin_sortie} ({chemin_sortie_absolue}), "
                                        "le dossier n'existe pas.")
        # Ajout du chemin
        self._chemin_sortie = chemin_sortie

    def export_vers_json(self, donnees: dict, nom_fichier: str) -> None:
        """
        Export le dictionnaire fourni vers le ``chemin de sortie``.

        Args:
            donnees (dict): Le dictionnaire qui contient les données.
            nom_fichier (str): Le nom du fichier JSON.

        Returns:
            None

        Raises:
            TypeError: Le paramètre ``donnees`` n'est pas un dictionnaire.
            ExportationJsonException: Une erreur lors de l'écriture dans le fichier JSON.
        """
        # Vérification du type des paramètres
        if not isinstance(donnees, dict):
            raise TypeError("Les statistiques à exporter doivent être sous une forme "
            "de dictionnaire.")
        if not isinstance(nom_fichier, str):
            raise TypeError("Le nom du fichier doit être une chaîne de caractère.")
        # Vérification du nom du fichier
        if not nom_fichier.endswith(".json"):
            raise ValueError("Le fichier JSON doit terminé par l'extention '.json'.")
        # Exportation
        chemin_fichier = join(self._chemin_sortie, nom_fichier)
        try:
            with open(chemin_fichier, 'w', encoding="utf-8") as fichier:
                dump(donnees, fichier, indent=4)
        except Exception as ex:
            raise ExportationJsonException(str(ex)) from ex

    def export_vers_html_camembert(self,
                                     donnees: list,
                                     nom_fichier: str) -> None:
        """
        Export la liste fournie vers un camembert HTML vers le ``chemin de sortie``.

        Args:
            donnees (list): Les données du camembert. La liste doit contenir
                des listes de deux éléments où le premier reprèsente le nom de cette
                partie du camembert et le deuxième sa valeur.
            nom_fichier (str): Le nom du fichier HTML.

        Returns:
            None

        Raises:
            TypeError: Les paramètres ne sont pas du type attendu ou la liste ``donnees``
                contient un élément qui n'est pas une liste.
            ValueError: Le paramètre ``nom_fichier`` ne termine pas par .html ou le paramètre
                ``donnees`` ne contient pas des listes de longueur 2.
            ExportationCamembertHtmlException: Erreur lors de l'exportation du camembert.
        """
        # Vérification du type des paramètres
        if not isinstance(donnees, list):
            raise TypeError("Les données de l'histogramme à exporter doit être sous une forme "
                "de liste.")
        if not isinstance(nom_fichier, str):
            raise TypeError("Le nom du fichier doit être une chaîne de caractère.")
        # Vérification du nom du fichier
        if not nom_fichier.endswith(".html"):
            raise ValueError("Le fichier HTML doit terminé par l'extention '.html'.")
        # Récupération des axes du graphique
        axe_x = []
        axe_y = []
        for donnee in donnees:
            if not isinstance(donnee, list):
                raise ValueError("La liste des données de l'histogramme à exporter ne doit "
                    "contenir que des listes.")
            if not len(donnee) == 2:
                raise ValueError("La liste des données de l'histogramme à exporter ne doit "
                    "contenir que des listes de deux éléments (x, y).")
            axe_x.append(donnee[0])
            axe_y.append(donnee[1])
        axes = DataFrame({"x": axe_x, "y": axe_y})
        # Exportation
        try:
            chemin_fichier = join(self._chemin_sortie, nom_fichier)
            base = Chart(axes).encode(
                theta=Theta(field="y", type="quantitative"),
                color=Color(field="x", type="nominal"),
                tooltip=['x:N', 'y:Q']
            )
            camembert = base.mark_arc(outerRadius=200)
            graphique = (camembert).properties(
                width=400,
                height=400
            )
            graphique.save(chemin_fichier)
        except Exception as ex:
            raise ExportationCamembertHtmlException("Erreur lors de l'exportation "
                f"du camembert {nom_fichier} {ex}.") from ex


class ExportationException(Exception):
    """
    Représente une erreur lors de l'exportation de données.
    """

class ExportationJsonException(ExportationException):
    """
    Représente une erreur lors de l'exportation de données vers un format JSON.
    """

class ExportationCamembertHtmlException(ExportationException):
    """
    Représente une erreur lors de l'exportation de données vers un histogramme
    au format HTML.
    """

class ExportationDossierIntrouvableException(ExportationException):
    """
    Représente une erreur lorsque une exportation est impossible
    lorsque le dossier de l'exportation n'existe pas.
    """
