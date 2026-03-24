from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class CartPage(BasePage):

    CART_LINK = (By.CSS_SELECTOR, "a[href='/shop/cart/']")
    PROCEED_TO_CHECKOUT = (By.ID, "proceedCheckout")
    SUMMARY_TOTAL = (By.CSS_SELECTOR, "div.summary-total")
    ORDER_SUMMARY = (By.CSS_SELECTOR, "div.order-summary")

    def __init__(self, driver):
        super().__init__(driver)

    def click_cart_icon(self):
        self.click(*self.CART_LINK)
        self.wait_seconds(2)
        print(" Clicked Cart icon")

    def wait_for_cart_page(self):
        cart_wait = WebDriverWait(self.driver, 60)
        cart_wait.until(EC.presence_of_element_located(self.PROCEED_TO_CHECKOUT))
        self.wait_seconds(3)
        print(" Cart page loaded")

    def assert_cart_items(self, expected_count=3):
        items = self.driver.find_elements(
            By.XPATH, "//div[contains(@class,'cart-item')] | //tr[contains(@class,'cart-row')]"
        )
        actual = len(items)
        print(f" Cart items found: {actual}")
        assert actual >= expected_count, f" Expected {expected_count} items, but found {actual}"
        print(f" Cart has {actual} items — OK!")

    def select_all_items(self):
        try:
            checkboxes = self.driver.find_elements(
                By.XPATH, "//input[@type='checkbox']"
            )
            for cb in checkboxes:
                if not cb.is_selected():
                    self.driver.execute_script("arguments[0].click();", cb)
                    self.wait_seconds(0.3)
            print(f" All {len(checkboxes)} cart items selected!")
        except Exception as e:
            print(f" Checkbox select error: {e}")

    def click_proceed_to_checkout(self):
    

        self.wait.until(EC.presence_of_element_located(self.PROCEED_TO_CHECKOUT))
        element = self.driver.find_element(*self.PROCEED_TO_CHECKOUT)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.wait_seconds(1)

        # javascript:void(0) button — use JS click
        self.driver.execute_script("arguments[0].click();", element)
        self.wait_seconds(3)

        if "checkout" in self.driver.current_url:
            print(" Navigated to Checkout — cart session carried!")
        else:
            # Try dispatchEvent as fallback
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new MouseEvent('click', {
                    bubbles: true, cancelable: true, view: window
                }));
            """, element)
            self.wait_seconds(3)

            if "checkout" in self.driver.current_url:
                print(" Navigated to Checkout via dispatchEvent!")
            else:
                raise Exception(" Failed to navigate to checkout — cart session lost!")
