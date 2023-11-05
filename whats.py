import re 
import time as tmp
from lxml import html
from selenium import webdriver
from root import WHATS,MODEL,USER
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from v1_test_unitario import send,seeker,Buscar_DNI_por_Nombres,Disney


def update_msg(driver):
    tmp.sleep(2)
    code = html.fromstring(driver.page_source)
    xpath_elements_div = code.xpath(WHATS().FRAGMENT)
    count_elements_div = len(xpath_elements_div)
    return count_elements_div

def server(driver,Msg,identify,user_search):
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




# driver = ''
# Msg = ''
# client = server(driver,Msg,MODEL().MSG_UPDATE_CLIENT,USER().USER_CLIENT)
# serv = server(driver,Msg,MODEL().MSG_UPDATE_SERVER,USER().USER_SERVER)