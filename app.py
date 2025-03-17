import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

# -------------------------------------------------------------------------------------------------------------------------------

# Read the CSV file
df = pd.read_csv("information.csv")
path = os.getcwd()

# -------------------------------------------------------------------------------------------------------------------------------

# Access the email and password columns
emails = df["Email"]
passwords = df["Password"]
title = df["Title"][0]
price = df["Price"][0]
tags = df["Tags"]
description = df["Description"][0]
locations = df["Postcodes"]
# print (description[0])
url = 'http://www.facebook.com'

# print(len(locations))
# -------------------------------------------------------------------------------------------------------------------------------

# Initialize Selenium driver
def get_driver(inp):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")  # Disable notification popups
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument(f'--user-data-dir=D:\softwear\chromeprofile{inp}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)
    driver.maximize_window()
    time.sleep(2)
    count = 0
    return count ,driver


# -------------------------------------------------------------------------------------------------------------------------------

def run_script(driver, images_path, title, price, tags, description, location):
    time.sleep(3)
    driver.get("https://www.facebook.com/marketplace/create/item")
    time.sleep(5)
    s = driver.find_element("xpath","//input[@type='file']")
    s.send_keys(images_path)
    time.sleep(8)
    list_input = driver.find_elements(By.XPATH, "//input[@type='text']") #.send_keys(title)
    print("\n Number of input feilds: ", len(list_input))
    if len(list_input) >= 2:
        list_input[0].send_keys(title)
        time.sleep(2)
        list_input[1].send_keys(str(price))
        time.sleep(2)
    else:
        print("Error: Input fields not found")
    list_dropdown = driver.find_elements(By.XPATH, "//label[@aria-labelledby]")
    if len(list_dropdown) >= 2:
        list_dropdown[0].click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//span[text()='Furniture']").click()
        time.sleep(2)
        list_dropdown[1].click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//span[text()='New']/ancestor::div[@role='option']").click()
        time.sleep(2)
    else:
        print("Error: Dropdown fields not found")
    driver.find_element(By.XPATH, "//span[text()='Description']/following::textarea[1]").send_keys(description)
    time.sleep(2)
    for tag in tags:
        tag_input = driver.find_element(By.XPATH, "//span[text()='Product tags']/following::textarea[1]")
        tag_input.send_keys(tag)
        time.sleep(2)
        tag_input.send_keys(Keys.ENTER)
        time.sleep(2)
    location_input = driver.find_element(By.XPATH, "//input[@aria-label='Location']")
    location_input.send_keys(Keys.CONTROL + "a")
    location_input.send_keys(Keys.DELETE)
    time.sleep(2)
    location_input.send_keys(location)
    time.sleep(2)
    driver.find_element(By.XPATH, "//ul[@role='listbox']/li[1]").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,"[aria-label='Next']").click()
    time.sleep(10)
    driver.find_element(By.CSS_SELECTOR,"[aria-label='Publish']").click()
    time.sleep(15)
    driver.close()
    return

# -------------------------------------------------------------------------------------------------------------------------------

for idx, i in enumerate(emails):
# -------------------------------------------------------------------------------------------------------------------------------

    count, driver = get_driver(idx)
    try:
        # Log in to Facebook
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Email address or phone number']").send_keys(i)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "[aria-label='Password']").send_keys(passwords[idx])
        time.sleep(2)
        driver.find_element(By.NAME, "login").click()
        time.sleep(10)
    except Exception as e:
        print("\nWrong credientials\n")
        print(e)

# -------------------------------------------------------------------------------------------------------------------------------
    # print(locations[0])
    # Get all file names in the "images" folder
    image_files = os.listdir("images")
    for i in image_files:
        images_path = path + "/images/" + i
        print(images_path)
        time.sleep(2)
        try:
            run_script(driver, images_path, title, price, tags, description, locations[count])
            count += 1
            if count == len(locations):
                count = 0
        except Exception as e:
            print("Failed: image_path: ", images_path)
            print(e)
