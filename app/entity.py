# entity.py = entities in memory

from typing import Iterator, Union

from bozen.butil import dpr, printargs, htmlEsc, attrEsc, form
from bozen.bztypes import HtmlStr
from bozen import (FormDoc, IntField, StrField)

#---------------------------------------------------------------------

"""
An entity is a bit like a MonDoc, but in memory (not in a database)
"""

class Entity(FormDoc):
    
    _id = StrField(desc="unique identifier of entity")
    name = StrField(desc="short name of entity")
    longName = StrField(desc="long name of entity")
    
    def __init__(self, id: str, name: str, **kwargs):
        super().__init__(**kwargs)
        self._id = id
        self.name = name
        
    def __repr__(self) -> str:
        """ string for debugging """
        s = "<%s %s %r" % (self.__class__.__name__, self._id, self.name)
        fieldSet = set(self.__dict__.keys())
        extraFields = sorted(list(fieldSet - set(['_id', 'name'])))
        for fn in extraFields:
            fv = self.__dict__[fn]            
            s += " %s=%r" % (fn, fv)
        #//for    
        s += ">"
        return s
          
    def getName(self) -> str:
        if self.name: return self.name
        return self._id
          
    def getNameH(self) -> HtmlStr:
        """ name, html-encoded """       
        return htmlEsc(self.getName())
    
    def getLongName(self) -> str:
        if self.longName: return self.longName
        if self.name: return self.name
        return self._id
                
    def getLongNameH(self) -> HtmlStr:
        """ long name, html-encoded """       
        return htmlEsc(self.getLongName())

    @classmethod
    def stub(cls) -> str:
        n = cls.__name__
        return n[:1].lower() + n[1:]

    def url(self) -> str:
        """
        The URL at which this entity can be accessed in the web app.
        By convention this is /{stub}/{_id} 
        where stub = the class name but with the 1st character in 
        lower case.
        """
        u = form("/{}/{}", self.stub(), self._id)
        return u
    
    @classmethod
    def classLogo(cls) -> HtmlStr:
        """ A logo for the document, for example using Font Awesome or 
        a similar web logo collection. If a logo is used, insert a space 
        after it unless you want it to be right next to the text 
        describing the document.
        """
        return ""

    def logo(self) -> HtmlStr:
        """ Override to make the logo different by instance.
        """
        return self.classLogo()
    
    def a(self, includeLogo=True) -> HtmlStr:
        """Return an a-href for an entity """
        if includeLogo:
            logo = self.logo()
        else:
            logo = ""
        h = "<a href='%s'>%s%s</a>" % (attrEsc(self.url()),
            logo, self.getNameH())
        return h

    @classmethod
    def all(cls) -> Iterator['Entity']:
        """ return all entities of this class """  
        keys = sorted(cls.docs.keys())
        for key in keys:
            yield cls.docs[key]
            
    @classmethod
    def getDoc(cls, id) -> Union['Entity',None]:
        if id in cls.docs:
            return cls.docs[id] 
        else:
            return None



#---------------------------------------------------------------------


#end
