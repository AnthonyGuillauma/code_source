"""
Point d'entrée de l'application LogBuster !
"""

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
    colorama.init()
    a = AfficheurCLI()
    try:
        a.affiche_message("Who ya gonna call? LogBuster!")
        a.lance_animation_chargement()
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
        a.stop_animation_chargement()
    except ArgumentCLIException as ex:
        print(f"Erreur dans les arguments fournis !\n {ex}")
    except FileNotFoundError as ex:
        print(f"Erreur dans la recherche du log Apache !\n{ex}")
    except FormatLogApacheInvalideException as ex:
        print(f"Erreur dans l'analyse du log Apache !\n{ex}")
    except ExportationException as ex:
        print(f"Erreur dans l'exportation de l'analyse !\n{ex}")
    except Exception as ex:
        print(f"Erreur interne !\n{ex}")


if __name__ == "__main__":
    main()
