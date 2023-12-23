from selenium import webdriver

# Ruta al directorio del perfil que deseas cargar
profile_directory = r'C:\Users\upset\AppData\Local\Microsoft\Edge\User Data'

# Configurar opciones para el perfil
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + profile_directory)

# Crear instancia del controlador Chrome con el perfil especificado
driver = webdriver.Chrome(executable_path=r"C:\Path\to\chromedriver.exe", options=options)

# Ahora puedes usar 'driver' para interactuar con el navegador con el perfil cargado
driver.get('https://www.example.com')
