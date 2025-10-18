from playwright.sync_api import Page, expect

def test_locator_role(page: Page,):
    page.get_by_role("button", name="Найти").click()
    expect(page.get_by_text("стивен кинг")).to_be_visible()

def test_locator_placeholder(page: Page):
    page.get_by_placeholder("Искать на Литрес").fill("игра престолов")
    page.keyboard.press("Enter")
    expect(page.get_by_text("Результаты поиска <<игра престолов>>"))

def test_locator_datatestid(page: Page):
    page.get_by_test_id("header-catalog-button").click()
    expect(page.get_by_text("Бесплатные книги")).to_be_visible()

def test_locator_alttext(page: Page):
    page.get_by_alt_text("Логотип Литрес").click()
    expect(page).to_have_url("https://www.litres.ru/")

def test_locator_xpath(page: Page):
    expect(page.locator("xpath=//a[@title='YouTube']")).to_be_visible()