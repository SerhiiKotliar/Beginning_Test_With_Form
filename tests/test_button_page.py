from pages.simple_button import Simple_Button_Page
import allure
@allure.feature("simple_button")
@allure.story("existance")
def test_button1_exist(browser):
    with  allure.step("open_simple_button_step"):
        simple_page = Simple_Button_Page(browser)
        simple_page.open()
    with allure.step("open_simple_button_displayed_step"):
        assert simple_page.button_is_displayed()

@allure.feature("simple_button")
@allure.story("clicable")
def test_button1_clicked(browser):
    with allure.step("click_simple_button_step"):
        simple_page = Simple_Button_Page(browser)
        simple_page.open()
        simple_page.click_button()
    with allure.step("submit_simple_button_text_step"):
        assert "Submitted" == simple_page.result().text


