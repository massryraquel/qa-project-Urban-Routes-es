"""Proyecto: Urban Routes App 

Este proyecto automatiza el proceso de solicitud de un taxi en la aplicación web Urban Routes utilizando Selenium WebDriver.
Las pruebas automatizadas cubren el flujo completo de uso de la aplicación como ingresar direcciones, seleccionar tarifas, 
registrar número telefónico, añadir métodos de pago y realizar la solicitud de un taxi.

La tecnologías utilizadas fueron las siguientes: Python 3.13, Selenium WebDriver, 
pytest, Google Chrome y ChromeDriver.

Las técnicas utilizadas fueron las siguientes: Page Object Model (POM) y  WebDriverWait

---

## Estructura del Proyecto
qa-project-Urban-Routes-es/ 
test_urban_routes.py # Pruebas automatizadas
data.py # Datos de prueba (direcciones, teléfono, tarjeta)
helpers.py      # Funciones de ayuda, como retrieve_phone_code
urban_routes_pages.py        # Clase UrbanRoutesPage con localizadores y métodos
README.md # Desglose de acciones realizadas
"""