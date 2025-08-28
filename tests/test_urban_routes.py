from data import data
from symtable import Class
from selenium.webdriver.ie.service import Service
from pages import urban_routes_page as urp
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from utils import helpers
import time


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):#configuraciones iniciales antes de empezar a probar
        chrome_options= webdriver.ChromeOptions()
        chrome_options.set_capability("goog:loggingPrefs", {'performance':'ALL'})
        cls.driver = webdriver.Chrome (service=Service(), options=chrome_options)
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = urp.UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        #self.driver.get(data.urban_routes_url) #se llama en setup_class
        #routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

    def test_select_comfort(self):
        #routes_page = UrbanRoutesPage(self.driver)
        self.routes_page.click_on_request_taxi_button()
        self.routes_page.click_on_comfort_icon()
        #self.routes_page.set_phone_code(self.driver)

    def test_enter_phone_and_sms(self):
        phone_number = data.phone_number
        self.routes_page.click_on_phone_field()
        self.routes_page.set_phone_input(phone_number)
        assert self.routes_page.get_phone_input() == phone_number
        self.routes_page.set_phone_code()
        #time.sleep(2)

    def test_add_card(self):
        card_number, card_code = data.card_number, data.card_code
        self.routes_page.add_card(card_number, card_code)
        #self.routes_page.click_on_card_header #probar
        #time.sleep(3)

    def test_enter_message(self):
        self.routes_page.enter_message(data.message_for_driver)

    def test_request_blanket(self):
        self.routes_page.request_blanket()
        time.sleep(2)

    def test_add_ice_creams(self):
        self.routes_page.add_ice_cream(2)
        assert self.routes_page.get_ice_cream_value() == "2"

    def test_submit_order(self):
        self.routes_page.submit_order()
        time.sleep(3)

    @classmethod
    def teardown_class(cls): #cierra todo y deja limpio el sistema
        cls.driver.quit()
        #pass
