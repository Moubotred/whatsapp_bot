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
# from v1_test_unitario import seeker
import pandas as pd
import requests
import re


def send(x,iniciar):
    name = list(x)
    for x in name:
        iniciar.send_keys(x)
    iniciar.send_keys(Keys.RETURN)

def seeker(DNI):
    web = 'http://158.69.119.209/seek/index.php?view=mostrar&cod='
    url = web+DNI
    site = requests.get(url)

    code = html.fromstring(site.content)

    NOMBRE_APELLIDO = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[1]/h2/text()')
    SEPARACION = NOMBRE_APELLIDO[0].split()
    APELLDOS = ' '.join(SEPARACION[-2:])

    NOMBRE_APELLIDO[0] = ' '.join(SEPARACION[:-2])
    NOMBRE = NOMBRE_APELLIDO[0]

    SEXO = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[2]/p[3]/text()')[0]
    EDAD = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[2]/p[2]/text()')[0]
    FECHA = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[2]/p[1]/text()')[1]

    UBIGEO_NACIMIENTO = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[3]/p[3]/text()')[0]
    ESTADO = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[2]/p[4]/text()')[0]

    PADRE = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[2]/p[5]/text()')[0]
    MADRE = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[2]/p[6]/text()')[0]
    DIRECCION = code.xpath('/html/body/div[2]/div[1]/div/div[1]/div[2]/div[3]/p[2]/text()')[0]

    NUMERO = code.xpath('/html/body/div[2]/div[4]/div/div[2]/div[3]/table/tbody/tr/td/text()')

    df = pd.DataFrame([NUMERO[i:i+3] for i in range(0, len(NUMERO), 3)], columns=['Teléfono', 'Operador', 'Periodo'])

    datos = f'''
    • DOCUMENTO: {DNI}
    • NOMBRE: {NOMBRE}
    • APELLIDOS: {APELLDOS}
    • GENERO: {SEXO}

    [✅] NACIMIENTO:

    • FECHA: {FECHA}
    • EDAD: {EDAD}
    • UBIGEO NACIMIENTO: {UBIGEO_NACIMIENTO}

    [✅] PADRES:

    • PADRE: {PADRE}
    • MADRE: {MADRE}

    [✅] GENERALES:

    • ESTADO CIVIL: {ESTADO}
    • DIRECCION: {DIRECCION}

             NUMEROS
    {df.to_string(index=False)}
    '''

    return datos



profile_path = r'C:\Users\upset\AppData\Roaming\Mozilla\Firefox\Profiles\0vwq2jcr.default-release-1'
options=Options()
options.add_argument("-profile")
options.add_argument(profile_path)
options.add_argument('--headless')
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
                        dak = seeker(dni)
                        send(dak,Msg)
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
                        dako = seeker(dni)
                        send(dako,Msg)
                    else:
                        send('⚠️ el comando no contiene 8 digitos',Msg)
                        pass
                    
        except TimeoutException:
            print('no es texto')

except NoSuchElementException:
    print('se acabo el tiempo')
    driver.quit()