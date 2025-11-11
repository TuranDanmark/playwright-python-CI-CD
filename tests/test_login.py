
import os
import json
import pytest
from playwright.sync_api import expect
from pages.test_login_page import LoginPage
BASE_URL = "https://the-internet.herokuapp.com/login"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "data", "credentials.json")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
    creds = json.load(f)


@pytest.mark.parametrize("user_type", ["valid_user", "invalid_user"])
def test_login(page_with_video, user_type):
    page = page_with_video
    page.goto(BASE_URL)
    login_page = LoginPage(page)

    username = creds[user_type]["username"]
    password = creds[user_type]["password"]
    login_page.login(username, password)

    if user_type == "valid_user":
        expect(page).to_have_url("https://the-internet.herokuapp.com/secure")
        expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")
        page.screenshot(path=os.path.join(REPORTS_DIR, "success_login.png"))
    else:
        expect(page.locator("#flash")).to_contain_text("Your username is invalid!")
        page.screenshot(path=os.path.join(REPORTS_DIR, "failed_login.png"))


def test_logout(page_with_video):
    page = page_with_video
    page.goto(BASE_URL)
    login_page = LoginPage(page)
    login_page.login(creds["valid_user"]["username"], creds["valid_user"]["password"])
    login_page.logout()

    expect(page).to_have_url(BASE_URL)
    expect(page.locator("#flash")).to_contain_text("You logged out of the secure area!")
    page.screenshot(path=os.path.join(REPORTS_DIR, "logout.png"))
