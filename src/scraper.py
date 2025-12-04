from flask import flash, redirect
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from util import InvalidURLError, validate_url

def scrape_acm(url: str):
    try:
        validate_url(url)

        headers = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7444.175 Safari/537.36'
        options = Options()
        #options.add_argument('--headless=new')
        options.add_argument(f'user-agent={headers}')

        driver = webdriver.Chrome(options)
        driver.get(url)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'core-container'))
        )

        cookie_button = driver.find_element(By.ID, 'CybotCookiebotDialogBodyButtonDecline')
        cookie_button.click()

        button = driver.find_element(By.CSS_SELECTOR, 'button[data-title="Export Citation"]')
        button.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'csl-right-inline'))
        )

        soup = bs(driver.page_source, 'lxml')
        
        info = soup.find('div', {'class': 'csl-right-inline'})
        # ref_type = None
        # year = core.find('span', {'class': 'core-date-published'}).text
        # title = core.find('h1', {'property': 'name'}).text
        # authors = core.find('')

        driver.quit()
        return info

    except InvalidURLError as e:
        flash(str(e))
        return redirect("/new_ref")

    # except Exception:
    #     flash("An unexpected error happened, please try again.")
    #     return redirect("/new_ref")
    
print(scrape_acm("https://dl.acm.org/doi/10.1145/2380552.2380613"))
