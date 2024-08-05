import json
from scraper.scraper import Scraper

def main():
    driver_path = r'C:\Users\Hecto\OneDrive\Desktop\chromedriver-win64\chromedriver.exe'
    
    # Configura el JSON para INEGI
    inegi_actions_file = 'actions/actions_inegi.json'
    scraper = Scraper(driver_path, inegi_actions_file)
    
    scraper.setup_driver()
    scraper.execute_actions()
    scraper.quit()

if __name__ == "__main__":
    main()
