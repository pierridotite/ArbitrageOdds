# README

## Project Overview
Ce projet vise à extraire des cotes de matchs de football et à analyser les opportunités d'arbitrage. Les outils utilisés comprennent Selenium pour le scraping web, Python pour l'analyse des données et des fichiers texte pour stocker les résultats.

### Structure des fichiers

- **oddslooker.py** :
  - Script principal pour extraire les liens des matchs depuis [OddsPortal](https://www.oddsportal.com).
  - Utilise Selenium pour parcourir les pages de différentes ligues et récupérer les URLs des matchs pertinents.
  - Les résultats sont enregistrés dans `list_of_matches.txt`.

- **souptest.py** :
  - Analyse les matchs listés dans `list_of_matches.txt`.
  - Extrait les cotes, vérifie si les matchs sont passés et identifie les opportunités d'arbitrage.
  - Les opportunités sont enregistrées dans `arbitrage_opportunities.txt` avec les détails des bookmakers et marges de profit potentielles.

- **list_of_matches.txt** :
  - Contient les URLs des matchs extraits par `oddslooker.py`.
  - Chaque ligne représente un match différent.

- **arbitrage_opportunities.txt** :
  - Contient les opportunités d'arbitrage identifiées par `souptest.py`.
  - Les informations incluent les cotes optimales, les bookmakers correspondants et la marge de profit potentielle.

### Prérequis

1. **Python 3.x**
2. **Selenium WebDriver** pour le navigateur choisi (par défaut Chrome).
3. Bibliothèques Python :
   - `selenium`
   - `tqdm`

### Installation

1. Clonez ce dépôt :
   ```bash
   git clone <URL_DU_DEPOT>
   cd <NOM_DU_DEPOT>
   ```
2. Installez les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```
3. Téléchargez et configurez [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).

### Utilisation

#### Étape 1 : Extraction des liens de matchs

Exécutez `oddslooker.py` pour récupérer les liens des matchs :
```bash
python oddslooker.py
```
Les liens seront enregistrés dans `list_of_matches.txt`.

#### Étape 2 : Analyse des opportunités d'arbitrage

Exécutez `souptest.py` pour analyser les matchs et détecter les opportunités :
```bash
python souptest.py
```
Les opportunités seront enregistrées dans `arbitrage_opportunities.txt`.

### Résultats

Les résultats incluent :
- La liste des liens des matchs dans `list_of_matches.txt`.
- Les opportunités d'arbitrage dans `arbitrage_opportunities.txt`, comprenant les cotes optimales, les bookmakers, et les marges de profit potentielles.

### Contributions

1. Forkez ce dépôt.
2. Créez une branche pour vos modifications :
   ```bash
   git checkout -b feature/new-feature
   ```
3. Soumettez une pull request.

### Avertissements

- Les opportunités d'arbitrage sont sensibles au temps ; les cotes peuvent changer rapidement.
- Veuillez vérifier les lois et réglementations locales avant d'utiliser des outils d'arbitrage.

### Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

