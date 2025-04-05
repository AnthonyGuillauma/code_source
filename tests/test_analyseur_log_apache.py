"""
Modules des tests unitaires pour l'analyse statistique d'un fichier de log Apache.
"""

import pytest
from parse.fichier_log_apache import FichierLogApache
from analyse.filtre_log_apache import FiltreLogApache
from analyse.analyseur_log_apache import AnalyseurLogApache


# Tests unitaires

@pytest.mark.parametrize("fichier, filtre, nombre_par_top", [
    (False, FiltreLogApache(None, None), 3),
    (FichierLogApache("test.log"), False, 3),
    (FichierLogApache("test.log"), FiltreLogApache(None, None), False)
])
def test_analyseur_log_exception_type_invalide(fichier, filtre, nombre_par_top):
    """
    Vérifie que la classe AnalyseurLogApache lève une :class:`TypeError` si les types des 
    paramètres du constructeur sont invalides.

    Scénarios testés:
        - Type incorrect pour le paramètre ``fichier``.
        - Type incorrect pour le paramètre ``filtre``.
        - Type incorrect pour le paramètre ``nombre_par_top``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        fichier (any): Représentation du fichier log.
        nombre_par_top (any): Nombre maximum d'éléments dans le top classement.
    """
    with pytest.raises(TypeError):
        analyseur = AnalyseurLogApache(fichier, filtre, nombre_par_top)

def test_analyseur_log_exception_valeur_nombre_par_top_invalide():
    """
    Vérifie que la classe AnalyseurLogApache lève une exception si le
    paramètre ``nombre_par_top`` du constructeur est un entier négatif.

    Scénarios testés:
        - Nombre négatif pour ``nombre_par_top``.
    
    Asserts:
        - Une exception :class:`ValueError` est levée.
    """
    with pytest.raises(ValueError):
        analyseur = AnalyseurLogApache(FichierLogApache("test.log"),
                                       FiltreLogApache(None, None),
                                       -4)

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
    Vérifie que _get_repartition_elements lève une exception si les types sont invalides.

    Scénarios testés:
        - Type incorrect pour le paramètre ``liste_elements``.
        - Type incorrect pour le paramètre ``nom_element``.
        - Type incorrect pour le paramètre ``mode_top_classement``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

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

def test_analyseur_repartition_code_statut_http_valide(analyseur_log_apache):
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

@pytest.mark.parametrize("nombre_entrees", [
    (0), (3), (100)
])
def test_analyseur_get_total_entrees_valide(analyseur_log_apache,
                                            fichier_log_apache, 
                                            entree_log_apache, 
                                            nombre_entrees):
    """
    Vérifie que ``get_total_entrees`` retourne le nombre correcte d'entrées dans le fichier.

    Scénarios testés:
        - Vérification avec des fichiers avec des nombre d'entrées différents.

    Asserts:
        - La méthode renvoie le nombre d'éléments dans la liste.
        
    Args:
        analyseur_log_apache (AnalyseurLogApache): Fixture pour l'instance 
            de la classe :class:`AnalyseurLogApache`.
        fichier_log_apache (FichierLogApache): Fixture pour l'instance 
            de la classe :class:`FichierLogApache`.
        entree_log_apache (EntreeLogApache): Fixture pour l'instance 
            de la classe :class:`EntreeLogApache`.
        nombre_entrees (int): Le nombre total d'entrées dans le fichier.
    """
    fichier_log_apache.entrees = [entree_log_apache] * nombre_entrees
    assert analyseur_log_apache.get_total_entrees() == nombre_entrees

@pytest.mark.parametrize("nombre_entrees_valides", [
    (0), (3), (100)
])
def test_analyseur_get_entrees_passent_filtre_valide(mocker,
                                                     analyseur_log_apache,
                                                     entree_log_apache,
                                                     nombre_entrees_valides):
    """
    Vérifie que ``_get_entrees_passent_filtre`` retourne la liste des entrées
    qui passent le filtre.

    Scénarios testés:
        - Passage d'entrée à la méthode ``_get_entrees_passent_filtre``.

    Asserts:
        - Le nombre d'entrées retourné est égale au nombre de True retourné.
        
    Args:
        mocker (any): Fixture pour simuler des attributs et retours de méthode.
        analyseur_log_apache (AnalyseurLogApache): Fixture pour l'instance 
            de la classe :class:`AnalyseurLogApache`.
        entree_log_apache (EntreeLogApache): Fixture pour l'instance 
            de la classe :class:`EntreeLogApache`.
        nombre_entrees_valides (int): Le nombre d'entrées valides que retourne la méthode.
    """
    analyseur_log_apache.fichier = mocker.MagicMock()
    analyseur_log_apache.fichier.entrees = [entree_log_apache] * (nombre_entrees_valides * 2)

    retour_methode = [True] * nombre_entrees_valides
    retour_methode += [False] * nombre_entrees_valides

    analyseur_log_apache.filtre = mocker.MagicMock()
    analyseur_log_apache.filtre.entree_passe_filtre.side_effect = retour_methode

    entrees_filtre = analyseur_log_apache._get_entrees_passent_filtre()

    assert entrees_filtre == [entree_log_apache] * nombre_entrees_valides
    assert len(entrees_filtre) == nombre_entrees_valides

def test_analyseur_get_analyse_complete_valide(analyseur_log_apache):
    """
    Vérifie que ``get_analyse_complete`` retourne un rapport de l'analyse correct
    qui se base sur le retour des autres méthodes.

    Scénarios testés:
        - Vérification du rapport de l'analyse.

    Asserts:
        - Les éléments du rapport se basent sur les mêmes valeurs que les autres méthodes.
        
    Args:
        analyseur_log_apache (AnalyseurLogApache): Fixture pour l'instance 
            de la classe :class:`AnalyseurLogApache`.
    """
    analyse = analyseur_log_apache.get_analyse_complete()
    assert analyse["chemin"] == analyseur_log_apache.fichier.chemin
    assert analyse["total_entrees"] == analyseur_log_apache.get_total_entrees()
    assert analyse["filtre"] == analyseur_log_apache.filtre.get_dict_filtre()
    statistiques = analyse["statistiques"]
    assert statistiques["total_entrees_filtre"] == analyseur_log_apache.get_total_entrees_filtre()
    statistiques_requetes = statistiques["requetes"]
    assert statistiques_requetes["top_urls"] == analyseur_log_apache.get_top_urls()
    assert (statistiques_requetes["repartition_code_statut_http"] 
            == analyseur_log_apache.get_total_par_code_statut_http())
    