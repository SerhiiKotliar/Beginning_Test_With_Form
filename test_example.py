import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
# from main import get_user_input
#
# @pytest.fixture(scope="session")
# def user_data():
#     """Фікстура, яка перед запуском тестів показує форму і повертає введені дані"""
#     return get_user_input()
#
# @pytest.fixture()
# def browser():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     yield driver
#     driver.quit()


def test_username_not_empty(user_data):
    # Якщо користувач відмітив чекбокс для username, перевіряємо непорожність
    if user_data["login"]:
        assert user_data["login"] != "", "Логін користувача не може бути порожнім"

def test_url_contains_http(user_data):
    if user_data["url"]:
        assert "https" in user_data["url"], "URL має містити http"

def test_read_header(user_data, browser):
    url = user_data["url"]
    browser.get(url)
    #element = browser.find_element(By.ID, 'Welcome_to_Wikipedia')
    link = browser.find_element(By.LINK_TEXT, 'Wikipedia')
    link.click()
    history = browser.find_element(By.ID, 'toc-History')
    history.click()
    header = browser.find_element(By.LINK_TEXT, 'Nupedia')
    header.click()
    history2 = browser.find_element(By.ID, 'Nupedia')
    assert history2.text == 'Nupedia'

def test_find_header_text(user_data, browser):
    url = user_data["url"]
    browser.get(url)
    #element = browser.find_element(By.ID, 'Welcome_to_Wikipedia')
    link = browser.find_element(By.LINK_TEXT, 'Wikipedia')
    link.click()
    header = browser.find_element(By.ID, 'firstHeading')
    #history.click()
    header1 = browser.find_element(By.CSS_SELECTOR, 'table[class="infobox vcard"]')
    assert header.text == 'Wikipedia'
