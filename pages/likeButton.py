from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure

button_selector = (By.LINK_TEXT, "Click")
result_selector = (By.ID, 'result-text')


class Like_Button_Page(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    def open(self):
        with allure.step("open_like_a_button_page"):
            self.browser.get('https://www.qa-practice.com/elements/button/like_a_button')
    @property
    def button(self):
        return self.find(button_selector)

    def click_button(self):
        with allure.step("click_button"):
            self.button.click()

    @property
    def button_is_displayed(self):
        with allure.step("check_like_button_is_displayed"):
            return self.button.is_displayed()
    @property
    def result(self):
        return self.find(result_selector)

    @property
    def result_text(self):
        with allure.step("Get_result_text"):
            return self.result.text