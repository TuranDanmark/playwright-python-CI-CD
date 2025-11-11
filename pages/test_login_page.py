import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = "#username"
        self.password_input = "#password"
        self.submit_button = "button[type='submit']"
        self.flash = "#flash"
        self.logout_link = "a[href='/logout']"

    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.screenshot(path=os.path.join(REPORTS_DIR, "step_login.png"))
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_button)

    def logout(self):
        self.page.click(self.logout_link)
        self.page.screenshot(path=os.path.join(REPORTS_DIR, "step_logout.png"))
