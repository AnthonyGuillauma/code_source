"""
Module des tests unitaires pour le parseur de fichier de log Apache.
"""

import pytest
from re import match
from datetime import datetime, timezone, timedelta
from parse.parseur_log_apache import ParseurLogApache, FormatLogApacheInvalideException

# Données utilisées pour les tests unitaires

# Liste d'entrées valides
lignes_log_apache = [
    # Première entrée
    '192.168.1.1 - - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 532',
    # Deuxième entrée
    '::1 - - [05/Mar/2025:16:59:43 +0100] "POST /backend/getConnexion.php HTTP/1.1" 200 20'
    '"http://localhost/backend/connexion.php?titre=Connexion" "Mozilla/5.0 (Windows NT 10.0;'
    ' Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"',
    # Troisième entrée
    '::1 - - [05/Mar/2025:16:59:43 +0100] "DELETE / HTTP/2.1" 200 20'
]

# Liste d'entrées invalides
lignes_log_apache_invalides = [
    '',
    'Une ligne avec un format invalide !',
    '::1 - - [05/Mar/2025:16:59:43] "DELETE / HTTP/2.1" 200 20',
    '192.168.1.1 - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" test 532'
]

@pytest.fixture()
def log_apache(tmp_path):
    """ 
    Fixture pour créer et récupérer un fichier de log Apache temporaire.
    Cette fixture permet de générer un fichier de log Apache temporaire contenant
    soit des lignes valides, soit des lignes invalides selon le paramètre fourni.
    Args:
        tmp_path (Path): Chemin temporaire fourni par pytest.
    Returns:
        Callable[[bool], Path]: Une fonction qui crée et retourne le chemin 
        du fichier de log temporaire.
    """
    def _creer_log(valide):
        """
        Crée un fichier de log Apache temporaire.
        Args:
            valide (bool): Si True, le fichier contient des lignes de log valides.
                Sinon, il contient des lignes invalides.
        Returns:
            Path: Le chemin du fichier de log temporaire créé.
        """
        contenu = (
            "\n".join(lignes_log_apache) 
            if valide == True
            else "\n".join(lignes_log_apache_invalides)
        )
        fichier_temp = tmp_path / "access.log"
        fichier_temp.write_text(contenu)
        return fichier_temp
    return _creer_log

@pytest.fixture
def parseur_log_apache(log_apache, request):
    """
    Fixture pour initialiser le parseur de log Apache.
    Retourne une instance de la classe ParseurLogApache pour être utilisée dans les tests.
    Returns:
        ParseurLogApache: Une instance de la classe ParseurArgumentsCLI.
    """
    if hasattr(request, "param") and request.param == False:
        return ParseurLogApache(log_apache(False))
    return ParseurLogApache(log_apache(True))


# Tests unitaires

def test_exception_fichier_invalide():
    """
    Vérifie qu'une exception est bien levée lorsque le fichier n'existe pas.
    Returns:
        None
    """
    with pytest.raises(FileNotFoundError):
        parseur = ParseurLogApache("fichier/existe/pas.txt")

@pytest.mark.parametrize("parseur_log_apache", [False], indirect=["parseur_log_apache"])
def test_exception_fichier_invalide(parseur_log_apache):
    """
    Vérifie qu'une exception est bien levée lorsque le format d'un fichier n'est
    pas valide (une entrée invalide).
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe ParseurLogApache.
    Returns:
        None
    """
    with pytest.raises(FormatLogApacheInvalideException):
        fichier = parseur_log_apache.parse_fichier()

@pytest.mark.parametrize("ligne_log", lignes_log_apache_invalides)
def test_exception_entree_invalide(parseur_log_apache, ligne_log):
    """
    Vérifie qu'une exception est bien levée lorsque le format d'au moins une
    entrée est invalide dans un fichier de log Apache.
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe ParseurLogApache.
        ligne_log (str): L'entrée à analyser.
    Returns:
        None
    """
    with pytest.raises(FormatLogApacheInvalideException):
        parseur_log_apache.parse_entree(ligne_log)

def test_nombre_entrees_valide(parseur_log_apache):
    """
    Vérifie que le nombre d'entrées trouvé correspond au nombre de ligne dans le log.
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe ParseurLogApache.
    Returns:
        None
    """
    fichier_log = parseur_log_apache.parse_fichier()
    assert len(fichier_log.entrees) == len(lignes_log_apache)

@pytest.mark.parametrize("nom_information, retour_attendu", [
    ("ip", "192.168.1.1"),
    ("rfc", None),
    ("horodatage", "12/Jan/2025:10:15:32 +0000"),
    ("Existe pas !", None)
])
def test_regex_recuperation_information_entree(parseur_log_apache, nom_information, retour_attendu):
    """
    Vérifie que la récupération des informations à partir d'un résultat de regex fonctionne
    correctement et que toutes valeurs introuvables ou égales à - renvoient None. 
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe ParseurLogApache.
        nom_information (str): Nom de l'information à récupérer.
        retour_attendu (Union[None, str]): La valeur attendue de l'information.
    Returns:
        None
    """
    ligne = '192.168.1.1 - - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 532'
    analyse = match(parseur_log_apache.PATTERN_ENTREE_LOG_APACHE, ligne)
    resultat_analyse = analyse.groupdict()
    assert parseur_log_apache.get_information_entree(resultat_analyse, nom_information) == retour_attendu

def test_parsage_entree_valide(parseur_log_apache):
    """
    Vérifie qu'une entrée est correctement analysée et que les informations partent
    au bon endroit avec le bon typage.
    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe ParseurLogApache.
    Returns:
        None
    """
    ligne = '192.168.1.1 - - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" ' \
    '200 532 "/home" "Chrome/133.0.0.0"'
    entree = parseur_log_apache.parse_entree(ligne)
    assert entree.client.adresse_ip == "192.168.1.1"
    assert entree.client.identifiant_rfc == None
    assert entree.client.nom_utilisateur == None
    assert entree.client.agent_utilisateur == "Chrome/133.0.0.0"
    assert entree.requete.horodatage == datetime(2025, 1, 12, 10, 15, 32, 
                                                 tzinfo=timezone(timedelta(hours=0)))
    assert entree.requete.methode_http == "GET"
    assert entree.requete.url == "/index.html"
    assert entree.requete.protocole_http == "HTTP/1.1"
    assert entree.requete.ancienne_url == "/home"
    assert entree.reponse.code_statut_http == 200
    assert entree.reponse.taille_octets == 532
