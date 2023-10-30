from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from lxml import html
import time as tmp


def send(x,iniciar):
    name = list(x)
    for x in name:
        iniciar.send_keys(x)
    iniciar.send_keys(Keys.RETURN)

profile_path = r'C:\Users\upset\AppData\Roaming\Mozilla\Firefox\Profiles\0vwq2jcr.default-release-1'
options=Options()
options.add_argument("-profile")
options.add_argument(profile_path)
#options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

driver.get('https://web.whatsapp.com/')
time = WebDriverWait(driver,60)
Msg_wait = WebDriverWait(driver,60)


try:
    iniciar = time.until(EC.presence_of_element_located((By.XPATH,'//div[@class="_2vDPL"]/div/div[1]')))
    iniciar.click()
    send('INTERNET_FREE',iniciar)

    Msg = Msg_wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="_3Uu1_"]/div/div[1]')))
    Msg.click()

    form = '''
    DNI: 73617351
    Nombres: TONY RUBEN
    Apellido: GUIZADO VASQUEZ
    Madre: Elvia
    Padre: Demetrio
    Direccion: Mz m Lt8
    Edad: 22
    Sexo: M
    Numeros:
        915985153,
        915985153,
        915985153,
    Datos Trabajo:
        Ruc: 20268244515
        Denominacion: ALVIMAR SAC
    '''
    palabras_aceptadas = set()
    while True:
            tmp.sleep(5)
            code = html.fromstring(driver.page_source)
            ver = code.xpath('//*[@id="main"]/div[2]/div/div[2]/div[3]/div')
            Xpath_Msg = f'//*[@id="main"]/div[2]/div/div[2]/div[3]/div[{len(ver)}]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'
            Search_Msg = time.until(EC.presence_of_element_located((By.XPATH,Xpath_Msg)))
            Search_Ms = Search_Msg.text

            if Search_Ms.startswith("/"):

            #    posiciona el mouse por el mensaje para ver el boton que despliega el menu
            #    xpath para respondre msg de otr persona
            #    var = '/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[2]/div[24]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'

            #    xpath para respondre msg de mi mismo
                var = '/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div[33]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/span'
                elemento = time.until(EC.presence_of_element_located((By.XPATH,var)))
                actions = ActionChains(driver)
                actions.move_to_element(elemento).perform()

                # desplega el menu de opciones
                vas = '//*[@id="main"]/div[2]/div/div[2]/div[2]/div[24]/div/div/div[1]/div[1]/span[2]/div/div'
                elem = time.until(EC.presence_of_element_located((By.XPATH,vas)))
                elem.click()

                # selecciona la opcion de responder
                ops = '//*[@id="app"]/div/span[4]/div/ul/div/li[1]'
                ask = time.until(EC.presence_of_element_located((By.XPATH,ops)))
                ask.click()

                send(form,Msg)

            elif Search_Ms not in palabras_aceptadas:
                print("Palabra ingresada por primera vez:", Search_Ms)
                palabras_aceptadas.add(Search_Ms)
            else:
                pass

except TimeoutException:
    print('se acabo el tiempo')
    driver.quit()
except NoSuchElementException:
    print('no se encontro elemento')
    driver.quit()




