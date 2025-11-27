from pages.login_page import LoginPage
from playwright.sync_api import expect


def test_login_success(page):
    login = LoginPage(page)
    login.open()
    login.enter_username("standard_user")
    login.enter_password("secret_sauce")
    login.submit()
    expect(page.locator("[data-test=\"product-sort-container\"]")).to_contain_text("Name (A to Z)Name (Z to A)Price (low to high)Price (high to low)")


def test_login_fail(page):
    login = LoginPage(page)
    login.open()
    login.enter_username("wrong")
    login.enter_password("wrong")
    login.submit()
    login.should_have_error("Username and password do not match")
