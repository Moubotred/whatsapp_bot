from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import pandas as pd
import requests
import time as tmp
from bs4 import BeautifulSoup

# DNI = str(input('dni: '))
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

def Buscar_DNI_por_Nombres(NAME):
    # profile_path = r'C:\Users\upset\AppData\Roaming\Mozilla\Firefox\Profiles\0vwq2jcr.default-release-1'
    WEB = 'https://eldni.com/pe/buscar-por-nombres'
    # busqueda = 'elvia vasquez mendoza'
    busqueda = NAME
    partes = busqueda.split()
    n,m,p = partes[:-2],partes[-1],partes[-2]  

    options = Options()
    # options.add_argument("-profile")
    # options.add_argument(profile_path)
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    driver.get(WEB)

    time = WebDriverWait(driver,10)
    NOMBRES = time.until(EC.presence_of_element_located((By.XPATH,'//*[@id="nombres"]')))
    for i in range(len(n)):
        NOMBRES.send_keys(n[i]+' ')

    APELLIDO_P = time.until(EC.presence_of_element_located((By.XPATH,'//*[@id="apellido_p"]')))
    APELLIDO_P.send_keys(p)

    APELLIDO_M = time.until(EC.presence_of_element_located((By.XPATH,'//*[@id="apellido_m"]')))
    APELLIDO_M.send_keys(m)
    
    Search = time.until(EC.presence_of_element_located((By.XPATH,'//*[@id="btn-buscar-por-nombres"]')))
    Search.click()
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all(['th', 'td'])
        cols = [col.get_text(strip=True) for col in cols]
        data.append(cols)
    df = pd.DataFrame(data)
    try:
        df.columns = ['DNI', 'NOMBRES', 'APELLIDO_P', 'APELLIDO_M']
        return df.to_string(index=False)
    except:
        return '⚠️ no se encotraon resultados'


# Buscar_DNI_por_Nombres()


# Search_Ms = '/name TONY RUBEN GUIZADO VASQUEZ'
# if Search_Ms.startswith("/name"):
#     dni = Search_Ms[5:]
    




































