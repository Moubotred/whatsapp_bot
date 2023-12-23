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
import re


def send(x,iniciar):
    name = list(x)
    for x in name:
        iniciar.send_keys(x)
    iniciar.send_keys(Keys.RETURN)


profile_path = r'C:\Users\upset\AppData\Roaming\Mozilla\Firefox\Profiles\n1c9fewx.automata'
options=Options()
options.add_argument("-profile")
options.add_argument(profile_path)
#options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

driver.get('https://web.whatsapp.com/')
time = WebDriverWait(driver,60)
Msg_wait = WebDriverWait(driver,60)
tim = WebDriverWait(driver,10)


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

    # busca los elemntos div de texto y ver cuantos de divs hay
    # dependiendo de eso uso ese numero para ver el texto dentro 
    # de de otro xpath que muestra el texto

    # tmp.sleep(5)
    # code = html.fromstring(driver.page_source)
    # xpath_elements_div = code.xpath('/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div')
    # count_elements_div = len(xpath_elements_div)
    # print(count_elements_div)

    xpath_principal = '/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div'

    texto = set()
    while True:
        try:
            tmp.sleep(5)
            code = html.fromstring(driver.page_source)
            # xpath_elements_div = code.xpath('/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div')
            xpath_elements_div = code.xpath(xpath_principal)
            count_elements_div = len(xpath_elements_div)

            Xpath_Msg = xpath_principal+f'[{count_elements_div}]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'
            # Xpath_Msg = f'/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div[{count_elements_div}]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'
            Search_Msg = tim.until(EC.presence_of_element_located((By.XPATH,Xpath_Msg)))
            Search_Ms = Search_Msg.text

            # print(Search_Ms)

            if Search_Ms.startswith("/dni"):
                # print('comando acepatado')
                try:
                    users = xpath_principal+f'[{count_elements_div}]/div/div/div[1]/div[2]/div[1]/div/div[2]'
                    Search_M = tim.until(EC.presence_of_element_located((By.XPATH,users)))
                    mio = Search_M.get_attribute("data-pre-plain-text")
                    patron = r'\[(.*?)\] (.*)'
                    Expresion = re.search(patron,mio)
                    user = Expresion.group(2) 
                    dni = Search_Ms[5:]

                    if len(dni) == 8:
                        print(user+dni) # print(coincidencia.group(1))
                        send(form,Msg)
                    else:
                        send('⚠️ el comando no contiene 8 digitos',Msg)
                        pass

                except TimeoutException:
                    mi_user = xpath_principal+f'/div/div/div[1]/div[1]/div[1]/div/div[1]'
                    Search_M = tim.until(EC.presence_of_element_located((By.XPATH,mi_user)))
                    mio = Search_M.get_attribute("data-pre-plain-text")
                    patron = r'\[(.*?)\] (.*)'
                    Expresion = re.search(patron,mio)
                    user = Expresion.group(2) 
                    dni = Search_Ms[5:]

                    if len(dni) == 8:
                        print(user+dni) # print(coincidencia.group(1))
                        send(form,Msg)
                    else:
                        send('⚠️ el comando no contiene 8 digitos',Msg)
                        pass

        except TimeoutException:
            print('no es texto')

except NoSuchElementException:
    print('se acabo el tiempo')
    driver.quit()