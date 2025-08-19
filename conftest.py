import pytest
from selenium import webdriver
# from selenium.webdriver.common.by import By
from main import get_user_input

@pytest.fixture(scope="session")
def user_data():
    """Фікстура, яка перед запуском тестів показує форму і повертає введені дані"""
    return get_user_input()

@pytest.fixture()
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture()
def goto_adress(browser, user_data):
    # url = user_data["url"]
    browser.get(user_data["url"])
    return browser