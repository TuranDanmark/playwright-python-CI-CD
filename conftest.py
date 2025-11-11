import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Загружаем .env переменные
load_dotenv(override=True)


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")


@pytest.fixture(scope="session")
def credentials():
    return {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }


@pytest.fixture(scope="function")
def page_with_video(tmp_path_factory, request):
    """
    Для каждого теста создаётся отдельный браузер и контекст.
    Если тест падает — снимаем скриншот и логи добавляем в HTML-отчёт.
    """
    test_name = request.node.name
    video_dir = tmp_path_factory.mktemp(f"videos_{test_name}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir=str(video_dir))
        page = context.new_page()

        # собираем консольные логи браузера
        browser_logs = []
        page.on("console", lambda msg: browser_logs.append(f"{msg.type.upper()}: {msg.text}"))

        yield page

        # сохраняем логи браузера в атрибут теста (для отчёта)
        request.node.browser_logs = browser_logs

        context.close()
        browser.close()


def pytest_configure(config):
    os.makedirs("reports/screenshots", exist_ok=True)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Добавляем в отчёт HTML:
      - скриншот упавшего теста
      - текст ошибки со страницы
      - логи браузера (console)
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page_with_video", None)
        screenshot_path = os.path.join("reports", "screenshots", f"{item.name}.png")

        extra_html = ""

        # --- Скриншот ---
        if page:
            try:
                page.screenshot(path=screenshot_path)
                extra_html += f'<div><a href="{screenshot_path}" target="_blank">📸 View Screenshot</a></div>'
            except Exception as e:
                extra_html += f"<div>⚠️ Ошибка при сохранении скриншота: {e}</div>"

        # --- Сообщение об ошибке со страницы ---
        try:
            flash_message = page.locator("#flash").inner_text()
            extra_html += f"<div><b>💬 Flash Message:</b> {flash_message}</div>"
        except Exception:
            pass

        # --- Логи браузера ---
        browser_logs = getattr(item, "browser_logs", [])
        if browser_logs:
            logs_html = "<br>".join(browser_logs[-10:])  # последние 10 сообщений
            extra_html += f"<div><b>🧾 Browser console logs:</b><pre>{logs_html}</pre></div>"

        # --- Добавляем всё в отчёт HTML ---
        if "pytest_html" in item.config.pluginmanager.plugins:
            extra = getattr(rep, "extra", [])
            extra.append(pytest_html.extras.html(extra_html))
            rep.extra = extra
