from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class ShopPage(BasePage):


    LIPSTICK_LISTING_ADD_TO_CART = (By.CSS_SELECTOR, "a.add-cart")

    
    LIPSTICK_DETAIL_ADD_TO_CART = (By.CSS_SELECTOR, "button.add-cart.detail-cart-btn")

    
    QUICK_ADD_TO_CART = (By.CSS_SELECTOR, "button.add-cart.quick-add")

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_shop_page(self, selector):
        shop_wait = WebDriverWait(self.driver, 60)
        shop_wait.until(EC.presence_of_element_located(selector))
        self.wait_seconds(2)
        print(" Shop category page loaded")

    
    def add_lipstick_to_cart(self):
        
        self.wait_for_shop_page(self.LIPSTICK_LISTING_ADD_TO_CART)
        element = self.driver.find_element(*self.LIPSTICK_LISTING_ADD_TO_CART)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.wait_seconds(1)
        self.js_click(*self.LIPSTICK_LISTING_ADD_TO_CART)
        self.wait_seconds(2)
        print("Clicked Add to Cart on Lipstick listing -> Going to Detail Page")

        # Step 2: detail page → click button.add-cart.detail-cart-btn
        detail_wait = WebDriverWait(self.driver, 60)
        detail_wait.until(EC.presence_of_element_located(self.LIPSTICK_DETAIL_ADD_TO_CART))
        self.wait_seconds(1)
        element = self.driver.find_element(*self.LIPSTICK_DETAIL_ADD_TO_CART)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.wait_seconds(1)
        self.js_click(*self.LIPSTICK_DETAIL_ADD_TO_CART)
        self.wait_seconds(2)
        print("Clicked Add to Cart on Lipstick Detail Page -> Added!")

    
    
    def add_quick_product_to_cart(self, category_name):
        self.wait_for_shop_page(self.QUICK_ADD_TO_CART)
        element = self.driver.find_element(*self.QUICK_ADD_TO_CART)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.wait_seconds(1)
        self.js_click(*self.QUICK_ADD_TO_CART)
        self.wait_seconds(2)
        print(f"Clicked Add to Cart on {category_name} listing -> Added!")

    
    def add_product_to_cart(self, category_name):
        if category_name == "Lipsticks":
            self.add_lipstick_to_cart()
        else:
            self.add_quick_product_to_cart(category_name)
        print(f" '{category_name}' product added to cart successfully!! ")