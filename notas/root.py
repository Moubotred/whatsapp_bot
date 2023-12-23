
class WHATS:
    def __init__(self):
        self.BANNER = '''
__┌-[ Lanzar_cuentas ]--------█
■├ comando /hbo -- NO DISPONIBLE
■├ comando /disney 
└┴
 |
_┌-[ Info ]
■├ comando /dni 
■├ comando: /name
 |
_┌-[ Download yt ]
■├ comando /ytdv -- NO DISPONIBLE
■├ comando /ytda -- NO DISPONIBLE
┴-------------------------------█
                    '''
        self.SEARCH = '//div[@class="_2vDPL"]/div/div[1]'
        self.BOX_MSG = '//div[@class="_3Uu1_"]/div/div[1]'
        self.FRAGMENT = '/html/body/div[1]/div/div/div[5]/div/div[2]/div/div[2]/div[3]/div'

class MODEL(WHATS):
    def __init__(self,count):
        super().__init__()
        self.count = count
        self.MSG_UPDATE_CLIENT = self.FRAGMENT+f'[{self.count}]/div/div/div[1]/div[2]/div[1]/div/div[2]/div/span[1]/span'
        self.MSG_UPDATE_SERVER = self.FRAGMENT+f'[{self.count}]/div/div/div[1]/div[1]/div[1]/div/div[1]/div/span[1]/span'    


class USER(MODEL,WHATS):
    def __init__(self,count):
        super().__init__(count)

        self.USER_CLIENT = self.FRAGMENT+f'[{self.count}]/div/div/div[1]/div[2]/div[1]/div/div[2]'
        self.USER_SERVER = self.FRAGMENT+f'[{self.count}]/div/div/div[1]/div[1]/div[1]/div/div[1]'
    

