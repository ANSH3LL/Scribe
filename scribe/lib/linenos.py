from Tkinter import Canvas

class LineCanvas(Canvas):
    '''Support class for Scribe meant to provide line number support.'''
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.twidget = None
        self.config(bg = '#000', highlightbackground = '#000')

    def subscribe(self, twidget):
        self.twidget = twidget

    def update(self, event = None):
        self.delete('all')
        currline = self.twidget.index('@0, 0')
        while True:
            line = self.twidget.dlineinfo(currline)
            if not line:
                break
            #x = line[0]
            y = line[1]
            linenum = str(currline).split('.')[0]
            #Resize according to number of lines present
            if int(linenum) >= 0:
                self.config(width = 15)
            if int(linenum) >= 10:
                self.config(width = 25)
            if int(linenum) >= 100:
                self.config(width = 35)
            if int(linenum) >= 1000:
                self.config(width = 45)
            if int(linenum) >= 10000:
                self.config(width = 55)
            if int(linenum) >= 100000:
                self.config(width = 65)
            if int(linenum) >= 1000000:
                self.config(width = 75)
            if int(linenum) >= 10000000:
                self.config(width = 85)
            if int(linenum) >= 100000000:
                self.config(width = 95)
            #Create text showing line number
            self.create_text(2, y, text = linenum, fill = '#bdbdbd', font = 'Consolas 12 italic', anchor = 'nw')#(x, y...
            currline = self.twidget.index('%s+1line' %(currline))
