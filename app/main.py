"""
Point d'entrée de l'application LogBuster !
"""

import colorama
from cli.parseur_arguments_cli import ParseurArgumentsCLI, ArgumentCLIException
from parse.parseur_log_apache import ParseurLogApache, FormatLogApacheInvalideException
from analyse.analyseur_log_apache import AnalyseurLogApache


if __name__ == "__main__":
    colorama.init()
    print(colorama.Style.DIM + r"""
                                  .-. .-')                 .-')    .-') _     ('-.  _  .-')  ,---.
                                  \  ( OO )               ( OO ). (  OO) )  _(  OO)( \( -O ) |   |
 ,--.      .-'),-----.   ,----.    ;-----.\  ,--. ,--.   (_)---\_)/     '._(,------.,------. |   |
 |  |.-') ( OO'  .-.  ' '  .-./-') | .-.  |  |  | |  |   /    _ | |'--...__)|  .---'|   /`. '|   |
 |  | OO )/   |  | |  | |  |_( O- )| '-' /_) |  | | .-') \  :` `. '--.  .--'|  |    |  /  | ||   |
 |  |`-' |\_) |  |\|  | |  | .--, \| .-. `.  |  |_|( OO ) '..`''.)   |  |  (|  '--. |  |_.' ||  .'
(|  '---.'  \ |  | |  |(|  | '. (_/| |  \  | |  | | `-' /.-._)   \   |  |   |  .--' |  .  '.'`--' 
 |      |    `'  '-'  ' |  '--'  | | '--'  /('  '-'(_.-' \       /   |  |   |  `---.|  |\  \ .--. 
 `------'      `-----'   `------'  `------'   `-----'     `-----'    `--'   `------'`--' '--''--' 
            
          """)
    try:
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
    except ArgumentCLIException as ex:
        print(f"Erreur dans les arguments fournis !\n {ex}")
    except FileNotFoundError as ex:
        print(f"Erreur dans la recherche du log Apache !\n{ex}")
    except FormatLogApacheInvalideException as ex:
        print(f"Erreur dans l'analyse du log Apache !\n{ex}")
    except Exception as ex:
        print(f"Erreur interne !\n{ex}")
