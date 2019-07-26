import os
import tkFileDialog

class Librarian(object):
    def __init__(self):
        pass

    def acquire(self):
        acquisition = tkFileDialog.askopenfilename(filetypes = [('python files', '.py .pyw'), ('fig files', '.fig'), ('text files', '.txt'), ('all files', '.*')])
        if acquisition:
            with open(acquisition, 'r') as acquisitor:
                data = acquisitor.read()
            return acquisition, data
        return 'None', None

    def shelve(self, fname, data):
        if os.path.exists(fname):
            requisition = fname
        else:
            requisition = tkFileDialog.asksaveasfilename(defaultextension = '.py')
        if requisition:
            with open(requisition, 'w') as requisitor:
                requisitor.write(data)
            return requisition
        return None
