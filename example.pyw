import scribe
from Tkinter import *

root = Tk()
root.geometry('800x500+250+100')
x = scribe.Scribe(root, bg = '#111111', fg = '#bdbdbd', insertbackground = '#bdbdbd', font = 'consolas', selectbackground = '#bdbdbd', selectforeground = '#000')#bg = '#1e1e1e'
x.pack(expand = True, fill = 'both')
x.focus_set()
x.addfilter('py')
root.mainloop()
