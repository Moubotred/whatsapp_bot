from selenium import webdriver

# Ruta al archivo ejecutable de GeckoDriver
# geckodriver_path = 'C:\Program Files\geckodriver'

# Configuración del navegador
options = webdriver.FirefoxOptions()
options.headless = False  # Cambia a True si deseas que el navegador sea invisible

# Configuración del tiempo de espera
options.set_preference("http.connection.timeout", 10)
options.set_preference("network.connection.timeout", 10)

# Inicializar el navegador
driver = webdriver.Firefox(options=options)

# Resto del código...
