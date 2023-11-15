from pathlib import Path
import datetime
import time

class repo:
    def __init__(self, address):
        self.addr = Path(address)
    @property
    def file(self):
        return self.addr / 'logyourself.log'
    def decorateLog(self, line):
        return f"[{datetime.datetime.now().isoformat()}]  {line}\n"
    def log(self, string:str):
        with self.open() as f :
            f.write(self.decorateLog(string))
            f.close()
    def open(self):
        return open(self.file,'a+')
    def read(self):
        with open(self.file,'r+') as f:
            dist = f.read()
            f.close()
            return dist