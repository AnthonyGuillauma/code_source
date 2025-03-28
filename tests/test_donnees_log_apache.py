"""
Module des tests unitaires pour les classes contenant les données des logs Apache
(ClientInformations, RequetesInformations et ReponseInformations).
"""

import pytest
from datetime import datetime, timezone, timedelta
from donnees.client_informations import ClientInformations
from donnees.requete_informations import RequeteInformations
from donnees.reponse_informations import ReponseInformations

@pytest.mark.parametrize("adresse_ip, identifiant_rfc, utilisateur, agent_utilisateur", [
    ("192.168.0.1", "rfc", "utilisateur", "Mozilla/5.0")
])
def test_client_informations_valide(adresse_ip, 
                                    identifiant_rfc, 
                                    utilisateur, 
                                    agent_utilisateur):
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
def test_client_exception_type_invalide(adresse_ip, 
                                        identifiant_rfc, 
                                        utilisateur, 
                                        agent_utilisateur):
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
def test_requete_informations_valide(horodatage, 
                                    methode_http, 
                                    url, 
                                    protocole_http,
                                    ancienne_url):
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
def test_requete_exception_type_invalide(horodatage, 
                                        methode_http, 
                                        url, 
                                        protocole_http,
                                        ancienne_url):
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
def test_reponse_informations_valide(code_statut_http,
                                     taille_octets):
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
    with pytest.raises(TypeError):
        reponse = ReponseInformations(
            code_statut_http,
            taille_octets
        )