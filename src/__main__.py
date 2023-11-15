from settings import settings
from shell import shell as baseShell, KeepShell, Command
from repo import repo
class shell(baseShell):
    def __init__(self,app):
        super().__init__()
        self.app = app
    @baseShell.itsCommand
    def help (self, name, args):
        ...
    @Command('/using <repoAddress|repoName> # uses a repo')
    def using(self, name, args):
        self.app.setUse(args[0])
    @baseShell.itsCommand
    def log (self,name,args):
        string = ' '.join(args)
        self.app.inUse.log(string)
    @Command('')
    def show(self, name, args):
        print(self.app.inUse.read())
    def parseCommand(self, String: str):
        #String = String[1:]
        return super().parseCommand(String)
    def lap(self):
        dist = self.input()
        if len(dist.strip()) == 0 :
            commandString = 'show'
        else:
            if dist.strip()[0] == '/':
                commandString = dist.strip()[1:]
            else :
                commandString = f'logThenShow {dist}'
        self.execute(*self.parseCommand(commandString))
    @Command('')
    def logThenShow(self, name, args):
        self.log('log',args)
        self.show('show',args)

class application:
    def __init__(self):
        if hasattr(settings,'DEFAULT_REPO'):
            self.use(settings.DEFAULT_REPO)
    def use(self,repoName):
        self._inUse = repo( settings.REPOS[repoName] )
    @property
    def inUse(self):
        if not self._inUse :
            raise KeepShell(f'''
First use a repo
HINT: {shell.using.desc}
HINT: /repos # lists all repos you added and you can use
HINT: /add <name> <clonedRepoAddress> # adds a repo
                            ''')
        return self._inUse    
if __name__ == '__main__':
    app = application()
    appshell = shell(app)
    appshell.run()