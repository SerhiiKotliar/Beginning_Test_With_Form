from selenium.webdriver.common.by import By
from Beginning_Test_With_Form.pages.simple_button import Simple_Button_Page


def test_button1_exist(browser):
    simple_page = Simple_Button_Page(browser)
    simple_page.open()
    assert simple_page.button_is_displayed()


def test_button1_clicked(browser):
    simple_page = Simple_Button_Page(browser)
    simple_page.open()
    simple_page.click_button()
    assert "Submitted" == simple_page.result().text


