"""
Module des tests unitaires pour le point d'entrée de l'application.
"""

import pytest
from main import main
from cli.parseur_arguments_cli import ArgumentCLIException
from parse.parseur_log_apache import FormatLogApacheInvalideException
from export.exporteur import ExportationException


@pytest.mark.parametrize(
    "exception",
    [
        (ArgumentCLIException),
        (FormatLogApacheInvalideException),
        (ExportationException),
        (TypeError),
        (ValueError),
    ],
)
def test_main_gestion_exception(mocker, exception):
    """
    Vérifie que les exceptions attendues sont interceptées dans fichier principal.

    Scénarios testés:
        - Vérification que les exceptions n'arrête pas le programme.

    Args:
        mocker (MockerFixture): Une fixture pour simuler des exceptions.
        exception (any): L'exception à simuler.
    """
    mocker.patch("main.ParseurArgumentsCLI", side_effect=exception)
    main()


def test_main_succes(mocker):
    """
    Vérifie le fonctionnement du fichier principal sans exception.

    Scénarios testés:
        - Vérification que le fichier principal s'execute sans exception lors
            d'un déroulement normal.

    Args:
        mocker (MockerFixture): Une fixture pour simuler des retours pour les classes
            et méthodes dans main.
    """
    # Mock des classes pour simuler un fonctionnement correct
    mock_parseur_cli = mocker.patch("main.ParseurArgumentsCLI")
    mock_parseur_cli.return_value.parse_args.return_value = mocker.MagicMock(
        chemin_log="test.log"
    )

    mocker.patch("main.FiltreLogApache")

    mock_parseur_log = mocker.patch("main.ParseurLogApache")
    mock_parseur_log.return_value.parse_fichier.return_value = mocker.MagicMock()

    mock_analyseur_log = mocker.patch("main.AnalyseurLogApache")
    mock_analyseur_log.return_value.get_analyse_complete.return_value = {
        "chemin": "test.log"
    }

    mocker.patch("main.Exporteur")

    # Vérifie qu'aucune exception n'est levée
    try:
        main()
    except Exception:
        pytest.fail("Aucune exception ne doit être levée ici")
