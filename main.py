from selenium.webdriver.common.keys import Keys
from parsel import Selector
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import numpy as np
import json

with open("data.json", "w") as f:
    json.dump([], f)


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
sleep(0.5)

driver.get('https://www.linkedin.com')
sleep(2)

driver.find_element(
    By.XPATH, '//a[@class="nav__button-secondary btn-md btn-secondary-emphasis"]').click()
sleep(2)

username_input = driver.find_element(By.XPATH, '//input[@name="session_key"]')
username_input.send_keys('your mail id')
sleep(2)

password_input = driver.find_element(By.ID, 'password')
password_input.send_keys('your linkedin password')
sleep(2)

driver.find_element(By.XPATH, '//div/button[text()="Sign in"]').click()
sleep(2)

search_input = driver.find_element(By.XPATH, '//input[@placeholder="Search"]')
sleep(1)

search_input.send_keys('software engineer')
search_input.send_keys(Keys.RETURN)
sleep(8)

driver.find_element(By.XPATH, '//button[text() = "People"]').click()
sleep(8)

driver.find_element(By.XPATH, '//button[text() = "Locations"]').click()
sleep(8)
location_input = driver.find_element(
    By.XPATH, '//input[@placeholder = "Add a location"]')
location_input.send_keys('United States')
location_input.send_keys(Keys.RETURN)
sleep(4)

driver.find_element(By.XPATH, '//span[text()="United States"]').click()
sleep(4)

driver.find_elements(
    By.XPATH, '//*[@aria-label="Apply current filter to show results"]')[1].click()
sleep(4)
pages = 0

while True:

    def write_json(new_data, filename='data.json'):
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data.append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    pages = pages + 1
    starting_url = driver.current_url

    profiles = driver.find_elements(
        By.XPATH, '//div[@class="display-flex"]/span/span/a')
    profiles = [profile.get_attribute('href') for profile in profiles]
    for profile in profiles:
        driver.get(profile)
        sleep(4)
        sel = Selector(text=driver.page_source)

        name = sel.xpath(
            '//title/text()').extract_first().split(' | ')[0].split(') ')[1]
        current_company = sel.xpath(
            '//a[@href = "#experience"]/h2/div/text()').extract_first()
        job_title = sel.xpath(
            '//*[@class="text-body-medium break-words"]/text()').extract_first()

        sleep(4)

        secondary_links = driver.find_elements(
            By.XPATH, '//div[contains (@class, "pvs-list__footer-wrapper")]/div/a')  
        secondary_links = [link.get_attribute(
            'href') for link in secondary_links]  

        for link in secondary_links:
            if 'education' in link: 
                driver.get(link)
                sleep(3)

                sel = Selector(driver.page_source)
                education = sel.xpath(
                    '//span[contains(@class, "mr1 hoverable-link-text t-bold")]/span[1]/text()').extract()
                education = np.array(education)
                education = np.unique(education).tolist()
                sleep(3)

                driver.find_element(
                    By.XPATH, '//*[@aria-label="Back to the main profile page"]').click()
                sleep(3)

            else:
                sel = Selector(driver.page_source)
                education = sel.xpath(
                    '//span[contains(text(), "Education")]//following::div[1]/ul/li/div//child::span[contains(@class, "mr1 hoverable-link-text t-bold")]/span[1]/text()').extract()
                sleep(3)

            if 'skills' in link:
                driver.get(link)
                sleep(3)

                sel = Selector(driver.page_source)
                all_skills = sel.xpath(
                    '//span[contains(@class, "mr1 t-bold")]/span[1]/text()').extract()
                skills = np.array(all_skills)
                skills = np.unique(skills).tolist()
                sleep(4)

                driver.find_element(
                    By.XPATH, '//*[@aria-label="Back to the main profile page"]').click()
                sleep(2)

            else:
                sel = Selector(driver.page_source)
                skills = sel.xpath(
                    '//*[contains(text(), "Skills")][1]//following::div[1]//child::span[contains(@class, "mr1 t-bold")]/span[1]/text()').extract()
                sleep(3)

            # experience
            if 'experience' in link:
                driver.get(link)
                sleep(3)

                sel = Selector(driver.page_source)
                former_companies = sel.xpath(
                    '//span[@class="t-14 t-normal"]//child::span[1]/text()').extract()
                sleep(3)

                driver.find_element(
                    By.XPATH, '//*[@aria-label="Back to the main profile page"]').click()
                sleep(3)

            else:
                sel = Selector(driver.page_source)
                companies = sel.xpath(
                    '//span[contains(text(), "Full-time")]/text()')
                for company in companies:
                    former_companies = company.extract().split()[0]
                    sleep(3)
                    if former_companies == "Full-time":
                        sel = Selector(driver.page_source)
                        former_companies = sel.xpath(
                            '//a[@data-field="experience_company_logo"]//child::span[@class="mr1 hoverable-link-text t-bold"]/span[1]/text()')[1:].extract()
                    else:
                        former_companies = company.extract().split()[0]
        print('\n')
        print(name)
        print(current_company)
        print(former_companies)
        print(job_title)
        print(skills)
        print(education)
        print('\n')

        write_json({'name': name, 'current_company': current_company, 'former_companies': former_companies,
                    'job_title': job_title, 'skills': skills, 'education': education})

    driver.get(starting_url)

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    sleep(7)

    next_page = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
    next_page.click()
    sleep(6)
    if pages == 100:  
        break

else:
    driver.quit()
