from Beginning_Test_With_Form.pages.base_page import BasePage
from selenium.webdriver.common.by import By

button_selector = (By.LINK_TEXT, "Click")
result_selector = (By.ID, 'result-text')


class Like_Button_Page(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    def open(self):
        self.browser.get('https://www.qa-practice.com/elements/button/like_a_button')
    @property
    def button(self):
        return self.find(button_selector)

    def click_button(self):
        self.button.click()

    @property
    def button_is_displayed(self):
        return self.button.is_displayed()
    @property
    def result(self):
        return self.find(result_selector)

    @property
    def result_text(self):
        return self.result.text