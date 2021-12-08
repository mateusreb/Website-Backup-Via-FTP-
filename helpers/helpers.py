import os

class Helpers:
    @staticmethod
    def CreateDir(path):
        try:
            os.mkdir(os.getcwd() + "/storage" + path)
        except OSError:
            return False
        else:
            return True
    
    @staticmethod
    def GetCurDir():
        return os.getcwd()
