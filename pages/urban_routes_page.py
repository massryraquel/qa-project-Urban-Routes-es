from symtable import Class
from selenium.webdriver.ie.service import Service
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
from data.data import phone_number
from utils import helpers



class UrbanRoutesPage: #Coloca aquí los localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, "//button[text()='Pedir un taxi']")
    comfort_icon = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")#hasta aca todo bn
    phone_field = (By.XPATH, "//div[@class='np-button'][.//div[text()='Número de teléfono']]")
    phone_input = (By.ID, "phone")
    next_phone_button = (By.XPATH, "//button[text()='Siguiente']")
    phone_code_field = (By.ID, "code")
    confirm_sms_button = (By.XPATH, "//button[@type='submit' and contains(normalize-space(.), 'Confirmar')]")
    payment_method_value = (By.XPATH, "//div[@class='pp-value-text' and text()='Efectivo']")
    add_card_button = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    card_number_input = (By.ID, "number")
    card_cvv_input = (By.CSS_SELECTOR, "div.card-code-input input#code")
    card_header = (By.XPATH, "//div[text()='Agregar tarjeta']")
    close_button =(By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    card_submit_button = (By.XPATH, "//button[contains(text(),'Agregar')]")
    message_input = (By.ID, "comment") #mensaje para el conductor
    blanket_checkbox = (By.CLASS_NAME, 'switch') #(By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following::input[1]")
    ice_cream_plus = (By.CLASS_NAME, "counter-plus")
    ice_cream_number = (By.CSS_SELECTOR, "div.counter-value")
    submit_button = (By.XPATH, "//button[@class='smart-button']") #enviar pedido

    def __init__(self, driver):
        self.driver = driver
        self.wait =WebDriverWait (driver,5)

    def set_from(self, from_address):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        self.wait.until(EC.presence_of_element_located(self.from_field)).send_keys(from_address)

    def set_to(self, to_address):
        #self.driver.find_element(*self.to_field).send_keys(to_address)
        self.wait.until(EC.presence_of_element_located(self.to_field)).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route (self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_request_taxi_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.request_taxi_button))
        #este es el paso dos, el getter, para obtener elemento

    def click_on_request_taxi_button(self):
        self.get_request_taxi_button().click()
        #paso tres, realizar la acción que quiero

    def get_comfort_icon(self):
        return self.wait.until(EC.element_to_be_clickable(self.comfort_icon))

    def click_on_comfort_icon(self):
        self.get_comfort_icon().click()

    def click_on_phone_field(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_field)).click()

    def set_phone_input(self, phone_number):
        self.wait.until(EC.element_to_be_clickable(self.phone_input)).send_keys(phone_number)
        self.wait.until(EC.element_to_be_clickable(self.next_phone_button)).click()

    def get_phone_input(self):
        return self.driver.find_element(*self.phone_input).get_property('value')

    def set_phone_code(self):
        code = helpers.retrieve_phone_code(self.driver)
        self.wait.until(EC.presence_of_element_located(self.phone_code_field)).send_keys(code)
        self.wait.until(EC.element_to_be_clickable(self.confirm_sms_button)).click()

    def add_card(self, card_number, card_code):
        self.wait.until(EC.element_to_be_clickable(self.payment_method_value)).click() #getter, setter, clicker
        self.wait.until(EC.element_to_be_clickable(self.add_card_button)).click()
        number_input = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        number_input.send_keys(card_number)
        cvv_input = self.wait.until(EC.visibility_of_element_located(self.card_cvv_input))
        cvv_input.send_keys(card_code)
        cvv_input.send_keys(Keys.TAB) #simula click en el tabulador
        #self.wait.until(EC.element_to_be_clickable(self.card_header)) .click() #probar el random click
        self.wait.until(EC.element_to_be_clickable(self.card_submit_button)).click()
        self.wait.until(EC.element_to_be_clickable(self.close_button)).click()

    def enter_message(self, message):
        self.wait.until(EC.presence_of_element_located(self.message_input)).send_keys(message)

    def request_blanket(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_checkbox)).click()

    def add_ice_cream(self, count):
        for _ in range(count):
            self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus)).click()

    def get_ice_cream_value(self):
        return self.wait.until(EC.element_to_be_clickable(self.ice_cream_number)).text.strip()

    def submit_order(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()

