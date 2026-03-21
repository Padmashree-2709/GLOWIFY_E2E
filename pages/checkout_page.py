import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    # Shipping Address Fields
    FIRST_NAME = (By.NAME, "first_name")
    LAST_NAME  = (By.NAME, "last_name")
    MOBILE     = (By.NAME, "mobile")
    ADDRESS    = (By.NAME, "address")
    CITY       = (By.NAME, "city")
    STATE      = (By.NAME, "state")
    PINCODE    = (By.NAME, "pincode")

    # Place Order Button
    PLACE_ORDER_BTN = (By.ID, "placeOrderBtn")

    # Values
    FIRST_NAME_VAL = "Shree"
    LAST_NAME_VAL  = "rishi"
    MOBILE_VAL     = "9360456985"
    ADDRESS_VAL    = "NO:05, MALLIGAI PURAM, GIRI ROAD, SRINIVASAPURAM"
    CITY_VAL       = "Thanjavur"
    STATE_VAL      = "Tamil Nadu"
    PINCODE_VAL    = "613009"

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_checkout_page(self):
        checkout_wait = WebDriverWait(self.driver, 60)
        checkout_wait.until(EC.url_contains("checkout"))
        self.wait_seconds(2)
        checkout_wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
        self.wait_seconds(1)
        print("✅ Checkout page loaded")

    def fill_shipping_address(self):
        self.type_text(*self.FIRST_NAME, self.FIRST_NAME_VAL)
        self.wait_seconds(0.3)
        self.type_text(*self.LAST_NAME, self.LAST_NAME_VAL)
        self.wait_seconds(0.3)
        self.type_text(*self.MOBILE, self.MOBILE_VAL)
        self.wait_seconds(0.3)
        self.type_text(*self.ADDRESS, self.ADDRESS_VAL)
        self.wait_seconds(0.3)
        self.type_text(*self.CITY, self.CITY_VAL)
        self.wait_seconds(0.3)
        self.type_text(*self.STATE, self.STATE_VAL)
        self.wait_seconds(0.3)
        self.type_text(*self.PINCODE, self.PINCODE_VAL)
        self.wait_seconds(0.3)
        print("✅ Shipping address filled successfully")

    def click_place_order(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(self.PLACE_ORDER_BTN)
        )
        self.js_click(*self.PLACE_ORDER_BTN)
        print("✅ Clicked Place Order")

    def handle_razorpay_flow(self):
        print("\n" + "="*60)
        print("👤 MANUAL ACTION REQUIRED — RAZORPAY PAYMENT")
        print("="*60)
        print("📱 Please complete these steps manually:")
        print("   1. Enter phone: 9360456985")
        print("   2. Click Pay Later")
        print("   3. Click Amazon Pay Later")
        print("   4. Enter OTP from phone")
        print("   5. Click Continue")
        print("   6. Close white blank page")
        print("   7. Close Payment Successful green screen")
        print("="*60)
        print("⏳ Automation waiting for Thank You page (max 5 mins)...")

        self.driver.switch_to.default_content()

        try:
            WebDriverWait(self.driver, 300).until(EC.url_contains("billing"))
            self.wait_seconds(5)
            if "billing" in self.driver.current_url:
                print("✅ Thank you for Your Purchase — Page Loaded Successfully!")
            else:
                print("⚠️ Thank You page not displayed — Skipping to next step")
        except:
            print("⚠️ Thank You page not displayed — Skipping to next step")
