from scraper.scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper(
        driver_path=r'C:\Users\Hecto\OneDrive\Desktop\chromedriver-win64\chromedriver.exe',
        actions_file='actions/eBay_instructions.json'
    )
    scraper.setup_driver()
    scraper.execute_actions()
    scraper.quit()
