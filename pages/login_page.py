from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):

    # Locators
    EMAIL_FIELD = (By.NAME, "email")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.auth-btn")

    # Credentials
    EMAIL = "Shreerishi2709@gmail.com"
    PASSWORD = "12345678glow"

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_login_page(self):
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FIELD))
        self.wait_seconds(1)
        print("Login page loaded")

    def perform_login(self):
        self.wait_for_login_page()
        self.type_text(*self.EMAIL_FIELD, self.EMAIL)
        print(f"Entered email: {self.EMAIL}")
        self.type_text(*self.PASSWORD_FIELD, self.PASSWORD)
        print("Entered password")
        self.click(*self.LOGIN_BUTTON)
        print("Clicked Login button")
        self.wait_seconds(3)
        print("Login successful!")
