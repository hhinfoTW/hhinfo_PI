import configparser
class ServerModel:
    token = ''
    token_key = ''
    serverip = ''
    serverport = ''
    VPNserverip = ''
  
 
  
    
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read("config.ini")
        self.token = cf.get("ServerConfig", "token")
        self.token_key = cf.get("ServerConfig", "token_key")
        self.serverip = cf.get("ServerConfig", "serverip")
        self.serverport = cf.get("ServerConfig", "serverport")
        self.VPNserverip = cf.get("ServerConfig", "VPNserverip")
        self.show()
    def show(self):
        print("__________ServerModel show__________")
        print("token = " + self.token)
        print("token_key = " + self.token_key)
        print("serverip = " + self.serverip)
        print("serverport = " + self.serverport)
        print("VPNserverip = " + self.VPNserverip)
   
      
       