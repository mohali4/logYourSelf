from platform import system as __system
import os
from pathlib import Path
import json
import logging
from typing import Any

class SettingModel :
    def __init__(self, dictionary):
        if isinstance(dictionary, list|tuple):
            self.__fromList(dictionary)
        elif isinstance(dictionary, dict):
            self.__fromDict(dictionary)
        self.dictionary:dict
    def __fromList(self, List):
        self.__fromDict( {
            f"{num}":val for num,val in zip(range(len(List)),List)
        } )
    def __fromDict(self,Dict):
        self.dictionary = {
            str(key):val  for key, val in Dict.items()
        }
    def __getattribute__(self, __name: str) -> Any:
        try: return super().__getattribute__(__name)
        except AttributeError as e :
            try:
                return self.__resume( self.dictionary[__name] )
            except KeyError:
                if self.__isUpper(__name):
                    return None
                raise e
    def __getitem__(self,__name):    
        return self.__resume(self.dictionary.get(str(__name)))
    def __resume(self,Object):
        if isinstance(Object,list|dict|tuple):
            return type(self)(Object)
        return Object
    def __isUpper(self,String:str):
        return String == String.upper()


_os = __system()
match _os:
    case 'Linux':
        settingFile = os.environ.get('LYS_SETTING_FILE')
        if not settingFile :
            prefix = os.environ.get('PREFIX', '')
            settingFile = f'{prefix}/etc/lys/config.json'
        settingFile = Path(settingFile)
    case 'Windows':
        pass
with open(settingFile,'r') as f:
    dist = f.read()
    try :
        dictionary = json.loads(dist)
    except:
        logging.error(f'''
Unvallid setting file [{settingFile}] 
HINT: try setup LYS_SETTING_FILE in environmet, see https://www3.ntu.edu.sg/home/ehchua/programming/howto/Environment_Variables.html''')
        quit(code=1)
settings = SettingModel(
        dictionary
    )