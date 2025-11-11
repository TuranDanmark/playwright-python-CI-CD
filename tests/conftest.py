import os
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


@pytest.fixture
def page_with_video(playwright):
    browser = playwright.chromium.launch(headless=False, slowMo=300)
    context = browser.new_context(record_video_dir=REPORTS_DIR)
    page = context.new_page()
    yield page
    context.close()
    browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.failed:
        page = item.funcargs.get("page_with_video") or item.funcargs.get("page")
        if page:
            screenshot_path = os.path.join(REPORTS_DIR, f"{item.name}_failed.png")
            page.screenshot(path=screenshot_path, full_page=True)
            if hasattr(result, "extra"):
                from pytest_html import extras
                result.extra.append(extras.image(screenshot_path))
