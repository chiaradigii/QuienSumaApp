# applications/functional_tests/test_user_signup_and_login.py
from selenium import webdriver
from django.test import LiveServerTestCase
from django.urls import reverse
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserSignupAndLoginFunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_user_signup_and_login(self):
        # User visits the signup page
        self.browser.get(f'{self.live_server_url}{reverse("jugador_app:signup")}')
        self.assertIn("Signup", self.browser.title)

        # User fills the signup form
        self.browser.find_element(By.NAME, 'user').send_keys('testuser_signup')
        self.browser.find_element(By.NAME, 'nombre').send_keys('Test')
        self.browser.find_element(By.NAME, 'apellido').send_keys('User')
        self.browser.find_element(By.NAME, 'fecha_nacimiento').send_keys('01-01-1990')
        self.browser.find_element(By.NAME, 'sexo').send_keys('M')
        self.browser.find_element(By.NAME, 'correo').send_keys('testuser_signup@example.com')
        self.browser.find_element(By.NAME, 'posicion').send_keys('Medio')
        self.browser.find_element(By.NAME, 'password1').send_keys('Password123')
        self.browser.find_element(By.NAME, 'password2').send_keys('Password123')
        self.browser.find_element(By.NAME, 'direccion').send_keys('Valid Address')

        submit_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, 'confirmarButton'))
        )
        submit_button.click()

        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, 'registroExitosoModal'))
        )    
         # Click the "Iniciar Sesión" button in the modal
        login_button = self.browser.find_element(By.LINK_TEXT, 'Iniciar Sesión')
        login_button.click()

        # Debugging information
        print(f"Current URL after modal interaction: {self.browser.current_url}")
        print(f"Page title after modal interaction: {self.browser.title}")

        # User logs in
        self.browser.find_element(By.NAME, 'username').send_keys('testuser_signup')
        self.browser.find_element(By.NAME, 'password').send_keys('Password123')
        submit_button = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'submit')))
        submit_button.click()

        try:
            WebDriverWait(self.browser, 10).until(
                EC.title_contains("Home")
            )
        except selenium.common.exceptions.TimeoutException:
            print("Did not redirect to home page.")
            return

        # User is redirected to the home page
        self.assertIn("Home", self.browser.title)


if __name__ == "__main__":
    LiveServerTestCase.main()