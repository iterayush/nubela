# Tutorial - How to build your own LinkedIn Profile Scraper in 2022

A Selenium LinkedIn scraper that loops through multiple pages and collects profile data.

## What you can use for?

We  can use this to get details from LinkedIn profiles of specific group of people e.g. details of people working as _'Software Engineer'_.

## Getting Started
LinkedIn is one of the largest platform for the professionals. You can reach to people here with similar skills, jobs etc. All the information can be accessed by hand easily here. But if we want to collect profile data on larger scale, then what? We use scraper for this purpose.  
In this article, we are going to build our own LinkedIn scraper.  
For this we need to have **[ Python ]( https://www.python.org)** & **[ChromeDriver](https://chromedriver.chromium.org/downloads)** in our system.  
While downloading **ChromeDriver**, we must _take care_ of our chrome version. Check your current chrome browser version and download ChromeDriver according to it.  
We will use *Selenium, Webdriver, Selector from parsel, numpy and json(to collect the data).  
  
After the environment setup, open the Python IDLE and import the following:
```python
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import numpy as np
import json
```

##### We have to create a .json file to collect our data, the process is as follows:
```python
with open("data.json", "w") as f:
    json.dump([], f)
 ```
#### Now our next step is to sign in into LinkedIn. For this we will use webdriver and automate this process.  
```python
# open webdriver.
driver = webdriver.Chrome(ChromeDriveManager().install())
driver.maximize_window() #to maximize the chrome window.
sleep(0.5)
# to open linkedin
driver.get('https://www.linkedin.com')
sleep(2)
# clicking on the signin button to input email id and password.
driver.find_element(By.XPATH,'//a[@class="nav__button-secondary btn-md btn-secondary-emphasis"]').click()
sleep(2)
```
*The sleep() function suspends (waits) execution of the current thread for a given number of seconds.*  
  
#### Our next move will be to fill login credentials automatically in LinkedIn sign in page. On inspecting the linkedin signin page we will get the XPATH of username and password. And we will use this to fill the details automatically as follows:
```python
#find the xpath to the username field and input username. Same with password
username_input = driver.find_element(By.XPATH, '//input[@name="session_key"]')
username_input.send_keys('yourmail@gmail.com')
sleep(2)

password_input = driver.find_element(By.ID, 'password')
password_input.send_keys('yourlinkedinpassword')
sleep(2)
```  
#### Now similarly find the XPATH of signin button and use to automatically click on it as follows:
```python
# find xpath to sign in button and click
driver.find_element(By.XPATH, '//div/button[text()="Sign in"]').click()
sleep(2)
```
