"""
Point d'entrée de l'application LogBuster !
"""
from cli.afficheur_cli import AfficheurCLI
from cli.parseur_arguments_cli import ParseurArgumentsCLI, ArgumentCLIException
from parse.parseur_log_apache import ParseurLogApache, ParsageLogApacheException
from analyse.filtre_log_apache import FiltreLogApache
from analyse.analyseur_log_apache import AnalyseurLogApache
from export.exporteur import Exporteur, ExportationException
from datetime import datetime

def main() -> None:
    """
    Point d'entrée de l'application.

    Returns:
        None
    """
    afficheur_cli = AfficheurCLI()
    afficheur_cli.affiche_message("Who ya gonna call? LogBuster!")
    try:
        # Récupération des arguments
        parseur_cli = ParseurArgumentsCLI()
        arguments_cli = parseur_cli.parse_args()
        # Lance l'animation de chargement
        afficheur_cli.lance_animation_chargement()
        # Analyse syntaxique du fichier log
        parseur_log = ParseurLogApache(arguments_cli.chemin_log)
        fichier_log = parseur_log.parse_fichier()
        # Filtre à appliquer lors de l'analyse
        filtre_log = FiltreLogApache(arguments_cli.ip, arguments_cli.code_statut_http)
        # Analyse statistique du fichier log
        analyseur_log = AnalyseurLogApache(fichier_log, filtre_log)
        analyse = analyseur_log.get_analyse_complete()
        # Exportation de l'analyse
        exporteur = Exporteur(arguments_cli.sortie)
        exporteur.export_vers_json(analyse, "analyse-log-apache.json")
        # Termine l'animation de chargement
        afficheur_cli.stop_animation_chargement()
    except ArgumentCLIException as ex:
        gestion_exception(afficheur_cli, "Erreur dans les arguments fournis !", ex)
    except ParsageLogApacheException as ex:
        gestion_exception(afficheur_cli, "Erreur dans l'analyse du log Apache !", ex)
    except ExportationException as ex:
        gestion_exception(afficheur_cli, "Erreur dans l'exportation de l'analyse !", ex)
    except (ValueError, TypeError) as ex:
        gestion_exception(afficheur_cli, "Erreur interne !", ex)

def gestion_exception(afficheur_cli: AfficheurCLI, message: str, exception: Exception) -> None:
    """
    Gère les erreurs qui demandent une fin du programme.
    Affiche un message d'erreur personnalisé ainsi que les détails de l'exception.

    Args:
        afficheur_cli (AfficheurCLI): L'objet permettant d'intéragir avec la ligne
            de commande.
        message (str): Message principal à afficher.
        exception (Exception): L'exception qui s'est produite.

    Returns:
        None
    """
    afficheur_cli.stop_animation_chargement(True)
    afficheur_cli.affiche_erreur(message, exception)

if __name__ == "__main__":
    main()
