import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm  # Pour la barre de progression

# Configuration du WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Exécuter en mode sans interface graphique
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")  # Ajuste la taille de la fenêtre pour gagner en performance

# Initialiser un seul WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Fonction pour vérifier si le match est passé
def is_match_past(match_date_str):
    try:
        # Nettoyer la chaîne de caractères en remplaçant les doubles espaces par un seul
        match_date_str = ' '.join(match_date_str.split())  # Remplacer les espaces multiples par un seul

        # Parser la date avec le bon format
        match_date = datetime.strptime(match_date_str, "%d %b %Y, %H:%M")
        current_date = datetime.now()

        # Vérifier si la date du match est passée
        return match_date < current_date
    except Exception as e:
        print(f"Erreur de parsing de la date : {e}")
        return False


# Fonction pour extraire les cotes et la date d'un match
def extract_odds_and_date(url):
    driver.get(url)
    print(f"Traitement de l'URL: {url}")  # Afficher l'URL en cours de traitement

    # Attendre que la table des cotes soit chargée
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex.h-9.border-b.border-l.border-r.text-xs"))
    )

    # Extraire la date du match
    try:
        date_elements = driver.find_elements(By.CSS_SELECTOR, ".text-gray-dark.font-main.item-center.flex.gap-1.text-xs.font-normal p")
        date_text = " ".join([element.text.strip() for element in date_elements if element.text.strip()])
        date_text = date_text.split(",")[-2:]  # Prendre juste la date et l'heure
        date_text = ", ".join(date_text).strip()

        if is_match_past(date_text):
            print(f"Le match pour {url} est déjà passé. Ignoré.")
            return None, None  # Ignorer les matchs passés
    except Exception as e:
        print(f"Erreur lors de l'extraction de la date pour {url}: {e}")
        return None, None

    # Trouver les lignes des cotes
    odds_rows = driver.find_elements(By.CSS_SELECTOR, "div.flex.h-9.border-b.border-l.border-r.text-xs")
    odds_data = []

    # Liste pour stocker les bookmakers avec fond jaune
    yellow_bookmakers = []

    for row in odds_rows:
        try:
            bookmaker_element = row.find_element(By.CSS_SELECTOR, "p.height-content")
            bookmaker_name = bookmaker_element.text.strip()
        except:
            bookmaker_name = "Unknown"

        if bookmaker_name in ["Payout", "Average", "Highest", "My coupon"]:
            continue

        # Vérifier si le bookmaker a un fond jaune
        yellow_odds_elements = row.find_elements(By.XPATH, ".//div[contains(@class, 'bg-[#ffcf0d]')]")
        if yellow_odds_elements:
            yellow_bookmakers.append(bookmaker_name)

        # Trouver les cotes ("1", "X", "2")
        odds_elements = row.find_elements(By.CSS_SELECTOR, "div.flex-center.flex-col.font-bold")
        extracted_odds = [odd.text.strip() for odd in odds_elements if odd.text.strip()]

        if len(extracted_odds) == 3:  # Vérifier qu'il y a 3 cotes
            odds_data.append({
                "bookmaker": bookmaker_name,
                "odds": extracted_odds
            })

    # Ne conserver que les bookmakers avec fond jaune dans les cotes
    yellow_odds_data = [entry for entry in odds_data if entry["bookmaker"] in yellow_bookmakers]

    print(f"Extraction réussie pour {url}")
    return date_text, yellow_odds_data


# Fonction pour trouver des opportunités d'arbitrage
def find_arbitrage_opportunities(odds_data):
    # Dictionnaires pour stocker les meilleures cotes pour chaque issue et leur(s) bookmaker(s)
    best_odds = {"1": {"value": 0, "bookmakers": []}, "X": {"value": 0, "bookmakers": []}, "2": {"value": 0, "bookmakers": []}}

    # Parcourir les données des bookmakers et trouver les meilleures cotes pour chaque issue
    for entry in odds_data:
        bookmaker = entry["bookmaker"]
        odds = entry["odds"]
        for i, outcome in enumerate(["1", "X", "2"]):
            # Si la cote actuelle est plus élevée que la précédente, on la remplace
            if float(odds[i]) > best_odds[outcome]["value"]:
                best_odds[outcome]["value"] = float(odds[i])
                best_odds[outcome]["bookmakers"] = [bookmaker]  # Remplacer la liste des bookmakers
            elif float(odds[i]) == best_odds[outcome]["value"]:
                best_odds[outcome]["bookmakers"].append(bookmaker)  # Ajouter le bookmaker à la liste

    print(f"Meilleures cotes trouvées : {best_odds}")

    # Calcul de la somme des inverses des cotes pour chaque issue
    sum_inverses = sum(1 / odd["value"] for odd in best_odds.values())
    print(f"Somme des inverses : {sum_inverses:.4f}")

    arbitrage_matches = []
    if sum_inverses < 1:  # Opportunité d'arbitrage trouvée
        profit_margin = (1 / sum_inverses) - 1  # Calcul de la marge bénéficiaire

        arbitrage_matches.append({
            "best_odds": best_odds,
            "sum_inverses": sum_inverses,
            "profit_margin (%)": round(profit_margin * 100, 2)
        })

    return arbitrage_matches


# Fonction pour afficher les opportunités d'arbitrage et enregistrer les résultats
def display_arbitrage_live(arbitrage_matches, match_date, match_url, output_file):
    for match in arbitrage_matches:
        best_odds = match["best_odds"]
        sum_inverses = match["sum_inverses"]
        profit_margin = match["profit_margin (%)"]

        # Affichage immédiat des opportunités d'arbitrage dans la console
        print(f"\nOpportunité d'arbitrage pour le match : {match_url}")
        print(f"  Date : {match_date}")
        for outcome, odds_info in best_odds.items():
            bookmakers = ", ".join(odds_info["bookmakers"])
            print(f"  {outcome}: {odds_info['value']} chez {bookmakers}")
        print(f"  Somme des inverses : {sum_inverses:.4f}")
        print(f"  Marge de profit potentielle : {profit_margin}%")

        # Enregistrer directement dans le fichier trié
        with open(output_file, 'a') as f:  # Ouvrir en mode 'a' pour ajouter
            f.write(f"\nOpportunité d'arbitrage pour le match : {match_url}\n")
            f.write(f"  Date : {match_date}\n")
            for outcome, odds_info in best_odds.items():
                bookmakers = ", ".join(odds_info["bookmakers"])
                f.write(f"  {outcome}: {odds_info['value']} chez {bookmakers}\n")
            f.write(f"  Somme des inverses : {sum_inverses:.4f}\n")
            f.write(f"  Marge de profit potentielle : {profit_margin}%\n")


# Fonction principale pour analyser les matchs depuis un fichier d'entrées
# Fonction principale pour analyser les matchs depuis un fichier d'entrées
# Fonction principale pour analyser les matchs depuis un fichier d'entrées
def analyze_matches(input_file, output_file):
    results = []

    with open(input_file, 'r') as f:
        urls = f.readlines()

    # Utilisation de tqdm pour afficher une barre de progression
    for url in tqdm(urls, desc="Traitement des matchs", unit="match"):
        url = url.strip()
        if not url:
            continue

        try:
            match_date, odds_data = extract_odds_and_date(url)
            if match_date and odds_data:
                arbitrage_matches_for_match = find_arbitrage_opportunities(odds_data)

                # Ajouter la date et l'URL au résultat
                for match in arbitrage_matches_for_match:
                    match["date"] = match_date  # Ajouter la date ici
                    match["match_url"] = url  # Ajouter l'URL ici
                    results.append(match)

                # Afficher et enregistrer les résultats au fur et à mesure
                display_arbitrage_live(arbitrage_matches_for_match, match_date, url, output_file)
            else:
                print(f"URL ignorée (problème d'extraction) : {url}")
        except Exception as e:
            print(f"Erreur lors du traitement de {url}: {e}")

    # Avant de trier, vérifier que chaque match contient bien l'URL
    print(f"\nAvant de trier, voici un exemple de résultats :")
    print(results[0] if results else "Aucun résultat")

    # Trier les résultats par date (assurez-vous que la date est bien formatée avant)
    results.sort(key=lambda x: datetime.strptime(x["date"], "%d %b %Y, %H:%M"))

    # Réenregistrer les résultats triés
    with open(output_file, 'w') as f:
        f.write("Résultats des opportunités d'arbitrage triés :\n")
        for result in results:
            best_odds = result["best_odds"]
            sum_inverses = result["sum_inverses"]
            profit_margin = result["profit_margin (%)"]
            match_url = result.get("match_url", "URL inconnue")

            f.write(f"\nOpportunité d'arbitrage pour le match : {match_url}\n")
            f.write(f"  Date : {result['date']}\n")
            for outcome, odds_info in best_odds.items():
                bookmakers = ", ".join(odds_info["bookmakers"])
                f.write(f"  {outcome}: {odds_info['value']} chez {bookmakers}\n")
            f.write(f"  Somme des inverses : {sum_inverses:.4f}\n")
            f.write(f"  Marge de profit potentielle : {profit_margin}%\n")

    print(f"\nAnalyse terminée. Les résultats ont été enregistrés dans '{output_file}'.")


# Exemple d'utilisation
input_file = "list_of_matches.txt"  # Remplacez par le chemin vers votre fichier d'entrées avec les URL
output_file = "arbitrage_opportunities.txt"  # Remplacez par le chemin vers le fichier de sortie

start_time = time.time()  # Démarrer le chronométrage
analyze_matches(input_file, output_file)
end_time = time.time()  # Fin du chronométrage

print(f"\nAnalyse terminée en {end_time - start_time:.2f} secondes.")
