"""
Modules des tests unitaires pour l'analyse statistique d'un fichier de log Apache.
"""

import pytest
from parse.fichier_log_apache import FichierLogApache
from analyse.analyseur_log_apache import AnalyseurLogApache

# Tests unitaires

@pytest.mark.parametrize("fichier, nombre_par_top", [
    (False, 3),
    (FichierLogApache("test.log"), False)
])
def test_analyseur_exception_type_invalide(fichier, nombre_par_top):
    """
    Vérifie que la classe AnalyseurLogApache lève une :class:`TypeError` si les types des 
    paramètres du constructeur sont invalides.

    Scénarios testés:
        - Type incorrect pour le paramètre ``fichier``.
        - Type incorrect pour le paramètre ``nombre_par_top``.

    Args:
        fichier (any): Représentation du fichier log.
        nombre_par_top (any): Nombre maximum d'éléments dans le top classement.
    """
    with pytest.raises(TypeError):
        analyseur = AnalyseurLogApache(fichier, nombre_par_top)

def test_analyseur_exception_valeur_nombre_par_top_invalide():
    """
    Vérifie que la classe AnalyseurLogApache lève une :class:`ValueError` si le
    paramètre ``nombre_par_top`` du constructeur est un entier négatif.

    Scénarios testés:
        - Nombre négatif pour ``nombre_par_top``.
    """
    with pytest.raises(ValueError):
        analyseur = AnalyseurLogApache(FichierLogApache("test.log"), -4)

@pytest.mark.parametrize("liste_elements, nom_element, mode_top_classement", [
    (0, "test", True),
    ([], 0, True),
    ([], "test", 0)
])
def test_analyseur_exception_repartition_elements_type_invalide(analyseur_log_apache, 
                                                      liste_elements, 
                                                      nom_element, 
                                                      mode_top_classement):
    """
    Vérifie que _get_repartition_elements lève une :class:`TypeError` si les types sont invalides.

    Scénarios testés:
        - ``liste_elements`` n'est pas une ``list``.
        - ``nom_element`` n'est pas un ``str``.
        - ``mode_top_classement`` n'est pas un ``bool``.

    Args:
        analyseur_log_apache (AnalyseurLogApache): Fixture pour l'instance 
            de la classe ``ParseurLogApache``.
        liste_elements (any): Liste des éléments à répartir.
        nom_element (any): Nom des éléments à analyser.
        mode_top_classement (any): Mode top-classement activé ou non.
    """
    with pytest.raises(TypeError):
        analyseur_log_apache._get_repartition_elements(liste_elements, 
                                                       nom_element, 
                                                       mode_top_classement)
        
@pytest.mark.parametrize("liste_elements, nom_element, resultat_attendu", [
    ([1] * 6 + [2] * 4, "chiffre", [
        {"chiffre": 1, "total": 6, "taux": 60.0},
        {"chiffre": 2, "total": 4, "taux": 40.0}
    ]),
    (["GET"] * 1 + ["POST"] * 7 + ["DELETE"] * 2, "methode", [
        {"methode": "POST", "total": 7, "taux": 70.0},
        {"methode": "DELETE", "total": 2, "taux": 20.0},
        {"methode": "GET", "total": 1, "taux": 10.0}
    ]),
])
def test_analyseur_repartition_elements_valide(analyseur_log_apache,
                                               liste_elements,
                                               nom_element,
                                               resultat_attendu):
    """
    Vérifie la répartition correcte des éléments dans ``_get_repartition_elements``.

    Scénarios testés:
        - Répartition de chiffres avec deux valeurs fréquentes.
        - Répartition de méthodes HTTP avec trois valeurs fréquentes.

    Asserts:
        - La liste est triée dans l'ordre attendu.
        - Le nombre d'éléments dans le résultat correspond à celui attendu.
        - Les totaux et les taux sont correctement calculés.
    
    Args:
        analyseur_log_apache (AnalyseurLogApache): Fixture pour l'instance 
            de la classe ``ParseurLogApache``.
        liste_elements (list): Liste des éléments à analyser.
        nom_element (str): Nom de l'élément à analyser.
        resultat_attendu (list): Résultat attendu après répartition.
    """
    repartitions = analyseur_log_apache._get_repartition_elements(
        liste_elements, nom_element
    )
    assert len(repartitions) == len(resultat_attendu)
    for repartition, resultat in zip(repartitions, resultat_attendu):
        assert repartition[nom_element] == resultat[nom_element]
        assert repartition["total"] == resultat["total"]
        assert repartition["taux"] == resultat["taux"]

@pytest.mark.parametrize("liste_elements, nom_element, nombre_top, resultat_attendu", [
    ([1] * 6 + [2] * 4, "chiffre", 1, [
        {"chiffre": 1, "total": 6, "taux": 60.0}
    ]),
    (["GET"] * 1 + ["POST"] * 7 + ["DELETE"] * 2, "methode", 2, [
        {"methode": "POST", "total": 7, "taux": 70.0},
        {"methode": "DELETE", "total": 2, "taux": 20.0}
    ]),
])
def test_analyseur_repartition_mode_top_elements_valide(analyseur_log_apache,
                                               liste_elements,
                                               nom_element,
                                               nombre_top,
                                               resultat_attendu):
    """
    Vérifie que ``_get_repartition_elements`` retourne les top éléments correctement.

    Scénarios testés:
        - Classement des chiffres avec un seul élément dans le top.
        - Classement des méthodes HTTP avec deux éléments dans le top.

    Asserts:
        - Le nombre de top éléments retournés correspond à ``nombre_top``.
        - Les totaux et les taux sont correctement calculés.

    Args:
        analyseur_log_apache (AnalyseurLogApache): Fixture pour l'instance 
            de la classe ``ParseurLogApache``.
        liste_elements (list): Liste des éléments à analyser.
        nom_element (str): Nom de l'élément à analyser.
        nombre_top (int): Nombre maximum d'éléments à retourner.
        resultat_attendu (list): Résultat attendu.
    """
    analyseur_log_apache.nombre_par_top = nombre_top
    repartitions = analyseur_log_apache._get_repartition_elements(
        liste_elements, nom_element, True
    )
    assert len(repartitions) == len(resultat_attendu)
    for repartition, resultat in zip(repartitions, resultat_attendu):
        assert repartition[nom_element] == resultat[nom_element]
        assert repartition["total"] == resultat["total"]
        assert repartition["taux"] == resultat["taux"]


def test_analyseur_top_urls_valide(analyseur_log_apache):
    """
    Vérifie que la méthode ``get_top_urls`` retourne correctement les URLs les plus fréquentées.

    Scénarios testés:
        - Vérification du tri et du calcul du taux de fréquence.

    Asserts:
        - La liste est triée dans l'ordre attendu.
        - Le nombre d'éléments dans le résultat correspond à celui attendu.

    Args:
        analyseur_log_apache (AnalyseurLogApache): Fixture pour l'instance 
            de la classe ParseurLogApache.
    """
    top_urls = analyseur_log_apache.get_top_urls()
    assert len(top_urls) == 2
    assert top_urls[0]["url"] == "/index.html"
    assert top_urls[0]["total"] == 3
    assert top_urls[0]["taux"] == 60.0
    assert top_urls[1]["url"] == "/"
    assert top_urls[1]["total"] == 2
    assert top_urls[1]["taux"] == 40.0

def test_analyseur_repartition_code_statut_htpp_valide(analyseur_log_apache):
    """
    Vérifie que ``get_total_par_code_statut_http`` retourne la répartition correcte des codes HTTP.

    Scénarios testés:
        - Vérification du tri et du calcul du taux de fréquence.

    Asserts:
        - La liste est triée dans l'ordre attendu.
        - Le nombre d'éléments dans le résultat correspond à celui attendu.
        
    Args:
        analyseur_log_apache (AnalyseurLogApache): Fixture pour l'instance 
            de la classe ParseurLogApache.
    """
    repartition = analyseur_log_apache.get_total_par_code_statut_http()
    assert len(repartition) == 2
    assert repartition[0]["code"] == 500
    assert repartition[0]["total"] == 4
    assert repartition[0]["taux"] == 80.0
    assert repartition[1]["code"] == 200
    assert repartition[1]["total"] == 1
    assert repartition[1]["taux"] == 20.0