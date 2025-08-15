def test_username_not_empty(user_data):
    # Якщо користувач відмітив чекбокс для username, перевіряємо непорожність
    if user_data["username"]:
        assert user_data["username"] != "", "Логін користувача не може бути порожнім"

def test_url_contains_http(user_data):
    if user_data["url"]:
        assert "http" in user_data["url"], "URL має містити http"
