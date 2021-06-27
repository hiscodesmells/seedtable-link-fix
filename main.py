from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome("./chromedriver", options=options)

STARTUPS_URL = "https://www.seedtable.com/european-startup-rankings?locale=en"

driver.get(STARTUPS_URL)
city_urls = {element.get_attribute("href") for element in
             driver.find_elements_by_xpath("//a[contains(@href, 'startups-')]")}


class Item:
    def __init__(self, company, city, broken_url):
        self.city = city
        self.company = company
        self.broken_url = broken_url


items = []
for url in city_urls:
    print(f'Scanning startups in - {url.split("-")[-1]}')
    driver.get(url)
    elements = driver.find_elements_by_xpath("//a[contains(@href, 'https://https')]")
    for element in elements:
        items.append(Item(
            element.text,
            url.split("-")[-1],
            element.get_attribute("href")
        ))

with open("broken-links.txt", 'w') as file:
    for item in items:
        file.write('Company: ' + item.company + ', City: ' + item.city + ', Broken Link: ' + item.broken_url + '\n\n')
