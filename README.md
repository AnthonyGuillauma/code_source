# LogBuster

```
                                  .-. .-')                 .-')    .-') _     ('-.  _  .-')  ,---.
                                  \  ( OO )               ( OO ). (  OO) )  _(  OO)( \( -O ) |   |
 ,--.      .-'),-----.   ,----.    ;-----.\  ,--. ,--.   (_)---\_)/     '._(,------.,------. |   |
 |  |.-') ( OO'  .-.  ' '  .-./-') | .-.  |  |  | |  |   /    _ | |'--...__)|  .---'|   /`. '|   |
 |  | OO )/   |  | |  | |  |_( O- )| '-' /_) |  | | .-') \  :` `. '--.  .--'|  |    |  /  | ||   |
 |  |`-' |\_) |  |\|  | |  | .--, \| .-. `.  |  |_|( OO ) '..`''.)   |  |  (|  '--. |  |_.' ||  .'
(|  '---.'  \ |  | |  |(|  | '. (_/| |  \  | |  | | `-' /.-._)   \   |  |   |  .--' |  .  '.'`--' 
 |      |    `'  '-'  ' |  '--'  | | '--'  /('  '-'(_.-' \       /   |  |   |  `---.|  |\  \ .--. 
 `------'      `-----'   `------'  `------'   `-----'     `-----'    `--'   `------'`--' '--''--' 
```

Bienvenue dans le monde de LogBuster, l'outil ultime pour analyser, décortiquer et sauver vos logs Apache des griffes du chaos. Vous avez des logs qui traînent, qui sont indéchiffrables ou tout simplement encombrants ? Pas de panique, LogBuster est là pour les attraper, les analyser et vous offrir des statistiques claires et précises, comme jamais auparavant !

## 📋 Table des matières

- [👻 Fonctionnalités](#-fonctionnalités)
- [📦 Installation](#-installation)
- [🛠️ Utilisation de base](#️-utilisation-de-base)
- [📖 Documentation](#-documentation)
- [🧪 Lancer les tests](#-lancer-les-tests)
- [📜 Licence](#-licence)

## 👻 Fonctionnalités

- 📄 Parsing avancé de logs Apache.
- 📉 Extraire des statistiques clés.
- 🗂️ Ranger les données par catégorie.
- 🧹 Indiquer les erreurs de format avec précision.
- 🚚 Exporter les données en JSON.

## 📦 Installation

### Bash (linux/macOS)
```bash
git clone https://github.com/AnthonyGuillauma/code_source
cd code_source
python -m venv .venv
source .venv/bin/activate  # Activation de l'environnement virtuel sous Bash
pip install -r requirements.txt
```

### Windows (cmd)
```bash
git clone https://github.com/AnthonyGuillauma/code_source
cd code_source
python -m venv .venv
.venv\Scripts\activate  # Activation de l'environnement virtuel sous Windows
pip install -r requirements.txt
```

## 🛠️ Utilisation de base

```
python app/main.py chemin_log [-s SORTIE]
```
- `chemin_log` : Le chemin vers le fichier de log Apache à analyser.
- `-s SORTIE` (optionnel) : Le chemin où sauvegarder les résultats de l'analyse. Si non spécifié, les résultats seront sauvegardés dans un fichier `analyse-log-apache.json`.

## 📖 Documentation

La documentation complète du code du projet se situe [ici](https://anthonyguillauma.github.io/code_source/
).

Si vous souhaitez la générer vous même, suivez ces étapes :

Tout d'abord, placez-vous dans le dossier `docs` qui contient les fichiers sources de la documentation :

```bash
cd docs
```

Puis, générez la documentation via la commande suivante :

```bash
./make html
```

Enfin, ouvrez le fichier html `build/html/index.html` généré dans un navigateur.

## 🧪 Lancer les tests

Les tests unitaires du projet peuvent être exécutés avec pytest. Pour lancer les tests, assurez-vous d'avoir activé l'environnement virtuel et installé les dépendances.

Premièrement, placez-vous dans le dossier `tests` qui contient les fichiers de configuration pour les tests unitaires :

```bash
cd tests
```

Ensuite, exécutez les tests avec la commande suivante :

```bash
pytest
```

Enfin, si vous souhaitez également afficher la couverture des tests unitaires, utilisez la commande suivante :

```bash
pytest  --cov=../app --cov-report=term-missing
```

# 📜 Licence

Ce projet est sous licence MIT.