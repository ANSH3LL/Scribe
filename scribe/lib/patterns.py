import keyword
import __builtin__

class RegexMachine(object):
    def __init__(self):
        self.magicvars = '__bases__|__class__|__closure__|__code__|__defaults__|__dict__|__doc__|__file__|__func__|__globals__|__metaclass__|__module__|__mro__|__name__|__self__|__slots__|__weakref__'

    def _any(self, name, alternates):
        return '(?P<%s>' % name + '|'.join(alternates) + ')'

    def _pyregex(self):
        kw = r"\b" + self._any("KEYWORD", keyword.kwlist) + r"\b"
        builtinlist = [str(name) for name in dir(__builtin__) if not name.startswith('_')]
        builtinlist.remove('print')
        builtin = r"(\b)" + self._any("BUILTIN", builtinlist) + r"\b"
        comment = self._any("COMMENT", [r"#[^\n]*"])
        extra = self._any("EXTRA", [r"(self|cls|@[^\n]*|%s)(\b|^)" %(self.magicvars)])
        num = self._any("NUMBER", [r"\b[0-9\.]*"])
        hexbin = self._any("HEXBIN", [r"0[xX][a-fA-F0-9]+|0[bB][01]+"])
        stringprefix = r"(\br|u|ur|R|U|UR|Ur|uR|b|B|br|Br|bR|BR)?"
        sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
        dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
        sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
        dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
        string = self._any("STRING", [sq3string, dq3string, sqstring, dqstring])
        return kw + "|" + builtin + "|" + comment + "|" + string + "|" + extra + "|" + hexbin + "|" + num

    def _figregex(self):
        kw = r"\b" + self._any("KEYWORD", keyword.kwlist) + r"\b"
        builtinlist = [str(name) for name in dir(__builtin__) if not name.startswith('_')]
        builtinlist.remove('print')
        builtin = r"(\b)" + self._any("BUILTIN", builtinlist) + r"\b"
        comment = self._any("COMMENT", [r"#[^\n]*"])
        extra = self._any("EXTRA", [r"\b;"])
        num = self._any("NUMBER", [r"\b[0-9\.]*"])
        email = self._any("EMAIL", [r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"])
        fkw = self._any("FKW", [r"\$PY\$:"])
        url = self._any("URL", [r"((file\:|mailto|(ht|f)tp(s?)\://){1}\S+|((www)\.){1}\S+)"])
        hexbin = self._any("HEXBIN", [r"0[xX][a-fA-F0-9]+|0[bB][01]+"])
        stringprefix = r"(\br|u|ur|R|U|UR|Ur|uR|b|B|br|Br|bR|BR)?"
        sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
        dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
        sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
        dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
        string = self._any("STRING", [sq3string, dq3string, sqstring, dqstring])
        return kw + "|" + builtin + "|" + comment + "|" + string + "|" + url + "|" + email + "|" + fkw + "|" + extra + "|" + hexbin + "|" + num

    def _txtregex(self):
        comment = self._any("COMMENT", [r"#|\*|\+|~|\^|\(|\)|\[|\]|\{|\}"])
        num = self._any("NUMBER", [r"\b[0-9\.]*"])
        email = self._any("EMAIL", [r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"])
        url = self._any("URL", [r"((file\:|mailto|(ht|f)tp(s?)\://){1}\S+|((www)\.){1}\S+)"])
        hexbin = self._any("HEXBIN", [r"0[xX][a-fA-F0-9]+|0[bB][01]+"])
        return comment + "|" + email + "|" + url + "|" + hexbin + "|" + num
