"""
Point d'entrée de l'application LogBuster !
"""
from time import sleep
import colorama
from cli.afficheur_cli import AfficheurCLI
from cli.parseur_arguments_cli import ParseurArgumentsCLI, ArgumentCLIException
from parse.parseur_log_apache import ParseurLogApache, FormatLogApacheInvalideException
from analyse.analyseur_log_apache import AnalyseurLogApache
from export.exporteur import Exporteur, ExportationException


def main():
    """
    Point d'entrée de l'application.
    """
    afficheur_cli = AfficheurCLI()
    afficheur_cli.affiche_message("Who ya gonna call? LogBuster!")
    try:
        afficheur_cli.lance_animation_chargement()
        # Récupération des arguments
        parseur_cli = ParseurArgumentsCLI()
        arguments_cli = parseur_cli.parse_args()
        # Analyse syntaxique du fichier log
        parseur_log = ParseurLogApache(arguments_cli.chemin_log)
        fichier_log = parseur_log.parse_fichier()
        # Analyse statistique du fichier log
        analyseur_log = AnalyseurLogApache(fichier_log)
        analyse = analyseur_log.get_analyse_complete()
        # Exportation de l'analyse
        exporteur = Exporteur(arguments_cli.sortie)
        exporteur.export_vers_json(analyse)
        afficheur_cli.stop_animation_chargement()
    except Exception as ex:
        gestion_exception(afficheur_cli, ex)

def gestion_exception(afficheur_cli, exception):
    """
    Gère les erreurs qui demandent une fin du programme.
    Affiche également un message d'erreur personnalisé en fonction
    de l'exception.

    Args:
        afficheur_cli (AfficheurCLI): L'objet permettant d'intéragir avec la ligne
            de commande.
        exception (Exception): L'exception qui s'est produite.

    Returns:
        None
    """
    erreurs = {
        ArgumentCLIException: "Erreur dans les arguments fournis !",
        FileNotFoundError: "Erreur dans la recherche du log Apache !",
        FormatLogApacheInvalideException: "Erreur dans l'analyse du log Apache !",
        ExportationException: "Erreur dans l'exportation de l'analyse !"
    }
    message = erreurs.get(type(exception), "Erreur interne !")
    afficheur_cli.stop_animation_chargement(True)
    afficheur_cli.affiche_erreur(message, exception)

if __name__ == "__main__":
    main()
