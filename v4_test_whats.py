from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from v1_test_unitario import send,seeker,Buscar_DNI_por_Nombres
from lxml import html
import time as tmp
import re

profile_path = r'C:\Users\upset\AppData\Roaming\Mozilla\Firefox\Profiles\0vwq2jcr.default-release-1'
options=Options()
options.add_argument("-profile")
options.add_argument(profile_path)
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

driver.get('https://web.whatsapp.com/')
# time = WebDriverWait(driver,60)
Msg_wait = WebDriverWait(driver,60)
tim = WebDriverWait(driver,10)

try:
    iniciar = Msg_wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="_2vDPL"]/div/div[1]')))
    iniciar.click()
    send('operraros',iniciar)

    Msg = Msg_wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="_3Uu1_"]/div/div[1]')))
    Msg.click()

    xpath_principal = '/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div'

    while True:
        #>>>>>>>>----------[ACTUALIZA EL ULTIMO NUMERO DE MENSAJES DEL CHAT]------------------------<<<<<<<<
        tmp.sleep(2)
        code = html.fromstring(driver.page_source)
        xpath_elements_div = code.xpath(xpath_principal)
        count_elements_div = len(xpath_elements_div)
        #>>>>>>>>----------======================================================-------------------<<<<<<<<

        try:
            #>>>>>>>>----------[BUSCA EL ULTMIMO MENSAJE ENVIADO WHATSAPP]--------------------------<<<<<<<<
            Xpath_Msg = xpath_principal+f'[{count_elements_div}]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/span[1]/span'
            Search_Msg = tim.until(EC.presence_of_element_located((By.XPATH,Xpath_Msg)))
            Search_Ms = Search_Msg.text
            #>>>>>>>>----------======================================================----------------<<<<<<<<
            
            #>>>>>>>>----------[SECCION DE BUSQUEDA DE MI NOMBRE DE USUARIO DE WHATSAPP]-------------<<<<<<<<
            users = xpath_principal+f'[{count_elements_div}]/div/div/div[1]/div[2]/div[1]/div/div[2]'
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
            else:
                pass
            #>>>>>>>>----------======================================================-----------------<<<<<<<<S

        except TimeoutException:

            #>>>>>>>>----------[BUSCA EL ULTMIMO MENSAJE ENVIADO WHATSAPP]--------------------------<<<<<<<<
            # /html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div[33]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span
            # /html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div[35]/div/div/div/div[1]/div[1]/div[1]/div[2]/div
            # 
            try:
                Xpath_Msg = xpath_principal+f'[{count_elements_div}]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'
                Search_Msg = tim.until(EC.presence_of_element_located((By.XPATH,Xpath_Msg)))
                Search_Ms = Search_Msg.text
                #>>>>>>>>----------======================================================----------------<<<<<<<<

                #>>>>>>>>----------[SECCION DE BUSQUEDA DE MI NOMBRE DE USUARIO DE WHATSAPP]-------------<<<<<<<<
                mi_user = xpath_principal+f'[{count_elements_div}]/div/div/div[1]/div[1]/div[1]/div/div[1]'
                Search_M = tim.until(EC.presence_of_element_located((By.XPATH,mi_user)))
                mio = Search_M.get_attribute("data-pre-plain-text")
                #>>>>>>>>----------======================================================----------------<<<<<<<<

                #>>>>>>>>-------[ELIMINA ELEMENTOS INCESARIO DE LA LISTA DE NOMBRE DE USUARIO]------------<<<<<<<<
                patron = r'\[(.*?)\] (.*)'
                Expresion = re.search(patron,mio)
                user = Expresion.group(2) 
                #>>>>>>>>----------======================================================----------------<<<<<<<<

                #>>>>>>>>--------------------[SEPRARACION DEL COMANDO Y SU VALOR]------------------------<<<<<<<<
                value_cmd = Search_Ms[5:]
                #>>>>>>>>----------======================================================-----------------<<<<<<<<S

                #>>>>>>>>----------[COMANDO ADMITIDOS]----------------<<<<<<<<
                if Search_Ms.startswith("/dni") and len(value_cmd) == 8:
                    if len(value_cmd) == 8:
                        print(user+value_cmd) 
                        # print(value_cmd)
                        dako = seeker(value_cmd)
                        send(dako,Msg)
                    else:
                        send('⚠️ el comando es invalido',Msg)

                elif Search_Ms.startswith("/name"):
                    if value_cmd:
                        print(user+value_cmd) 
                        # print(value_cmd)
                        nombre_P_M = Buscar_DNI_por_Nombres(value_cmd)
                        send(nombre_P_M,Msg)
                    else:
                        send('⚠️ el comando es invalido',Msg)
                else:
                    pass
                #>>>>>>>>----------======================================================-----------------<<<<<<<<S
            except TimeoutException:
                pass

except NoSuchElementException:
    print('se acabo el tiempo')
    driver.quit()