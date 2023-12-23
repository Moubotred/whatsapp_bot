from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge

from hbo_brute_force import sites
from bs4 import BeautifulSoup
from lxml import etree
import time


head = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Vivaldi/"
profile_path = r'C:\Users\upset\AppData\Local\Microsoft\Edge\User Data\Profile 1'

edge_options = EdgeOptions()
edge_options.add_argument("-profile")#uso el privado ya que delete_all_cookies no borra los perfiles
edge_options.add_argument("user-data-dir="+profile_path)
edge_options.use_chromium = True

whatsapp = sites('https://web.whatsapp.com/')
# whatsapp.driver = webdriver.Firefox(options=options)
whatsapp.driver = Edge(executable_path=r"C:\Program Files\msgdriver\msedgedriver",options=edge_options)
whatsapp.driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": head})
whatsapp.driver.get(whatsapp.web)

time.sleep(30)
iniciar = whatsapp.driver.find_element(By.XPATH,'//div[@class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt qh0vvdkp"]')
iniciar.click()
name = ['o','p','e','r','r','a','r','o','s']
for x in name:
    iniciar.send_keys(x)
iniciar.send_keys(Keys.RETURN)
time.sleep(5)

element_html = whatsapp.driver.page_source  # Reemplaza con tu fragmento de HTML

# Crear un nuevo objeto Element a partir del fragmento de HTML
element_root = etree.HTML(element_html)

# Aplicar XPath para buscar elementos dentro del fragmento
ID = element_root.xpath('//div[@class="CzM4m"]/@data-id')  #ID de usuario
chats = element_root.xpath('//div[@class="CzM4m"]/div/div/div/div/div/div[@class="copyable-text"]/div/span/span/text()')# texto chat

result_list = [item[51:-5] for item in ID]
num = len(result_list)
cont = []
for x in range(0,num):
    if len(result_list[x]) == 11:
        rep = result_list[x]
        cont.append(rep)

    if len(result_list[x]) == 12:
        rep = result_list[x][-11:]
        cont.append(rep)

    if len(result_list[x]) == 22:
        rep = result_list[x][11:]
        cont.append(rep)

    if len(result_list[x]) == 23:
        rep = result_list[x][12:]
        cont.append(rep)
    
new_id = cont[26:]
new_chat = chats[14:]

print(new_id)
print(new_chat)


#//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[1]
time.sleep(3)

#div._3Uu1_

#'div._3ndVb.fbgy3m38.ft2m32mm.oq31bsqd.nu34rnf1'
div_element = whatsapp.driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]')
div_element.send_keys('mensaje')
div_element.send_keys(Keys.RETURN)



# name = ['o','p','e','n','-','s','e','r','v','e','r']
# for x in name:
#     div_element.send_keys(x)
# div_element.send_keys(Keys.RETURN)

# if new_chat == "/info":
    # cmd = whatsapp.driver.find_element(By.XPATH,'#//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[1]')
    # cmd.send_keys('respodiedo bot -----'+Keys.RETURN)



whatsapp.driver.quit()