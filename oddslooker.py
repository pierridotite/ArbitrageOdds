from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm  # Barre de progression
import time
import re

# URL de base
BASE_URL = "https://www.oddsportal.com"

# Liste des URL cibles
target_urls = [
    "/football/europe/",
    "/football/france/",
    "/football/england/",
    "/football/germany/",
    "/football/italy/",
    "/football/spain/",
    "/football/portugal/",
    "/football/netherlands/",
    "/football/belgium/",
    "/football/russia/",
    "/football/turkey/",
    "/football/ukraine/",
    "/football/greece/",
    "/football/scotland/",
    "/football/austria/",
]

# Configurer Selenium WebDriver
driver = webdriver.Chrome()  # Remplacez par le driver correspondant à votre navigateur

# Fonction pour attendre les éléments visibles
def wait_for_element(xpath, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        print(f"Element not found: {xpath}")
        return None

# Fonction pour récupérer les liens des leagues
def get_leagues(target_url):
    url = BASE_URL + target_url
    driver.get(url)
    time.sleep(1)  # Attendre que la page charge complètement
    links = driver.find_elements(By.XPATH, "//a[contains(@href, '/football/')]")
    leagues = list(set(link.get_attribute("href") for link in links))
    return leagues

# Fonction pour filtrer les liens de matchs
def filter_match_links(links):
    match_pattern = re.compile(r"^https://www.oddsportal.com/football/.+/[a-z0-9\-]+-[A-Za-z0-9]{8}/$")
    return [link for link in links if match_pattern.match(link)]

# Fichier de sortie
output_file = "list_of_matches.txt"

# Ensemble pour éviter les doublons
unique_match_links = set()

# Ouvrir une barre de progression pour les cibles
with tqdm(total=len(target_urls), desc="Processing target URLs", unit="target") as target_pbar:
    for target_url in target_urls:
        print(f"Fetching leagues for {target_url}...")
        leagues = get_leagues(target_url)

        if not leagues:
            target_pbar.update(1)
            continue

        print(f"Leagues found: {len(leagues)}")

        # Barre de progression pour les leagues
        with tqdm(total=len(leagues), desc=f"Fetching matches in {target_url}", unit="league") as league_pbar:
            for league in leagues:
                print(f"Fetching matches for league: {league}")
                driver.get(league)
                time.sleep(1)

                # Extraire les liens des matchs
                links = driver.find_elements(By.XPATH, "//a[contains(@href, '/football/')]")
                match_links = filter_match_links([link.get_attribute("href") for link in links])

                print(f"Matches found: {len(match_links)}")

                # Ajouter les liens uniques au set
                unique_match_links.update(match_links)

                league_pbar.update(1)  # Mettre à jour la barre pour les leagues

        target_pbar.update(1)  # Mettre à jour la barre pour les cibles

# Enregistrer les liens uniques dans le fichier
with open(output_file, "w", encoding="utf-8") as file:
    for match_link in unique_match_links:
        file.write(match_link + "\n")

# Fermer le navigateur
driver.quit()
print(f"All unique match links have been saved to {output_file}")
