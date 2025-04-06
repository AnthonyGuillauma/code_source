.. Documentation de LogBuster

👻 Bienvenue dans la documentation de **LogBuster**
====================================================

**LogBuster** est un outil puissant pour analyser les fichiers de logs Apache.
Grâce à LogBuster, vous pouvez extraire des informations essentielles, gérer des erreurs de format et bien plus encore.

.. code:: text

                                    .-. .-')                 .-')    .-') _     ('-.  _  .-')  ,---.
                                    \  ( OO )               ( OO ). (  OO) )  _(  OO)( \( -O ) |   |
   ,--.      .-'),-----.   ,----.    ;-----.\  ,--. ,--.   (_)---\_)/     '._(,------.,------. |   |
   |  |.-') ( OO'  .-.  ' '  .-./-') | .-.  |  |  | |  |   /    _ | |'--...__)|  .---'|   /`. '|   |
   |  | OO )/   |  | |  | |  |_( O- )| '-' /_) |  | | .-') \  :` `. '--.  .--'|  |    |  /  | ||   |
   |  |`-' |\_) |  |\|  | |  | .--, \| .-. `.  |  |_|( OO ) '..`''.)   |  |  (|  '--. |  |_.' ||  .'
   (|  '---.'  \ |  | |  |(|  | '. (_/| |  \  | |  | | `-' /.-._)   \   |  |   |  .--' |  .  '.'`--' 
   |      |    `'  '-'  ' |  '--'  | | '--'  /('  '-'(_.-' \       /   |  |   |  `---.|  |\  \ .--. 
   `------'      `-----'   `------'  `------'   `-----'     `-----'    `--'   `------'`--' '--''--' 

**(҂-_•)⊃═O Fonctionnalités principales**
-------------------------------------------

- **Extraire des statistiques clés** : Obtenez des données précieuses sur vos fichiers de logs.
- **Exporter les données en JSON** : Accédez à un format structuré pour vos analyses.
- **Exporter des graphiques** : Générez des graphiques de vos fichiers de logs.
- **Filtrer les analyses** : Filtrez les analyses en toute simplicité.
- **Gérer les erreurs de format avec précision** : Identifiez rapidement les anomalies et les erreurs de vos fichiers log.

**d(■᎑■⌐) Utilisation**
---------------------------

```
python app/main.py chemin_log [-s SORTIE] [-i IP] [-c CODE_STATUT_HTTP] [--camembert CAMEMBERT]
```

- `chemin_log` : Le chemin vers le fichier de log Apache à analyser.
- `-s SORTIE` (optionnel) : Le chemin où sauvegarder les résultats de l'analyse. Si non spécifié, les résultats seront sauvegardés dans un fichier `analyse-log-apache.json`.
- `-i IP` (optionnel) : Le filtre à appliquer sur les adresses IP des entrées du fichier de log. Uniquement les entrées avec cette adresse IP seront analysées.
- `-c CODE_STATUT_HTTP` (optionnel) : Le filtre à appliquer sur les code de statut http des entrées du fichier de log. Uniquement les entrées avec ce code de statut http seront analysées.
- `--camembert CAMEMBERT` : (optionnel) : Active la génération de graphiques camemberts dans lors de l'analyse pour les statistiques compatibles. Les statistiques comptatibles.

**(ò_ó)⊃ Format de l'analyse**
--------------------------------

Lors de l'analyse des fichiers de logs, LogBuster fait en sorte de regrouper les statistiques clés par catégories.

Voici ci-dessous le format de l'analyse en JSON:

            - chemin: chemin absolu du fichier
            - total_entrees: nombre total d'entrées dans le fichier
            - filtre: filtres appliqués à l'analyse
               - adresse_ip: filtre sur l'adresse IP (None si désactivé)
               - code_statut_http: filtre sur le code de statut http (None si désactivé)
            - statistiques:
               - total_entrees_filtre: nombre total d'entrées analysées
               - requetes:
                  - top_urls: top 3 des urls
                     - dictionnaires contenant:
                        - url: ressource demandée
                        - total: nombre d'entrée avec cette ressource demandée
                        - taux: pourcentage d'entrée avec cette ressource demandée
               - reponses:
                  - repartition_code_statut_http: répartition des codes de statut http
                     - dictionnaires contenant:
                        - code: code de statut http retourné
                        - total: nombre d'entrée avec ce code de statut http retourné
                        - taux: pourcentage d'entrée avec ce code de statut http retourné

Pour les graphiques camemberts, un fichier HTML est généré avec ce graphique.
Néanmoins, toutes les statistiques ne sont pas compatibles avec ce type d'affichage.

Voici la liste des statistiques comptatibles avec les graphiques:

- `repartition_code_statut_http` : Répartition des codes de statut HTTP. (nom: camembert-code_statut_http)

**(ง'̀᎑'́)ง Format des fichier de log Apache**
------------------------------------------------

Le format de log Apache pris en charge est celui utilisé par le fichier `access.log`.
Ces logs Apache contiennent des informations détaillées sur les requêtes HTTP traitées par le serveur.
Chaque ligne d'un fichier représente une requête individuelle, et les informations sont généralement séparées par des espaces ou des caractères spécifiques.

Format commun (Common Log Format)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un fichier de log Apache standard suit généralement un format similaire au suivant :

``127.0.0.1 - - [10/Oct/2025:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326``

1. **IP de l'utilisateur** (127.0.0.1) : L'adresse IP de l'utilisateur qui a effectué la requête.
2. **Identifiant de l'utilisateur** (vide ici) : L'identifiant de l'utilisateur, souvent vide ou un tiret (`-`).
3. **Identifiant de l'utilisateur authentifié** (vide ici) : Si l'utilisateur est authentifié, cet identifiant sera visible, sinon il sera également vide ou un tiret (`-`).
4. **Date et heure de la requête** ([10/Oct/2025:13:55:36 +0000]) : La date et l'heure précises de la requête, suivies du fuseau horaire.
5. **Requête HTTP** ("GET /index.html HTTP/1.1") : La méthode HTTP utilisée (ici `GET`), l'URL demandée (ici `/index.html`), et la version du protocole HTTP (ici `HTTP/1.1`).
6. **Code de statut HTTP** (200) : Le code de statut retourné par le serveur (ici, `200` indique que la requête a réussi).
7. **Taille de la réponse** (2326) : La taille en octets de la réponse envoyée au client.

Dans LogBuster, l'**IP de l'utilisateur** et la **Date et heure de la requête** sont obligatoires, sinon un message d'erreur est retournée.

Format combiné (Combined Log Format)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le format combiné permet d'ajouter plus de détails sur chaque requête.
Voici un exemple de ligne de log avec ce format :

``127.0.0.1 - - [10/Oct/2025:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326 "http://referrer.com" "Mozilla/5.0"``

Dans ce format, deux informations supplémentaires à la fin de l'entrée sont présentes :

1. **Référent HTTP** ("http://referrer.com") : L'URL de la page depuis laquelle la requête a été faite. Cela peut être vide si la requête provient directement de l'utilisateur sans référence.
2. **Agent utilisateur** ("Mozilla/5.0") : L'agent utilisateur indique quel navigateur ou appareil a effectué la requête.

Assurez-vous que votre fichier de log Apache suit un format cohérent, comme ceux mentionnés ci-dessus, afin d'obtenir des résultats précis et fiables lors de l'utilisation de LogBuster.
Pour plus d'informations, consultez la documentation Apache sur ce lien : https://httpd.apache.org/docs/2.4/fr/logs.html

**(∩x_x) Précautions concernant l'affichage des caractères spéciaux**
----------------------------------------------------------------------

Le projet LogBuster utilise des caractères **Unicode**, tels que des symboles spéciaux, dans le terminal pour rendre l'affichage plus plaisant. Assurez-vous que votre terminal est configuré pour prendre en charge l'affichage de caractères Unicode afin de profiter pleinement de l'expérience utilisateur.

Si vous rencontrez des problèmes d'affichage (comme des symboles manquants ou mal rendus), vous pouvez essayer les solutions suivantes :

- Utiliser un terminal compatible avec Unicode (par exemple, Terminal sous macOS, Windows Terminal sous Windows, ou des terminaux comme GNOME Terminal ou Konsole sous Linux).
- Vérifier que votre terminal utilise une police qui prend en charge les caractères Unicode (par exemple, DejaVu Sans Mono ou Consolas).

**ε＝(( ꐑº-° )ꐑ Documentation du projet**
-------------------------------------------

Consultez les différentes sections pour en savoir plus sur le projet **LogBuster** :

.. toctree::
   :maxdepth: 4
   :caption: Contenu
   :numbered:

   modules/index_modules.rst

---

© 2025 - Projet LogBuster
