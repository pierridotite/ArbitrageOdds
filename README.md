# README

## Project Overview
This project aims to extract football match odds and analyze arbitrage opportunities. The tools used include Selenium for web scraping, Python for data analysis, and text files for storing results.

### File Structure

- **oddslooker.py**:
  - Main script to extract match links from [OddsPortal](https://www.oddsportal.com).
  - Uses Selenium to navigate league pages and retrieve relevant match URLs.
  - Results are saved in `list_of_matches.txt`.

- **souptest.py**:
  - Analyzes the matches listed in `list_of_matches.txt`.
  - Extracts odds, checks if matches are in the past, and identifies arbitrage opportunities.
  - Opportunities are recorded in `arbitrage_opportunities.txt` with details of bookmakers and potential profit margins.

- **list_of_matches.txt**:
  - Contains URLs of matches extracted by `oddslooker.py`.
  - Each line represents a different match.

- **arbitrage_opportunities.txt**:
  - Contains arbitrage opportunities identified by `souptest.py`.
  - Information includes optimal odds, corresponding bookmakers, and potential profit margins.

### Prerequisites

1. **Python 3.x**
2. **Selenium WebDriver** for the chosen browser (default is Chrome).
3. Python Libraries:
   - `selenium`
   - `tqdm`

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/pierridotite/ArbitrageOdds
   cd ArbitrageOdds
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download and configure [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/).

### Usage

#### Step 1: Extract Match Links

Run `oddslooker.py` to retrieve match links:
```bash
python oddslooker.py
```
Links will be saved in `list_of_matches.txt`.

#### Step 2: Analyze Arbitrage Opportunities

Run `souptest.py` to analyze matches and detect opportunities:
```bash
python souptest.py
```
Opportunities will be saved in `arbitrage_opportunities.txt`.

### Results

#### Example Output

- **list_of_matches.txt**:
  ```
  https://www.oddsportal.com/football/england/premier-league/nottingham-tottenham-dIMJtCwI/
  https://www.oddsportal.com/football/italy/serie-a/ac-milan-as-roma-foxKCMGU/
  https://www.oddsportal.com/football/france/ligue-1/lille-nantes-vgbyE4S6/
  ```

- **arbitrage_opportunities.txt**:
  ```
  Arbitrage opportunity for the match: https://www.oddsportal.com/football/italy/serie-a/ac-milan-as-roma-foxKCMGU/
    Date: 29 Dec 2024, 20:45
    1: 2.05 at 1xBet
    X: 3.79 at 1xBet
    2: 4.2 at Unibet
    Sum of inverses: 0.9898
    Potential profit margin: 1.04%
  
  Arbitrage opportunity for the match: https://www.oddsportal.com/football/england/premier-league/nottingham-tottenham-dIMJtCwI/
    Date: 26 Dec 2024, 16:00
    1: 2.55 at Unibet
    X: 4.04 at 1xBet
    2: 2.85 at bet-at-home
    Sum of inverses: 0.9906
    Potential profit margin: 0.95%
  ```

### Contributions

1. Fork this repository.
2. Create a branch for your changes:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Submit a pull request.

### Warnings

- Arbitrage opportunities are time-sensitive; odds can change quickly.
- Please verify local laws and regulations before using arbitrage tools.

### License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
