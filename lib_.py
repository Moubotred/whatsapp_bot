from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from root import WHATS,MODEL,USER
from lxml import html
import pandas as pd
import time as tmp
import requests
import random
import re

class cmd:
    def __init__(self):
        pass

    def seeker(self,DNI):
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

    def Buscar_DNI_por_Nombres(self,NAME):
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

    def Disney(self):
        accounts = []
        with open('account.txt','r') as tmp:
            read_accounts = tmp.read().splitlines()
            for i in read_accounts:
                accounts.append(read_accounts)
            rand_account = random.choice(accounts[0])
            return rand_account



class whats:
    def __init__(self):
        pass

    def send(self,x,iniciar):
        name = list(x)
        for x in name:
            iniciar.send_keys(x)
        iniciar.send_keys(Keys.RETURN)

    def update_msg(self,driver):
        tmp.sleep(2)
        code = html.fromstring(driver.page_source)
        xpath_elements_div = code.xpath(WHATS().FRAGMENT)
        count_elements_div = len(xpath_elements_div)
        return count_elements_div

    def server(self,driver,Msg,identify,user_search):
        s = cmd()
        tim = WebDriverWait(driver,10)
        #>>>>>>>>----------[BUSCA EL ULTMIMO MENSAJE ENVIADO WHATSAPP]--------------------------<<<<<<<<
        Xpath_Msg = identify
        Search_Msg = tim.until(EC.presence_of_element_located((By.XPATH,Xpath_Msg)))
        Search_Ms = Search_Msg.text
        #>>>>>>>>----------======================================================----------------<<<<<<<<
        
        #>>>>>>>>----------[SECCION DE BUSQUEDA DE MI NOMBRE DE USUARIO DE WHATSAPP]-------------<<<<<<<<
        users = user_search
        Search_M = tim.until(EC.presence_of_element_located((By.XPATH,users)))
        mio = Search_M.get_attribute("data-pre-plain-text")
        #>>>>>>>>----------======================================================----------------<<<<<<<<

        #>>>>>>>>-------[ELIMINA ELEMENTOS INCESARIO DE LA LISTA DE NOMBRE DE USUARIO]------------<<<<<<<
        patron = r'\[(.*?)\] (.*)'
        Expresion = re.search(patron,mio)
        user = Expresion.group(2) 
        #>>>>>>>>----------======================================================----------------<<<<<<<<
        value_cmd = Search_Ms[5:]
        #>>>>>>>>----------[COMANDO ADMITIDOS]----------------<<<<<<<<
        if Search_Ms.startswith("/dni"):
            if len(value_cmd) == 8:
                dako = s.seeker(value_cmd)
                self.send(dako,Msg)
                print(user+' '+value_cmd)
            else:
                self.send('⚠️ el comando no contiene 8 digitos',Msg)

        elif Search_Ms.startswith("/name"):
            if value_cmd:
                nombre_P_M = s.Buscar_DNI_por_Nombres(value_cmd)
                self.send(nombre_P_M,Msg)
                print(user+' '+value_cmd)

        elif Search_Ms.startswith("/disney"):
            account = s.Disney()
            self.send(account,Msg)
            print(user+' '+account)
        else:
            pass

    def main(self,ID):
        profile_path = r'C:\Users\upset\AppData\Roaming\Mozilla\Firefox\Profiles\0vwq2jcr.default-release-1'
        options=Options()
        
        options.add_argument("-profile")
        options.add_argument(profile_path)

        driver = webdriver.Firefox(options=options)

        driver.get('https://web.whatsapp.com/')
        time = WebDriverWait(driver,60)

        try:
            iniciar = time.until(EC.presence_of_element_located((By.XPATH,WHATS().SEARCH)))
            iniciar.click()
            self.send(ID,iniciar)

            Msg = time.until(EC.presence_of_element_located((By.XPATH,WHATS().BOX_MSG)))
            Msg.click()

            self.send(WHATS().BANNER,Msg)

            while True:
                count_elements_div = self.update_msg(driver)
                try:
                    self.server(driver,Msg,MODEL(count_elements_div).MSG_UPDATE_CLIENT,USER(MODEL(count_elements_div).count).USER_CLIENT)

                except TimeoutException:
                    self.server(driver,Msg,MODEL(count_elements_div).MSG_UPDATE_SERVER,USER(MODEL(count_elements_div).count).USER_SERVER)

        except TimeoutException:
            pass
        pass

