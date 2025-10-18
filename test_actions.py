from playwright.sync_api import Page, expect

def test_main_actions(page: Page):
    page.get_by_test_id("search__input").fill("python")
    page.keyboard.press("Enter")

    expect(page).to_have_url("https://www.litres.ru/search/?q=python")
    page.locator("xpath=//*[@aria-description='Книги, которые можно читать без ограничений с активной Литрес: Подпиской']").dblclick()
    page.locator("xpath=//*[@aria-description='Книги, которые можно взять по Литрес: Абонементу']").click()

    page.check("label[for='languages-ru']")

    page.locator("button:has-text('Принять')").click()

    page.screenshot(path="screenshot/action.png")

    page.pause()