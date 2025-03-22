"""
Point d'entrée de l'application LogBuster !
"""

import colorama
from cli.parseur_arguments_cli import ParseurArgumentsCLI, ArgumentCLIException


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
        # Analyse statistique du fichier log
        # Exportation de l'analyse
    except ArgumentCLIException as ex:
        print(f"Erreur dans les arguments fournis !\n {ex}")
