"""
Module des tests unitaires pour l'exporteur de données.
"""

import pytest
from json import load
from export.exporteur import (Exporteur,
                              ExportationJsonException,
                              ExportationCamembertHtmlException,
                              ExportationDossierIntrouvableException)

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
    Vérifie que la classe renvoie une erreur lorsque un chemin de dossier invalide
    est passé dans le constructeur.

    Scénarios testés:
        - Chemin invalide pour le paramètre ``chemin_sortie``.

    Asserts:
        - Une exception :class:`ExportationDossierIntrouvableException` est levée.
    """
    with pytest.raises(ExportationDossierIntrouvableException):
        exporteur = Exporteur("dossier/inexistant/")

@pytest.mark.parametrize("donnees, nom_fichier", [
    (False, "fichier.json"), ({}, False)
])
def test_exporteur_export_json_type_donnees_invalide(exporteur, donnees, nom_fichier):
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
        exporteur.export_vers_json(donnees, nom_fichier)

@pytest.mark.parametrize("nom_fichier", [
    ("fichier.rst"), ("sorite.html")
])
def test_exporteur_exeption_export_vers_json_fichier_invalide(exporteur,
                                                               nom_fichier):
    with pytest.raises(ValueError):
        exporteur.export_vers_json({}, nom_fichier)

@pytest.mark.parametrize("exception", [
    (PermissionError("Pas les droits")),
    (FileNotFoundError("Fichier non trouvé.")),
    (Exception("Toutes exceptions"))
])
def test_exporteur_export_json_exception_exportation(exporteur, mocker, exception):
    """
    Vérifie que la classe renvoie l'exception :class:`ExportationJsonException` lorsque
    une erreur apparait durant l'exportation des données.

    Scénarios testés:
        - Une exception :class:`PermissionError` survient.
        - Une exception :class:`FileNotFoundError` survient.
        - Une exception :class:`Exception` survient.

    Asserts:
        - Une exception :class:`ExportationJsonException` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        mocker (any): Une fixture pour simuler des exceptions.
        exception (any): L'exception levée dans la méthode.
    """
    mocker.patch("builtins.open", side_effect=exception)
    with pytest.raises(ExportationJsonException):
        exporteur.export_vers_json({}, "fichier.json")

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
    exporteur.export_vers_json(donnees, "sortie.json")
    assert fichier_json.exists()
    with open(fichier_json, "r") as exportation:
        contenu_exportation = load(exportation)
    assert contenu_exportation == donnees

@pytest.mark.parametrize("donnees, nom_fichier", [
    (False, "fichier.html"),
    ([], False)
])
def test_exporteur_exception_export_vers_html_camembert_type_invalide(exporteur,
                                                                      donnees,
                                                                      nom_fichier):
    """
    Vérifie qu'une exception est levée lorsque les paramètres ont des types incorrects.

    Scénarios testés:
        - Type incorrect pour le paramètre ``donnees``.
        - Type incorrect pour le paramètre ``nom_fichier``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        donnees (any): Les données à mettre sous forme de camembert.
        nom_fichier (any): Le nom du fichier HTML qui contient le camembert.
    """
    with pytest.raises(TypeError):
        exporteur.export_vers_html_camembert(donnees, nom_fichier)

@pytest.mark.parametrize("nom_fichier", [
    ("fichier.rst"), ("sorite.json")
])
def test_exporteur_exception_export_vers_html_camembert_fichier_invalide(exporteur,
                                                                      nom_fichier):
    """
    Vérifie qu'une exception est levée lorsque le nom du fichier n'est pas un
    fichier HTML.

    Scénarios testés:
        - Passage d'un nom de fichier qui ne termine pas par '.html'.

    Asserts:
        - Une exception :class:`ValueError` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        nom_fichier (any): Le nom du fichier HTML qui contient le camembert.
    """
    with pytest.raises(ValueError):
        exporteur.export_vers_html_camembert([], nom_fichier)

@pytest.mark.parametrize("donnees", [
    (["test"]), ([False])
])
def test_exporteur_exception_export_vers_html_camembert_elements_donnees_invalide(
    exporteur,
    donnees):
    """
    Vérifie qu'une exception est levée lorsque le paramètre ``donnees`` n'est pas une liste
    de listes.

    Scénarios testés:
        - Passage d'une liste de données ne contenant pas de liste..

    Asserts:
        - Une exception :class:`ValueError` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        donnees (any): Le nom du fichier HTML qui contient le camembert.
    """
    with pytest.raises(ValueError):
        exporteur.export_vers_html_camembert(donnees, "sortie.html")

@pytest.mark.parametrize("donnees", [
    ([[1, 1, 1]]), ([[1]]), ([[]])
])
def test_exporteur_exception_export_vers_html_camembert_listes_non_2_elements_invalide(
    exporteur,
    donnees):
    """
    Vérifie qu'une exception est levée lorsque la liste des données contient des listes
    ne contenant pas deux éléments.

    Scénarios testés:
        - Lancement de la méthode avec des listes incorrectes.

    Asserts:
        - Une exception :class:`ValueError` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        donnees (dict): Les données à mettre sous forme de camembert.
    """
    with pytest.raises(ValueError):
        exporteur.export_vers_html_camembert(donnees, "sortie.html")

@pytest.mark.parametrize("donnees, nom_fichier", [
    ([[200, 1], [404, 10]], "fichier.html"),
    ([["test", 12], ["essaie", 50], ], "fichier.html")
])
def test_exporteur_export_vers_html_camembert_valide(exporteur,
                                                     donnees,
                                                     nom_fichier):
    """
    Vérifie qu'aucune exception n'est levée lorsque du déroulement normale
    de la méthode.

    Scénarios testés:
        - Lancement de la méthode avec des paramètres correctes.

    Asserts:
        - Aucune exception n'est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        donnees (dict): Les données à mettre sous forme de camembert.
        nom_fichier (str): Le nom du fichier HTML du camembert.
    """
    try:
        exporteur.export_vers_html_camembert(donnees, nom_fichier)
    except Exception:
        pytest.fail("Aucune exception ne doit être levée ici")

@pytest.mark.parametrize("exception", [
    (PermissionError("Pas les droits")),
    (FileNotFoundError("Fichier non trouvé.")),
    (Exception("Toutes exceptions"))
])
def test_exporteur_export_vers_html_camembert_exception_exportation(exporteur, mocker, exception):
    """
    Vérifie que la classe renvoie l'exception :class:`ExportationCamembertHtmlException` lorsque
    une erreur apparait durant l'exportation des données.

    Scénarios testés:
        - Une exception :class:`PermissionError` survient.
        - Une exception :class:`FileNotFoundError` survient.
        - Une exception :class:`Exception` survient.

    Asserts:
        - Une exception :class:`ExportationCamembertHtmlException` est levée.

    Args:
        exporteur (Exporteur) : Fixture pour l'instance de la classe :class:`Exporteur`.
        mocker (any): Une fixture pour simuler des exceptions.
        exception (any): L'exception levée dans la méthode.
    """
    mocker.patch("altair.Chart.save", side_effect=exception)
    with pytest.raises(ExportationCamembertHtmlException):
        exporteur.export_vers_html_camembert([[200, 1], [404, 3]], "fichier.html")
