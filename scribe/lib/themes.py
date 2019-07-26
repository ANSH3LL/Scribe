class Thematics(object):
    def __init__(self):
        self.themedict = {'snkf' : self.snarchkoff,
                          'frut' : self.fruity}

    def get_theme(self, theme_name, colordict):
        return self.themedict[theme_name](colordict)

    def snarchkoff(self, colordict):
        if colordict.get('COMMENT'):
            return 'comment', '#3d17ea'
        elif colordict.get('BUILTIN'):
            return 'builtin', '#e91e63'
        elif colordict.get('STRING'):
            return 'string', '#008b00'
        elif colordict.get('KEYWORD'):
            return 'keyword', '#ff5722'
        elif colordict.get('EXTRA'):
            return 'extra', '#1e1'
        elif colordict.get('NUMBER'):
            return 'number', '#2196f3'
        elif colordict.get('FUNCDEF'):
            return 'funcdef', '#ff9800'
        elif colordict.get('CLASSDEF'):
            return 'classdef', '#ff9800'
        elif colordict.get('HEXBIN'):
            return 'hexbin', '#2196f3'
        elif colordict.get('URL'):
            return 'url', '#009688'
        elif colordict.get('FKW'):
            return 'fkw', '#4caf50'
        elif colordict.get('EMAIL'):
            return 'email', '#8bc34a'
        else:
            return 'none', 'NONE'

    def fruity(self, colordict):
        if colordict.get('COMMENT'):
            return 'comment', '#008800'
        elif colordict.get('BUILTIN'):
            return 'builtin', '#009688'
        elif colordict.get('STRING'):
            return 'string', '#0086d2'
        elif colordict.get('KEYWORD'):
            return 'keyword', '#fb660a'
        elif colordict.get('EXTRA'):
            return 'extra', '#444444'
        elif colordict.get('NUMBER'):
            return 'number', '#0086f7'
        elif colordict.get('FUNCDEF'):
            return 'funcdef', '#ff0086'
        elif colordict.get('CLASSDEF'):
            return 'classdef', '#ff0086'
        elif colordict.get('HEXBIN'):
            return 'hexbin', '#0086f7'
        elif colordict.get('URL'):
            return 'url', '#ff0086'
        elif colordict.get('FKW'):
            return 'fkw', '#ff0007'
        elif colordict.get('EMAIL'):
            return 'email', '#cdcaa9'
        else:
            return 'none', 'NONE'
