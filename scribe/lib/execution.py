import os

class Executor(object):
    def __init__(self):
        pass

    def execute(self, executable):
        os.chdir(os.path.dirname(executable))
        os.system('mode 150 && python -t "%s" && pause' %(executable))#pause so we can see output(if any)
