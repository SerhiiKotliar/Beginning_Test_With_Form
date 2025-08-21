import pytest
from selenium import webdriver
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

# @pytest.fixture()
# def browser():
#     chrome_browser = webdriver.Chrome()
#     chrome_browser.implicitly_wait(10)
#     return chrome_browser