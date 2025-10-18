from playwright.sync_api import Page, expect

def test_main_page_title(page: Page):
    page.goto("https://www.litres.ru/")
    assert page.title() == "Литрес – сервис электронных и аудиокниг, скачать в fb2 и mp3, читать и слушать онлайн на Litres"

def test_audiobook_page_title(page: Page):
    page.goto("https://www.litres.ru/")
    page.locator("xpath=//*[@id=\"lowerMenuWrap\"]/nav/div/a[6]").click()
    expect(page).to_have_title("Аудиокниги – слушать онлайн или скачать в mp3 на Литрес")