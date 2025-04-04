"""
Module des tests unitaires pour l'exporteur de données.
"""

import pytest
from json import load
from export.exporteur import Exporteur, ExportationException

@pytest.mark.parametrize("chemin_sortie", [
    (0), (None), ([])
])
def test_exporteur_type_chemin_invalide(chemin_sortie):
    """
    Vérifie que la classe renvoie une erreur lorsque un argument de type invalide
    est passé dans le constructeur.

    Scénarios testés:
        - Type incorrect pour le paramètre ``chemin_sortie``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        chemin_sortie (any): Le chemin de sortie utilisé dans le constructeur.
    """
    with pytest.raises(TypeError):
        exporteur = Exporteur(chemin_sortie)

def test_exporteur_emplacement_inexistant():
    """
    Vérifie que la classe renvoie une erreur lorsque un chemin de fichier invalide
    est passé dans le constructeur.

    Scénarios testés:
        - Chemin invalide pour le paramètre ``chemin_sortie``.

    Asserts:
        - Une exception :class:`ExportationException` est levée.
    """
    with pytest.raises(ExportationException):
        exporteur = Exporteur("dossier/inexistant/sortie.json")

def test_exporteur_verification_exception_exportation_possible_type_invalide(exporteur):
    """
    Vérifie que la méthode verification_exportation_possible renvoie une erreur lorsque le type
    de son paramètre est invalide.

    Scénarios testés:
        - Paramètre ``chemin_sortie`` avec un mauvais type.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
    """
    with pytest.raises(TypeError):
        exporteur.verification_exportation_possible(False)

@pytest.mark.parametrize("donnees", [
    (0), (None), ([])
])
def test_exporteur_export_json_type_donnees_invalide(exporteur, donnees):
    """
    Vérifie que la classe renvoie une erreur lorsque un argument de type invalide
    est passé dans la méthode ``export_vers_json``.

    Scénarios testés:
        - Type incorrect pour le paramètre ``données``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        donnees (any): Les données à exporter.
    """
    with pytest.raises(TypeError):
        exporteur.export_vers_json("type invalide")

@pytest.mark.parametrize("exception", [
    (PermissionError("Pas les droits")),
    (FileNotFoundError("Fichier non trouvé.")),
    (Exception("Toutes exceptions"))
])
def test_exporteur_export_json_exception_exportation(exporteur, mocker, exception):
    """
    Vérifie que la classe renvoie l'exception :class:`ExportationException` lorsque
    une erreur apparait durant l'exportation des données.

    Scénarios testés:
        - Une exception :class:`PermissionError` survient.
        - Une exception :class:`FileNotFoundError` survient.
        - Une exception :class:`Exception` survient.

    Asserts:
        - Une exception :class:`ExportationException` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        mocker (any): Une fixture pour simuler des exceptions.
        donnees (any): Les données à exporter.
    """
    mocker.patch("builtins.open", side_effect=exception)
    with pytest.raises(ExportationException):
        exporteur.export_vers_json({})

def test_exporteur_exportation_json_valide(exporteur, fichier_json):
    """
    Vérifie que la méthode ``export_vers_json`` exporte correctement les données
    vers une fichier.

    Scénarios testés:
        - Exportation d'un dictionnaire lambda.

    Asserts:
        - Le fichier est bien crée.
        - Les données dans le fichier sont conformes à celles fournies.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        fichier_json (Path): Le chemin du fichier.
    """
    donnees = {"cle": {"valeur": [1, 2, 3]}}
    exporteur.export_vers_json(donnees)
    assert fichier_json.exists()
    with open(fichier_json, "r") as exportation:
        contenu_exportation = load(exportation)
    assert contenu_exportation == donnees