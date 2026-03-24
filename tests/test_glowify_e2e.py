import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.chatbot_page import ChatbotPage

BASE_URL = "https://glowify-cosmetics-site.onrender.com/"

CATEGORIES = [
    "Lipsticks",
    "Skincare",
    "Eye Makeup",
]


class TestGlowifyE2E:

    def setup_method(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.popups": 1,
            "profile.default_content_setting_values.notifications": 2,
        })
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1280, 800)
        print("\n Browser launched")

    def teardown_method(self):
        time.sleep(2)
        self.driver.quit()
        print("Browser closed")

    def screenshot(self, name):
        import os
        path = f"screenshots/{name}.png"
        os.makedirs("screenshots", exist_ok=True)
        self.driver.save_screenshot(path)
        print(f" Screenshot saved: {path}")

    def test_glowify_e2e(self):

        # ============================================================
        # STEP 1: Website Load
        # ============================================================
        print("\n" + "="*60)
        print("STEP 1: Opening Glowify Website...")
        print("="*60)
        self.driver.get(BASE_URL)
        print(" Render server waking up — may take 2-3 mins...")
        home_page = HomePage(self.driver)
        home_page.wait_for_homepage()
        self.screenshot("01_homepage")

        # ============================================================
        # STEP 2: Login
        # ============================================================
        print("\n" + "="*60)
        print("STEP 2: Login")
        print("="*60)
        home_page.click_profile_icon()
        login_page = LoginPage(self.driver)
        login_page.perform_login()
        home_page.wait_for_homepage()
        self.screenshot("02_login_success")
        print(" Redirected to Homepage after login")

        # ============================================================
        # STEP 3: Shop → 3 Categories
        # ============================================================
        print("\n" + "="*60)
        print("STEP 3: Adding products from 3 categories...")
        print("="*60)
        shop_page = ShopPage(self.driver)
        for category in CATEGORIES:
            print(f"\n--- Category: {category} ---")
            self.driver.get(BASE_URL)
            home_page.wait_for_homepage()
            home_page.hover_shop_and_click_category(category)
            shop_page.add_product_to_cart(category)
            self.screenshot(f"03_added_{category.lower().replace(' ', '_')}")
        print("\n All 3 products added to cart!")

        # ============================================================
        # STEP 4: Cart
        # ============================================================
        print("\n" + "="*60)
        print("STEP 4: Cart → Checkout")
        print("="*60)
        self.driver.get(BASE_URL)
        home_page.wait_for_homepage()
        cart_page = CartPage(self.driver)
        cart_page.click_cart_icon()
        cart_page.wait_for_cart_page()
        cart_page.select_all_items()
        time.sleep(1)
        cart_page.assert_cart_items(expected_count=3)
        self.screenshot("04_cart_with_3_items")
        cart_page.click_proceed_to_checkout()

        # ============================================================
        # STEP 5: Checkout Form → Place Order
        # ============================================================
        print("\n" + "="*60)
        print("STEP 5: Filling Checkout Form...")
        print("="*60)
        checkout_page = CheckoutPage(self.driver)
        checkout_page.wait_for_checkout_page()
        checkout_page.fill_shipping_address()
        self.screenshot("05_checkout_form_filled")
        checkout_page.click_place_order()

        # ============================================================
        # STEP 6: Razorpay Payment (Manual)
        # ============================================================
        print("\n" + "="*60)
        print("STEP 6: Razorpay Payment Flow...")
        print("="*60)
        checkout_page.handle_razorpay_flow()
        self.screenshot("06_thank_you_page")

        # ============================================================
        # STEP 7: My Orders
        # ============================================================
        print("\n" + "="*60)
        print("STEP 7: My Orders")
        print("="*60)
        self.driver.get(BASE_URL)
        home_page.wait_for_homepage()
        account_toggle = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.icon-circle.account-toggle"))
        )
        account_toggle.click()
        time.sleep(1)
        print(" Clicked Account Toggle")
        my_orders_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/shop/my-orders/']"))
        )
        my_orders_link.click()
        time.sleep(2)
        print("Clicked My Orders")
        WebDriverWait(self.driver, 15).until(EC.url_contains("my-orders"))
        time.sleep(1)
        self.screenshot("07_my_orders_page")

        # ============================================================
        # STEP 8: Chatbot Test
        # ============================================================
        print("\n" + "="*60)
        print("STEP 8: Chatbot Test")
        print("="*60)
        self.driver.get(BASE_URL)
        home_page.wait_for_homepage()
        chatbot_page = ChatbotPage(self.driver)
        chatbot_page.perform_chatbot_test()
        self.screenshot("08_chatbot_test")

        # ============================================================
        # STEP 9: Logout
        # ============================================================
        print("\n" + "="*60)
        print("STEP 9: Logout")
        print("="*60)
        self.driver.get(BASE_URL)
        home_page.wait_for_homepage()
        home_page.click_logout()
        self.screenshot("09_logout")

        print("\n" + "="*60)
        print(" END-TO-END TEST COMPLETED SUCCESSFULLY!")
        print("="*60)