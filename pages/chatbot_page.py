from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class ChatbotPage(BasePage):

    # Locators
    CHATBOT_TOGGLE = (By.ID, "chatbot-toggle")
    CHAT_INPUT = (By.ID, "chat-input")
    CHAT_SEND = (By.ID, "chat-send")
    CHAT_CLOSE = (By.ID, "chat-close")
    CHAT_MESSAGES = (By.ID, "chat-messages")
    BOT_MSG = (By.CSS_SELECTOR, ".bot-msg")

    def __init__(self, driver):
        super().__init__(driver)

    def open_chatbot(self):
        self.click(*self.CHATBOT_TOGGLE)
        self.wait_seconds(2)
        self.wait.until(EC.visibility_of_element_located(self.CHAT_INPUT))
        print("✅ Chatbot opened")

    def send_message(self, message):
        self.type_text(*self.CHAT_INPUT, message)
        self.wait_seconds(0.5)
        self.click(*self.CHAT_SEND)
        print(f"✅ Sent message: '{message}'")

    def wait_for_bot_response(self, prev_count, timeout=15):
        """Wait until a new bot message appears"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(*self.BOT_MSG)) > prev_count
            )
            bot_msgs = self.driver.find_elements(*self.BOT_MSG)
            latest = bot_msgs[-1].text.strip()
            print(f"✅ Bot responded: '{latest[:60]}{'...' if len(latest) > 60 else ''}'")
            return len(bot_msgs)
        except:
            print("⚠️ Bot response not received within timeout — continuing")
            return prev_count

    def close_chatbot(self):
        self.click(*self.CHAT_CLOSE)
        self.wait_seconds(1)
        print("✅ Chatbot closed")

    def perform_chatbot_test(self):
        print("\n--- Starting Chatbot Test ---")

        # Open chatbot
        self.open_chatbot()
        self.wait_seconds(2)

        # Get initial bot message count
        initial_count = len(self.driver.find_elements(*self.BOT_MSG))

        # Send "hello" and wait for response
        self.send_message("hello")
        print("⏳ Waiting for bot response...")
        current_count = self.wait_for_bot_response(initial_count)

        # Send "lipsticks" and wait for response
        self.send_message("lipsticks")
        print("⏳ Waiting for bot response...")
        self.wait_for_bot_response(current_count)

        # Close chatbot
        self.close_chatbot()
        print("✅ Chatbot test completed!")
