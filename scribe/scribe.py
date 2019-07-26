import re

import ttk
import tkMessageBox
import tkSimpleDialog
from Tkinter import *

from lib import *

class Scribe(Text):
    '''Flexible and highly functional, code highlighting text editor with line numbers and support for many other cool features.\nA downside is that it may be slow when dealing with large pieces of highlighted code.It's also quite glitchy.\nYou have been warned.'''
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.filter = None
        self.pfilter = False
        self.theme = 'snkf'
        self.opfile = 'None'
        self.config(wrap = 'none', undo = True)
        self.createpopup()
        self.bind('<3>', self.showpopup)
        self.bind('<KeyRelease>', self.colorize)
        self.bind('<Return>', self.spacify)
        self.bind('<Tab>', self.indent)
        self.bind('<F5>', self.runcode)
        self.bind('<Alt-g>', self.goto)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)
        self.bind('<Control-a>', self.selectall)
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-y>', self.redo)
        self.bind('<Control-o>', self.openfile)
        self.bind('<Control-s>', self.savefile)
        self.bind('<1>', lambda _:self.tag_remove('gtl', '1.0', 'end'))
        self.bind('<3>', lambda _:self.tag_remove('gtl', '1.0', 'end'), add = '+')
        self.defkw = re.compile(r'(?P<FUNCDEF>def\s+(\w+)\S)')
        self.clskw = re.compile(r'(?P<CLASSDEF>class\s+(\w+)\S)')
        self.ifilter = re.compile(r'.+\:')

        self.fileman = fileio.Librarian()
        self.rexman = patterns.RegexMachine()
        self.enforcecolor = themes.Thematics()
        
        self.yscrollframe = Frame(self.master)
        self.yscroll = ttk.Scrollbar(self.yscrollframe, orient = 'vertical', cursor = 'arrow', command = self.yview)
        self.config(yscrollcommand = self.yscroll.set)
        self.yscrollframe.pack(side = 'right', fill = 'y')
        self.yscroll.pack(expand = True, fill = 'y')

        self.xscrollframe = Frame(self.master)
        self.xscroll = ttk.Scrollbar(self.xscrollframe, orient = 'horizontal', cursor = 'arrow', command = self.xview)
        self.config(xscrollcommand = self.xscroll.set)
        self.xscrollframe.pack(side = 'bottom', fill = 'x')
        self.xscroll.pack(expand = True, fill = 'x')

        self.lnframe = Frame(self.master)
        self.linenotify = linenos.LineCanvas(self.lnframe)
        self.linenotify.subscribe(self)
        self.lnframe.pack(side = 'left', fill = 'y')
        self.linenotify.pack(expand = True, fill = 'y')
        self.add_intercept()
        self.bind('<Configure>', self.linenotify.update)
        self.bind('<<Changed>>', self.linenotify.update)
        self.bind('<KeyRelease>', self.linenotify.update, add = '+')

    def add_intercept(self):
        self.tk.eval('''
proc widget_interceptor {widget command args} {

set orig_call [uplevel [linsert $args 0 $command]]

if {
    ([lindex $args 0] == "insert") ||
    ([lindex $args 0] == "delete") ||
    ([lindex $args 0] == "replace") ||
    ([lrange $args 0 2] == {mark set insert}) || 
    ([lrange $args 0 1] == {xview moveto}) ||
    ([lrange $args 0 1] == {xview scroll}) ||
    ([lrange $args 0 1] == {yview moveto}) ||
    ([lrange $args 0 1] == {yview scroll})} {

    event generate  $widget <<Changed>>
   }

   #return original command
   return $orig_call
}
''')
        self.tk.eval('''
rename {widget} new
interp alias {{}} ::{widget} {{}} widget_interceptor {widget} new
'''.format(widget = str(self)))

    def copy(self, event = None):
        self.event_generate('<<Copy>>')
        self.colorize()
        return 'break'

    def cut(self, event = None):
        self.event_generate('<<Cut>>')
        self.colorize()
        return 'break'

    def paste(self, event = None):
        self.event_generate('<<Paste>>')
        self.colorize()
        return 'break'

    def selectall(self, event = None):
        self.tag_add('sel', '1.0', 'end-1c')
        self.mark_set('insert', 'end-1c')
        #self.see("insert")
        return 'break'

    def undo(self, event = None):
        try:
            self.edit_undo()
        except TclError:
            pass
        else:
            self.colorize()
        return 'break'

    def redo(self, event = None):
        try:
            self.edit_redo()
        except TclError:
            pass
        else:
            self.colorize()
        return 'break'

    def goto(self, event = None):
        lineno = tkSimpleDialog.askinteger('Go to Line', 'Type a line number and press Enter:')
        try:
            assert isinstance(lineno, int) and lineno > 0
        except AssertionError:
            self.focus_set()
        else:
            self.mark_set('insert', '%d.0' % (lineno))
            self.tag_add('gtl', 'insert linestart', 'insert lineend+1c')
            self.tag_config('gtl', background = '#eeeeee')
            self.see('insert')
            self.focus_set()

    def spacify(self, event = None):
        data = self.get('insert linestart', 'end')
        if self.ifilter.match(data):
            self.insert('insert', '\n')
            self.insert('insert', ' ' * 4)
            return 'break'

    def indent(self, event = None):
        self.insert('insert', ' ' * 4)
        return 'break'

    def openfile(self, event = None):
        self.opfile, actxt = self.fileman.acquire()
        if actxt:
            self.delete('1.0', 'end')
            self.insert('1.0', actxt)
            self.colorize()
        else:
            pass
        return 'break'

    def savefile(self, event = None):
        data = self.get('1.0', 'end')
        #Strip worthless newlines at end of file and replace with one to comply w/ pep8 standards
        data = data.rstrip()
        data += '\n'
        sfpth = self.fileman.shelve(self.opfile, data)
        if sfpth:
            self.opfile = sfpth
            return True
        else:
            tkMessageBox.showerror('Failed to save file', 'No filename was given')
            return False

    def runcode(self, event = None):
        if self.opfile[-3:] == '.py':
            run = execution.Executor()
            self.savefile()
            run.execute(self.opfile)
        elif self.opfile == 'None':
            if self.savefile():
                self.runcode()
        else:
            tkMessageBox.showerror('Unable to run file', 'Only saved python files can be executed')

    def createpopup(self):
        self.popup = Menu(self, tearoff = 0)
        self.popup.add_command(label = 'Copy', command = self.copy)
        self.popup.add_command(label = 'Cut', command = self.cut)
        self.popup.add_command(label = 'Paste', command = self.paste)
        self.popup.add_command(label = 'Undo', command = self.undo)
        self.popup.add_command(label = 'Redo', command = self.redo)
        self.popup.add_separator()
        self.popup.add_command(label = 'Select All', command = self.selectall)

    def showpopup(self, event = None):
        self.config(cursor = 'arrow')
        self.mark_set('insert', '@%d, %d' %(event.x, event.y))
        self.popup.tk_popup(event.x_root, event.y_root)
        self.config(cursor = 'ibeam')

    def select_theme(self, theme):
        if theme in self.enforcecolor.themedict:
            self.theme = theme
        else:
            pass #Silently

    def addfilter(self, wfilter):
        if wfilter == 'py':
            self.filter = re.compile(self.rexman._pyregex(), re.DOTALL)
            self.pfilter = True
        elif wfilter == 'fig':
            self.filter = re.compile(self.rexman._figregex(), re.DOTALL)
            self.pfilter = True
        elif wfilter == 'txt':
            self.filter = re.compile(self.rexman._txtregex(), re.DOTALL)
        else:
            pass

    def _coordinate(self, start, end, string):
        srow = string[:start].count('\n') + 1
        scolsplitlines = string[:start].split('\n')
        if len(scolsplitlines) != 0:
            scolsplitlines = scolsplitlines[len(scolsplitlines) - 1]
        scol = len(scolsplitlines)
        lrow = string[:end + 1].count('\n') + 1
        lcolsplitlines = string[:end].split('\n')
        if len(lcolsplitlines) != 0:
            lcolsplitlines = lcolsplitlines[len(lcolsplitlines) - 1]
        lcol = len(lcolsplitlines) + 1
        return '{}.{}'.format(srow, scol), '{}.{}'.format(lrow, lcol)

    def coordinate(self, pattern, string, txt):
        line = string.splitlines()
        start = string.find(pattern)
        end = start + len(pattern)
        srow = string[:start].count('\n') + 1
        scolsplitlines = string[:start].split('\n')
        if len(scolsplitlines) != 0:
            scolsplitlines = scolsplitlines[len(scolsplitlines) - 1]
        scol = len(scolsplitlines)
        lrow = string[:end + 1].count('\n') + 1
        lcolsplitlines = string[:end].split('\n')
        if len(lcolsplitlines) != 0:
            lcolsplitlines = lcolsplitlines[len(lcolsplitlines) - 1]
        lcol = len(lcolsplitlines)
        return '{}.{}'.format(srow, scol),'{}.{}'.format(lrow, lcol)

    def colorize(self, event = None):
        if self.filter:
            text = self.get('1.0', 'end')
            if len(text) == 1:
                return
            for x in ['comment', 'builtin', 'string', 'keyword', 'extra', 'hexbin', 'number', 'funcdef', 'classdef', 'url', 'fkw', 'email']:
                self.tag_remove(x, '1.0', 'end')
            if not self.filter:
                return
            for x in self.filter.finditer(text):
                start = x.start()
                end = x.end() - 1
                tagtype, colour = self.enforcecolor.get_theme(self.theme, x.groupdict())
                if colour != 'NONE':
                    y, z = self._coordinate(start, end, text)
                    self.tag_add(tagtype, y, z)
                    self.tag_config(tagtype, foreground = colour)
                    #Cool formatting features dependent on tagtype
                    if tagtype == 'extra':
                        self.tag_config(tagtype, font = 'consolas 12 italic')
                    elif tagtype == 'fkw':
                        self.tag_config(tagtype, font = 'consolas 12 italic')
                    elif tagtype == 'email':
                        self.tag_config(tagtype, font = 'consolas 12 underline')
                    elif tagtype == 'url':
                        self.tag_config(tagtype, font = 'consolas 12 underline')
                    else:
                        pass

            if self.pfilter:
                for x in self.defkw.finditer(text):
                    start = x.span()[0] + 3
                    end = x.span()[1] - 2
                    word = text[start:end]
                    tagtype, colour = self.enforcecolor.get_theme(self.theme, {'FUNCDEF': word})
                    if colour != 'NONE':
                        y, z = self._coordinate(start, end, text)
                        self.tag_add(tagtype, y, z)
                        self.tag_config(tagtype, foreground = colour)

                for x in self.clskw.finditer(text):
                    start = x.span()[0] + 5
                    end = x.span()[1] - 2
                    word = text[start:end]
                    tagtype, colour = self.enforcecolor.get_theme(self.theme, {'CLASSDEF': word})
                    if colour != 'NONE':
                        y, z = self._coordinate(start, end, text)
                        self.tag_add(tagtype, y, z)
                        self.tag_config(tagtype, foreground = colour)
            else:
                pass
        else:
            pass
