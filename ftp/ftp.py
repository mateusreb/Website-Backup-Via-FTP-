from ftplib import FTP, all_errors

class MyFtp:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def Connect(self):   
        try:
            self.connection = FTP(self.host)     
            self.connection.encoding = "utf-8"        
            return self.connection.login(user = self.username, passwd = self.password)      
        except all_errors as error:
            return str(format(error))
           
    def Disconnect(self):  
        try:
            self.connection.quit()
        except all_errors as error: 
            print(format(error))

    def GetWelcome(self):        
        return self.connection.getwelcome()

    def Mlds(self, folder):
        data = []
        try:
            for file_data in self.connection.mlsd(folder):
                data.append(file_data)
        except all_errors as error: 
                print(format(error))
                return []                         
        return data

    def List(self, directory):
        data = []
        while not data:
            data = self.Mlds(directory) 
            if data:
                return data               
            else:                
                self.Disconnect()
                self.Connect()
    
    def GetServerFolders(self, folder):    
        data = []    
        paths = self.List(folder)    
        while len(paths) > 0:
            old_paths = paths
            paths = []
            for path_name, info in old_paths:                        
                if info["type"] == "dir":                
                    data.append(path_name)                    
                    for name, info in self.List(path_name):
                        if info["type"] == "dir":                                                
                            next_path = []
                            next_path.append(path_name + "/" + name)
                            next_path.append(info)                        
                            paths.append(next_path)
        return data

    def GetServerFiles(self, folder):    
        data = []    
        paths = self.List(folder)    
        while len(paths) > 0:
            old_paths = paths
            paths = []
            for index_name, info in old_paths:                        
                if info["type"] == "file":  
                    data.append({"path" : "", "file" : index_name, "type" : info["type"], "size" : info["size"], "modify" : info["modify"], "unique" : info["unique"] })                       
                elif info["type"] == "dir":                    
                    data.append({"path" : index_name, "file" : "", "type" : info["type"], "size" : info["sizd"], "modify" : info["modify"], "unique" : info["unique"] })                                
                    for name, info in self.List(index_name):
                        if info["type"] == "dir":                                                
                            next_path = []
                            next_path.append(index_name + "/" + name)
                            next_path.append(info)                        
                            paths.append(next_path)
                        elif info["type"] == "file":                                 
                            data.append({"path" : index_name, "file" : name, "type" : info["type"], "size" : info["size"], "modify" : info["modify"], "unique" : info["unique"] })
        return data

    def DownloadFile(self, remote, local):
        self.connection.retrbinary("RETR " + remote ,open(local, 'wb').write)