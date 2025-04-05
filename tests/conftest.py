"""
Module de configuration des tests unitaires.
"""

import pytest
from cli.afficheur_cli import AfficheurCLI
from cli.parseur_arguments_cli import ParseurArgumentsCLI
from parse.parseur_log_apache import ParseurLogApache
from analyse.analyseur_log_apache import AnalyseurLogApache
from export.exporteur import Exporteur


# -----------------
# Données générales
# -----------------

# Lignes respectant la syntaxe d'un fichier de log Apache
lignes_valides =  [
        '192.168.1.1 - - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" 200 532',

        '::1 - - [05/Mar/2025:16:59:43 +0100] "POST / HTTP/1.1" 500 20'
        '"http://localhost/connexion.php" "Mozilla/5.0 (Windows NT 10.0;'
        ' Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"',

        '::1 - - [05/Mar/2025:16:59:43 +0100] "DELETE /index.html HTTP/2.1" 500 20',

        '::1 - test [05/Mar/2025:16:59:59 +0100] "DELETE /index.html HTTP/2.1" 500 20',

        '111.89.7.3 - essaie [27/Feb/2025:10:0:0 +0110] "GET / HTTP/2.1" 500 20'
]

# Lignes ne respectant pas la syntaxe d'un fichier de log Apache
lignes_invalides = [
        '',

        'Une ligne avec un format invalide !',

        '::1 - - [05/Mar/2025:16:59:43] "DELETE / HTTP/2.1" 200 20',

        '- - - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" 500 532',

        '::1 - - - "GET /index.html HTTP/1.1" 500 532',

        '::1 - - [12/Jan/2025:10:15:32 +0000] "GET /index.html HTTP/1.1" - 120'
]

# ------------------
# Fixtures générales
# ------------------

@pytest.fixture
def afficheur_cli():
    return AfficheurCLI()

@pytest.fixture
def parseur_arguments_cli():
    """
    Fixture pour initialiser le parseur d'arguments CLI.

    Returns:
        ParseurArgumentsCLI: Une instance de la classe :class:`ParseurArgumentsCLI`.
    """
    return ParseurArgumentsCLI()

@pytest.fixture()
def log_apache(tmp_path):
    """ 
    Fixture pour créer et récupérer un fichier de log Apache temporaire.
    Elle permet de générer un fichier de log Apache temporaire contenant
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
            valide (bool): Si ``True``, le fichier contient des lignes de log valides.
                Sinon, il contient des lignes invalides.

        Returns:
            Path: Le chemin du fichier de log temporaire créé.
        """
        contenu = (
            "\n".join(lignes_valides) 
            if valide == True
            else "\n".join(lignes_invalides)
        )
        fichier_temp = tmp_path / "access.log"
        fichier_temp.write_text(contenu)
        return fichier_temp
    return _creer_log

@pytest.fixture
def parseur_log_apache(log_apache, request):
    """
    Fixture pour initialiser un parseur de fichier de log Apache.

    Args:
        log_apache (Path): La fixture pour initialiser un fichier temporaire.
        request (object): Paramètre de la fonction. Si il est égale à ``False``, cette fixture
            retourne un parseur de log Apache qui analyse un fichier avec un format
            invalide. Sinon, retourne un parseur de log Apache qui analyse un fichier
            avec un format valide.

    Returns:
        ParseurLogApache: Une instance de la classe :class:`ParseurLogApache`.
    """
    if hasattr(request, "param") and request.param == False:
        return ParseurLogApache(str(log_apache(False)))
    return ParseurLogApache(str(log_apache(True)))

@pytest.fixture()
def fichier_log_apache(parseur_log_apache):
    """
    Fixture pour initialiser une représentation d'un fichier de log Apache.
    Cette représentation comprend par défaut les entrées parsées de la liste
    ``lignes_valides``.

    Args:
        parseur_arguments_cli (ParseurArgumentsCLI): Fixture pour l'instance 
            de la classe :class:`ParseurLogApache`.

    Returns:
        FichierLogApache: Une instance de la classe :class:`FichierLogApache`.
    """
    return parseur_log_apache.parse_fichier()

@pytest.fixture()
def entree_log_apache(fichier_log_apache):
    """
    Fixture pour initialiser une représentation d'une entrée d'un fichier de log Apache.
    Cette représentation comprend par défaut les informations de la première ligne de
    ``lignes_valides``.

    Args:
        fichier_log_apache (EntreeLogApache): Fixture pour l'instance 
            de la classe :class:`EntreeLogApache`.

    Returns:
        EntreeLogApache: Une instance de la classe :class:`EntreeLogApache`.
    """
    return fichier_log_apache.entrees[0]

@pytest.fixture()
def analyseur_log_apache(fichier_log_apache):
    """
    Fixture pour initialiser un analyseur statistique de fichier de log Apache.
    Le fichier qu'analyse cet analyseur comprend par défaut les entrées parsées de la liste
    ``lignes_valides``.

    Args:
        fichier_log_apache (FichierLogApache): Fixture pour l'instance 
            de la classe :class:`FichierLogApache`.

    Returns:
        AnalyseurLogApache: Une instance de la classe :class:`AnalyseurLogApache`.
    """
    return AnalyseurLogApache(fichier_log_apache)

@pytest.fixture
def fichier_json(tmp_path):
    """
    Fixture pour retourner un chemin de fichier JSON temporaire.

    Args:
        tmp_path (Path): Chemin temporaire fourni par pytest.

    Returns:
        Path: Un chemin de fichier JSON temporaire.
    """
    fichier_temp = tmp_path / "sortie.json"
    return fichier_temp

@pytest.fixture
def exporteur(fichier_json):
    """
    Fixture pour initialiser un exportateur de données.

    Args:
        fichier_json (Path): Fixture pour initialiser 
            un chemin de fichier json temporaire.

    Returns:
        Exporteur: Une instance de la classe :class:`Exportateur`.
    """
    return Exporteur(str(fichier_json))