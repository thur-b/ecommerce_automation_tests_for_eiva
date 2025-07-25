import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time
import random

@allure.suite("Automation Exercise Test Suite")
class AutomationExerciseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("https://automationexercise.com/")

    def setUp(self):
        self.driver.get("https://automationexercise.com/")

    def generate_email(self):
        return f"testuser{random.randint(1000,9999)}@test.com"

    @allure.title("Test Registration and Auto Login")
    def test_01_registration_and_auto_login(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Signup / Login").click()
        name = "Test User"
        email = self.generate_email()
        firstname = "FirstName"
        lastname = "LastName"
        state = "State_1"
        city = "City_1"
        zipcode ="2223"
        mobilenumber = "12345678978"
        firstaddress = "222 Austin"

        driver.find_element(By.NAME, "name").send_keys(name)
        driver.find_element(By.XPATH, "//input[@data-qa='signup-email']").send_keys(email)
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()

        driver.find_element(By.ID, "id_gender1").click()
        driver.find_element(By.ID, "password").send_keys("TestPass123")
        driver.find_element(By.ID, "days").send_keys("1")
        driver.find_element(By.ID, "months").send_keys("January")
        driver.find_element(By.ID, "years").send_keys("1990")
        driver.find_element(By.ID, "first_name").send_keys(firstname)
        driver.find_element(By.ID, "last_name").send_keys(lastname)
        driver.find_element(By.ID, "address1").send_keys(firstaddress)
        driver.find_element(By.XPATH, "//option[text()='Australia']").click()
        driver.find_element(By.ID, "state").send_keys(state)
        driver.find_element(By.ID, "city").send_keys(city)
        driver.find_element(By.ID, "zipcode").send_keys(zipcode)
        driver.find_element(By.ID, "mobile_number").send_keys(mobilenumber)
        driver.find_element(By.XPATH, "//button[text()='Create Account']").click()

        success_text = driver.find_element(By.TAG_NAME, "h2").text
        self.assertIn("ACCOUNT CREATED!", success_text)
        driver.find_element(By.LINK_TEXT, "Continue").click()
        self.assertTrue("Logged in as" in driver.page_source)

        AutomationExerciseTests.new_email = email
        AutomationExerciseTests.password = "TestPass123"


    @allure.title("Test Logout and Login with Same Credentials")
    def test_02_logout_and_login(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Logout").click()
        self.assertIn("Login to your account", driver.page_source)

        driver.find_element(By.NAME, "email").send_keys(AutomationExerciseTests.new_email)
        driver.find_element(By.NAME, "password").send_keys(AutomationExerciseTests.password)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(2)
        self.assertTrue("Logged in as" in driver.page_source)

    @allure.title("Test Product Search and Add to Cart")
    def test_03_product_search_and_add_to_cart(self):
        driver = self.driver
        driver.find_element(By.PARTIAL_LINK_TEXT, "Products").click()
        driver.find_element(By.ID, "search_product").send_keys("t-shirt")
        driver.find_element(By.ID, "submit_search").click()

        self.assertIn("Searched Products", driver.page_source)
        driver.execute_script("window.scrollBy(0, 500);")
        driver.find_element(By.XPATH, "(//a[text()='Add to cart'])[1]").click()
        time.sleep(2)
        driver.find_element(By.LINK_TEXT, "View Cart").click()
        self.assertIn("Shopping Cart", driver.page_source)
        self.assertTrue("dress" in driver.page_source.lower())

    @allure.title("Test Cart Total Update")
    def test_04_cart_total_update(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        cart_total_elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Rs.')]")))
        cart_total = cart_total_elem.text
        self.assertTrue("Rs." in cart_total)
        driver.find_element(By.LINK_TEXT, "Logout").click()

    # Negative Tests

    @allure.title("Negative Test: Registration with Existing Email")
    def test_05_negative_registration_existing_email(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Signup / Login").click()
        driver.find_element(By.NAME, "name").send_keys("User")
        driver.find_element(By.XPATH, "//input[@data-qa='signup-email']").send_keys("test@test.com")
        driver.find_element(By.XPATH, "//button[text()='Signup']").click()
        time.sleep(3)
        self.assertIn("Email Address already exist!", driver.page_source)

    @allure.title("Negative Test: Invalid Login Credentials")
    def test_06_negative_login_invalid_credentials(self):
        driver = self.driver
        driver.find_element(By.LINK_TEXT, "Signup / Login").click()
        driver.find_element(By.NAME, "email").send_keys("fakeuser@test.com")
        driver.find_element(By.NAME, "password").send_keys("WrongPass")
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(3)
        self.assertIn("Your email or password is incorrect!", driver.page_source)

    @allure.title("Negative Test: Gibberish Product Search")
    def test_07_negative_search_gibberish(self):
        driver = self.driver
        driver.find_element(By.PARTIAL_LINK_TEXT, "Products").click()
        driver.find_element(By.ID, "search_product").send_keys("asldkjaslkdj")
        driver.find_element(By.ID, "submit_search").click()
        self.assertIn("Searched Products", driver.page_source)
        self.assertNotIn("Add to cart", driver.page_source)

    @allure.title("Negative Test: Check Empty Cart")
    def test_08_negative_cart_empty_check(self):
        driver = self.driver
        driver.find_element(By.PARTIAL_LINK_TEXT, "Cart").click()
        wait = WebDriverWait(driver, 10)
        cart_msg_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//b[contains(text(),'empty')]")))
        empty_text = cart_msg_element.text
        self.assertTrue("empty" in empty_text.lower())

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
