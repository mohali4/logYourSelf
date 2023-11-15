import logging

class CommandError(Exception):
    pass
class ShellExit(Exception):
    pass
class KeepShell(Exception):
    pass

def Command(desc):
    def decorate(func):
        setattr(func,'IS_COMMAND',True)
        setattr(func,'desc',desc)
        return func
    return decorate

class shell :
    point = ':) '
    
    @classmethod
    def itsCommand(cls,func):
        setattr(func,'IS_COMMAND',True)
        return func

    def __init__(self):
        self.inputLetterNum = 0
    def print(self):
        print(self.point,end='')
        self.inputLetterNum += len(self.point)
    def input(self):
        self.print()
        com = input()
        print('\r'+' '*self.inputLetterNum,end='')
        self.inputLetterNum=0
        return com
    def execute (self, command:str, args:tuple):
        handler = self.findHandler(command)
        try:
            handler(command,args)
        except ShellExit as e:
            raise e
        except Exception as e :
            logging.error(e.__str__())
    def findHandler(self,command:str):
        handler = getattr(self,command,None)
        if not handler or not getattr(handler,'IS_COMMAND',False) :
            return self.default
        return handler
    def default(self, name, args):
        raise CommandError(
            f'Unknown command {name}'
        )
    def parseCommand(self,String:str):
        String = String.split('#')[0]
        if String.strip() == '':
            return 'none', tuple()
        split = String.split()
        command = split[0]
        try:
            args = tuple(split[1:])
        except:
            args = tuple()
        return command, args
    def lap (self):
        commandString = self.input()
        command, args = self.parseCommand(commandString)
        self.execute(command,args)
    def run (self):
        while True:
            try:
                self.lap()
            except ShellExit :
                return
            except KeepShell as e :
                logging.error(e.__str__())
            except Exception as e:
                raise e
    @Command('')
    def none(self, name, args):
        return
    @Command('')
    def exit(self, name, args):
        raise ShellExit()
    @Command('')
    def quit(self,*args):
        self.exit(*args)

