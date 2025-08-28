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

from data import phone_number


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage: #Aquí coloca los localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, "//button[text()='Pedir un taxi']")
    comfort_icon = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    phone_input = (By.ID, "phone")



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

    def get_phone(self):
        return self.wait.until(EC.element_to_be_clickable(self.phone_input))

    def set_phone(self, phone_number):
        self.wait.until(EC.element_to_be_clickable(self.phone_input)) .send_keys(phone_number)

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):#configuraciones iniciales antes de empezar a probar
        chrome_options= webdriver.ChromeOptions()
        chrome_options.set_capability("goog:loggingPrefs", {'performance':'ALL'})
        cls.driver = webdriver.Chrome (service=Service(), options=chrome_options)
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
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

    def test_enter_phone(self):
        self.driver.get(data.urban_routes_url)
        phone_number = data.phone_number
        self.routes_page.set_phone_input(phone_number)
        assert self.routes_page.get_phone_input() == phone_number
        time.sleep(12)

    @classmethod
    def teardown_class(cls): #cierra todo y deja limpio el sistema
        cls.driver.quit()
