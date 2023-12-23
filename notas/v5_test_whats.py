import re
import time as tmp
from lxml import html
from selenium import webdriver
from root import WHATS,MODEL,USER
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from lib_ import send,seeker,Buscar_DNI_por_Nombres,Disney


class whastapp:
    def __init__(self,search):
        self.search = search 

    def server(self,driver,Msg,identify,user_search):
        #>>>>>>>>----------[BUSCA EL ULTMIMO MENSAJE ENVIADO WHATSAPP]--------------------------<<<<<<<<
        try:
            Xpath_Msg = identify
            tim = WebDriverWait(driver,10)
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
            if Search_Ms.startswith("/dni") and len(value_cmd) == 8:
                print(user+value_cmd) 
                if len(value_cmd) == 8:
                    # print(value_cmd)
                    dako = seeker(value_cmd)
                    send(dako,Msg)
                else:
                    send('⚠️ el comando no contiene 8 digitos',Msg)


            elif Search_Ms.startswith("/name"):
                if value_cmd:
                    print(user+value_cmd) 
                    # print(value_cmd)
                    nombre_P_M = Buscar_DNI_por_Nombres(value_cmd)
                    send(nombre_P_M,Msg)
                else:
                    send('⚠️ el comando es invalido',Msg)

            elif Search_Ms.startswith("/disney"):
                account = Disney()
                send(account,Msg)
            else:
                pass
        except NoSuchElementException and TimeoutException:
            print('generacion de error')
            pass

    def update_msg(self,driver):
        tmp.sleep(2)
        code = html.fromstring(driver.page_source)
        xpath_elements_div = code.xpath(WHATS().FRAGMENT)
        count_elements_div = len(xpath_elements_div)
        return count_elements_div

    def main(self,driver,Msg):
        while True:
            count_elements_div = self.update_msg(driver)
            try:
                self.server(driver,Msg,MODEL(count_elements_div).MSG_UPDATE_CLIENT,USER(MODEL(count_elements_div).count).USER_CLIENT)
            except NoSuchElementException and TimeoutException:
                self.server(driver,Msg,MODEL(count_elements_div).MSG_UPDATE_SERVER,USER(MODEL(count_elements_div).count).USER_SERVER)
                
    def run(self):        
        # C:\Users\nimun\AppData\Roaming\Mozilla\Firefox\Profiles\tped0zt5.automata

        # C:\Users\upset\AppData\Roaming\Mozilla\Firefox\Profiles\n1c9fewx.automata
        profile_path = r'C:\Users\nimun\AppData\Roaming\Mozilla\Firefox\Profiles\tped0zt5.automata'
        options=Options()
        options.add_argument("-profile")
        options.add_argument(profile_path)
        # options.add_argument('--headless')

        driver = webdriver.Firefox(options=options)
        driver.get('https://web.whatsapp.com/')
        Msg_wait = WebDriverWait(driver,60)
        tim = WebDriverWait(driver,10)

        try:
            start = Msg_wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="_2vDPL"]/div/div[1]')))
            start.click()
            send(self.search,start)

            Msg = Msg_wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="_3Uu1_"]/div/div[1]')))
            Msg.click()
            send(WHATS().BANNER,Msg)

            self.main(driver,Msg)

        except TimeoutException:
            print('se acabo el tiempo')
            driver.quit()
# w = whastapp('INTERNET_FREE')
# w.run()