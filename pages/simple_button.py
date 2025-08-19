from pages.base_page import BasePage
from selenium.webdriver.common.by import By

button_selector = (By.ID, 'submit-id-submit')

class Simple_Button_Page(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    def button(self):
        return self.find()