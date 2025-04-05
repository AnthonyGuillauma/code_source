"""
Module des tests unitaires pour le filtre de log Apache.
"""

import pytest
from analyse.filtre_log_apache import FiltreLogApache


# Tests unitaires

@pytest.mark.parametrize("filtre_adresse_ip, filtre_code_statut_http", [
    (False, 200),
    ("127.0.0.1", False)
])
def test_filtre_log_type_invalide(filtre_adresse_ip, filtre_code_statut_http):
    """
    Vérifie que la classe renvoie une erreur lorsque un argument de type invalide
    est passé dans le constructeur.

    Scénarios testés:
        - Type incorrect pour le paramètre ``filtre_adresse_ip``.
        - Type incorrect pour le paramètre ``filtre_code_statut_http``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        filtre_adresse_ip (any): La vérification sur l'adresse IP.
        filtre_code_statut_http (any): La vérification sur le code de statut http.
    """
    with pytest.raises(TypeError):
        filtre = FiltreLogApache(filtre_adresse_ip, filtre_code_statut_http)

def test_filtre_log_entree_passe_filtre_type_invalide(filtre_log_apache):
    """
    Vérifie que la méthode ``entree_passe_filtre`` renvoie une erreur en cas
    de type de paramètre invalide.

    Scénarios testés:
        - Type incorrect pour le paramètre ``entree``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        filtre_log_apache (FiltreLogApache): Fixture pour l'instance 
            de la classe :class:`FiltreLogApache`.
    """
    with pytest.raises(TypeError):
        filtre_log_apache.entree_passe_filtre(False)

@pytest.mark.parametrize("filtre_adresse_ip, adresse_ip_entree, retour_attendu", [
    ("127.0.0.1", "127.0.0.1", True),
    ("127.0.0.2", "127.0.0.1", False),
    ("127.0.0.1", "127.0.0.2", False)
])
def test_filtre_log_entree_passe_filtre_adresse_ip_valide(filtre_log_apache,
                                                      entree_log_apache,
                                                      filtre_adresse_ip,
                                                      adresse_ip_entree,
                                                      retour_attendu):
    """
    Vérifie que la méthode ``entree_passe_filtre`` applique correctement la vérification
    sur l'adresse IP.

    Scénarios testés:
        - L'adresse IP de l'entrée égale à celle du filtre.
        - L'adresse IP de l'entrée différente de celle du filtre.

    Asserts:
        - La méthode ``entree_passe_filtre`` est égale à ``retour_attendu``.

    Args:
        filtre_log_apache (FiltreLogApache): Fixture pour l'instance 
            de la classe :class:`FiltreLogApache`.
        entree_log_apache (EntreeLogApache): Fixture pour l'instance 
            de la classe :class:`EntreeLogApache`.
        filtre_adresse_ip (str): La valeur du filtre de l'adresse IP.
        adresse_ip_entree (str): L'adresse IP de l'entrée.
        retour_attendu (bool): Le retour attendu par la méthode.
    """
    filtre_log_apache.adresse_ip = filtre_adresse_ip
    entree_log_apache.client.adresse_ip = adresse_ip_entree
    assert filtre_log_apache.entree_passe_filtre(entree_log_apache) == retour_attendu

@pytest.mark.parametrize("filtre_code_statut_http, code_statut_http_entree, retour_attendu", [
    (200, 200, True),
    (404, 200, False),
    (200, 404, False)
])
def test_filtre_log_entree_passe_filtre_code_statut_http_valide(filtre_log_apache,
                                                      entree_log_apache,
                                                      filtre_code_statut_http,
                                                      code_statut_http_entree,
                                                      retour_attendu):
    """
    Vérifie que la méthode ``entree_passe_filtre`` applique correctement la vérification
    sur le code de statut http.

    Scénarios testés:
        - Le code de statut http de l'entrée égale à celle du filtre.
        - Le code de statut http de l'entrée différente de celle du filtre.

    Asserts:
        - La méthode ``entree_passe_filtre`` est égale à ``retour_attendu``.

    Args:
        filtre_log_apache (FiltreLogApache): Fixture pour l'instance 
            de la classe :class:`FiltreLogApache`.
        entree_log_apache (EntreeLogApache): Fixture pour l'instance 
            de la classe :class:`EntreeLogApache`.
        filtre_code_statut_http (str): La valeur du filtre du code de statut http.
        code_statut_http_entree (str): Le code de statut http de l'entrée.
        retour_attendu (bool): Le retour attendu par la méthode.
    """
    filtre_log_apache.code_statut_http = filtre_code_statut_http
    entree_log_apache.reponse.code_statut_http = code_statut_http_entree
    assert filtre_log_apache.entree_passe_filtre(entree_log_apache) == retour_attendu