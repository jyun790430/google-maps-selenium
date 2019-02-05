from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
import csv


def wait_and_find(waitDriver: WebDriverWait, xpath: str)->str:

    element = waitDriver.until(EC.visibility_of_element_located(
        (By.XPATH, xpath))).find_element_by_xpath(xpath)
    return element.text


def wait_and_click(waitDriver: WebDriverWait, xpath: str):
    page = waitDriver.until(EC.element_to_be_clickable(
        (By.XPATH, xpath)))  # result detail page
    page.click()


def hotel_xpath(id: int):
    index = 1
    newindex = id*2-index
    div_id = str(newindex)
    section_result_xpath = '//*[@id="pane"]/div/div[1]/div/div/div[4]/div['+div_id+']'
    return section_result_xpath


def extract_hotel_info(id: int)->(str, str):
    section_result_xpath = hotel_xpath(id)
    wait_and_click(wait, section_result_xpath)
    phone_number_xpath = '//*[@id="pane"]/div/div[1]/div/div/div[18]/div/div[1]/span[3]/span[3]'
    phone = wait_and_find(wait, phone_number_xpath)
    print(phone)
    hotel_name_xpath = '//*[@id="pane"]/div/div[1]/div/div/div[1]/div[3]/div[1]/h1'
    hotel = wait_and_find(wait, hotel_name_xpath)
    print(hotel)
    time.sleep(2)
    current_url = driver.current_url
    print(current_url)
    print("please skip manually if no response")
    return hotel, phone


def writeToCsv(name: str, phone: str):
    with open('results.csv', 'a', newline='') as csvfile:
        fieldnames = ['name', 'phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow({'name': name, 'phone': phone})


if __name__ == "__main__":

    driver = webdriver.Chrome()
    url = 'https://www.google.com/maps/search/H%C3%B4tels/@14.4964286,-61.0759903,13z'
    driver.get(url)  # lat, long, zoom level
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    wait = WebDriverWait(driver, 10)

    for i in range(1, 20):
        name, phone = extract_hotel_info(i)
        writeToCsv(name, phone)
        driver.execute_script(script="window.history.back();")

    driver.quit()
