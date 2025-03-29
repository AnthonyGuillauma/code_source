"""
Module des tests unitaires pour les classes contenant les données des logs Apache.
"""

import pytest
from datetime import datetime, timezone, timedelta
from donnees.client_informations import ClientInformations
from donnees.requete_informations import RequeteInformations
from donnees.reponse_informations import ReponseInformations


@pytest.mark.parametrize("adresse_ip, identifiant_rfc, utilisateur, agent_utilisateur", [
    ("192.168.0.1", "rfc", "utilisateur", "Mozilla/5.0")
])
def test_donnees_client_informations_valide(adresse_ip, 
                                    identifiant_rfc, 
                                    utilisateur, 
                                    agent_utilisateur):
    """
    Vérifie que les arguments passés dans le constructeur de la classe :class:`ClientInformations`
    sont bien récupérés.

    Scénarios testés:
        - Création d'une instance avec des arguments valides.

    Asserts:
        - La valeur des arguments sont bien conservées au bon endroit avec la bonne valeur.

    Args:
        adresse_ip (str): Une adresse IP.
        identifiant_rfc (str): Un identifiant RFC.
        utilisateur (str): Un nom d'utilisateur.
        agent_utilisateur (str): Un User-Agent.
    """
    client = ClientInformations(
        adresse_ip,
        identifiant_rfc,
        utilisateur,
        agent_utilisateur
    )
    assert client.adresse_ip == adresse_ip
    assert client.identifiant_rfc == identifiant_rfc
    assert client.nom_utilisateur == utilisateur
    assert client.agent_utilisateur == agent_utilisateur

@pytest.mark.parametrize("adresse_ip, identifiant_rfc, utilisateur, agent_utilisateur", [
    (False, "rfc", "utilisateur", "Mozilla/5.0"),
    ("192.168.0.1", False, "utilisateur", "Mozilla/5.0"),
    ("192.168.0.1", "rfc", False, "Mozilla/5.0"),
    ("192.168.0.1", "rfc", "utilisateur", False)
])
def test_donnees_client_exception_type_invalide(adresse_ip, 
                                        identifiant_rfc, 
                                        utilisateur, 
                                        agent_utilisateur):
    """
    Vérifie que la classe renvoie une erreur lorsque un argument de type invalide
    est passé dans le constructeur.

    Scénarios testés:
        - Type incorrect pour le paramètre ``adresse_ip``.
        - Type incorrect pour le paramètre ``identifiant_rfc``.
        - Type incorrect pour le paramètre ``utilisateur``.
        - Type incorrect pour le paramètre ``agent_utilisateur``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        adresse_ip (any): Une adresse IP.
        identifiant_rfc (any): Un identifiant RFC.
        utilisateur (any): Un nom d'utilisateur.
        agent_utilisateur (any): Un User-Agent.
    """
    with pytest.raises(TypeError):
        client = ClientInformations(
            adresse_ip,
            identifiant_rfc,
            utilisateur,
            agent_utilisateur
        )

@pytest.mark.parametrize("horodatage, methode_http, url, protocole_http, ancienne_url", [
    (datetime(2012, 12, 12, 10, 10, 10, tzinfo=timezone(timedelta(hours=10))), 
     "POST", "essaie.fr/contact", "HTTP/1.2", "essaie.fr/accueil")
])
def test_donnes_requete_informations_valide(horodatage, 
                                    methode_http, 
                                    url, 
                                    protocole_http,
                                    ancienne_url):
    """
    Vérifie que les arguments passés dans le constructeur de la classe :class:`RequeteInformations`
    sont bien récupérés.

    Scénarios testés:
        - Création d'une instance avec des arguments valides.

    Asserts:
        - La valeur des arguments sont bien conservées au bon endroit avec la bonne valeur.

    Args:
        horodatage (datetime): La date de reception de la requête.
        methode_http (str): La méthode HTTP utilisée.
        url (str): La ressource demandée.
        protocole_http (str): Le protocole HTTP utilisé.
        ancienne_url (str): L'ancienne ressource demandée.
    """
    requete = RequeteInformations(
        horodatage,
        methode_http,
        url,
        protocole_http,
        ancienne_url
    )
    assert requete.horodatage == horodatage
    assert requete.methode_http == methode_http
    assert requete.url == url
    assert requete.protocole_http == protocole_http
    assert requete.ancienne_url == ancienne_url

@pytest.mark.parametrize("horodatage, methode_http, url, protocole_http, ancienne_url", [
    (False, "POST", "essaie.fr/contact", "HTTP/1.2", "essaie.fr/accueil"),
    (datetime(2012, 12, 12, 10, 10, 10, tzinfo=timezone(timedelta(hours=10))), 
     False, "essaie.fr/contact", "HTTP/1.2", "essaie.fr/accueil"),
    (datetime(2012, 12, 12, 10, 10, 10, tzinfo=timezone(timedelta(hours=10))), 
     "POST", False, "HTTP/1.2", "essaie.fr/accueil"),
    (datetime(2012, 12, 12, 10, 10, 10, tzinfo=timezone(timedelta(hours=10))), 
     "POST", "essaie.fr/contact", False, "essaie.fr/accueil"),
    (datetime(2012, 12, 12, 10, 10, 10, tzinfo=timezone(timedelta(hours=10))), 
     "POST", "essaie.fr/contact", "HTTP/1.2", False),
])
def test_donnees_requete_exception_type_invalide(horodatage, 
                                        methode_http, 
                                        url, 
                                        protocole_http,
                                        ancienne_url):
    """
    Vérifie que la classe renvoie une erreur lorsque un argument de type invalide
    est passé dans le constructeur.

    Scénarios testés:
        - Type incorrect pour le paramètre ``horodatage``.
        - Type incorrect pour le paramètre ``methode_http``.
        - Type incorrect pour le paramètre ``url``.
        - Type incorrect pour le paramètre ``protocole_http``.
        - Type incorrect pour le paramètre ``ancienne_url``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        horodatage (any): La date de reception de la requête.
        methode_http (any): La méthode HTTP utilisée.
        url (any): La ressource demandée.
        protocole_http (any): Le protocole HTTP utilisé.
        ancienne_url (any): L'ancienne ressource demandée.
    """
    with pytest.raises(TypeError):
        requete = RequeteInformations(
            horodatage, 
            methode_http, 
            url, 
            protocole_http,
            ancienne_url
        )

@pytest.mark.parametrize("code_statut_http, taille_octets", [
    (404, 50)
])
def test_donnes_reponse_informations_valide(code_statut_http,
                                     taille_octets):
    """
    Vérifie que les arguments passés dans le constructeur de la classe :class:`ReponseInformations`
    sont bien récupérés.

    Scénarios testés:
        - Création d'une instance avec des arguments valides.

    Asserts:
        - La valeur des arguments sont bien conservées au bon endroit avec la bonne valeur.

    Args:
        code_statut_http (int): La code de retour.
        taille_octets (int): La taille de la réponse en octets.
    """
    reponse = ReponseInformations(
        code_statut_http,
        taille_octets
    )
    assert reponse.code_statut_http == code_statut_http
    assert reponse.taille_octets == taille_octets

@pytest.mark.parametrize("code_statut_http, taille_octets", [
    (False, 50),
    (404, False)
])
def test_reponse_exception_type_invalide(code_statut_http,
                                         taille_octets):
    """
    Vérifie que la classe renvoie une erreur lorsque un argument de type invalide
    est passé dans le constructeur.

    Scénarios testés:
        - Type incorrect pour le paramètre ``code_statut_http``.
        - Type incorrect pour le paramètre ``taille_octets``.

    Asserts:
        - Une exception :class:`TypeError` est levée.

    Args:
        code_statut_http (int): La code de retour.
        taille_octets (int): La taille de la réponse en octets.
    """
    with pytest.raises(TypeError):
        reponse = ReponseInformations(
            code_statut_http,
            taille_octets
        )