from pages.likeButton import Like_Button_Page
import allure

@allure.feature("like_a_button")
@allure.story("like_existance")
def test_button2_exist(browser):
    # with allure.step("open_like_button_step"):
    like_a_button_page = Like_Button_Page(browser)
    like_a_button_page.open()
    # with allure.step("displayed_like_button_step"):
    assert like_a_button_page.button.is_displayed()

@allure.feature("like_a_button")
@allure.story("like_clicable")
def test_button2_clicked(browser):
    # with allure.step("clicable_like_button_step"):
    like_a_button_page = Like_Button_Page(browser)
    like_a_button_page.open()
    like_a_button_page.click_button()
    with allure.step("submitted_like_button_text"):
        assert "Submitted" == like_a_button_page.result.text