from selenium.webdriver.common.by import By
from Beginning_Test_With_Form.pages.likeButton import Like_Button_Page



def test_button2_exist(browser):
    like_a_button_page = Like_Button_Page(browser)
    like_a_button_page.open()
    assert like_a_button_page.button.is_displayed()


def test_button2_clicked(browser):
    like_a_button_page = Like_Button_Page(browser)
    like_a_button_page.open()
    like_a_button_page.click_button()
    assert "Submitted" == like_a_button_page.result.text