from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class HomePage(BasePage):

    # Locators
    NAV_SHOP = (By.CSS_SELECTOR, "li.shop-hover")
    PROFILE_ICON = (By.CSS_SELECTOR, "a[href='/accounts/login/']")
    ACCOUNT_TOGGLE = (By.CSS_SELECTOR, "div.account-toggle")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/accounts/logout/']")

    # Category links
    CATEGORY_URLS = {
        "Lipsticks": "/shop/category/lipsticks/",
        "Skincare": "/shop/category/skincare/",
        "Eye Makeup": "/shop/category/eye-makeup/",

    }

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_homepage(self):
        # Render free hosting — server sleep state la irukum
        # 3 mins (180 secs) explicit wait — server wake up aaagum varaikkum
        print("⏳ Waiting for Render server to wake up (max 3 mins)...")
        render_wait = WebDriverWait(self.driver, 180)
        render_wait.until(EC.presence_of_element_located(self.NAV_SHOP))
        self.wait_seconds(2)
        print("Homepage loaded successfully — Server is awake!")

    def click_profile_icon(self):
        self.click(*self.PROFILE_ICON)
        self.wait_seconds(1)
        print(" Clicked Profile Icon")

    def hover_shop_and_click_category(self, category_name):
        # Hover over Shop
        from selenium.webdriver.common.action_chains import ActionChains
        shop_element = self.wait.until(
            EC.presence_of_element_located(self.NAV_SHOP)
        )
        ActionChains(self.driver).move_to_element(shop_element).perform()
        self.wait_seconds(1)
        print(f" Hovered over Shop menu")

        # Click category link
        category_url = self.CATEGORY_URLS[category_name]
        category_locator = (By.CSS_SELECTOR, f"a[href='{category_url}']")
        self.click(*category_locator)
        self.wait_seconds(2)
        print(f" Clicked category: {category_name}")

    def click_account_toggle(self):
        self.click(*self.ACCOUNT_TOGGLE)
        self.wait_seconds(1)
        print("Clicked Account Toggle")

    def click_logout(self):
        self.click_account_toggle()
        self.click(*self.LOGOUT_LINK)
        self.wait_seconds(2)
        print("Clicked Logout")
