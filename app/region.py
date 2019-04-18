# region.py = stuff for regions

from typing import ClassVar, Dict, Any

from bozen.bztypes import HtmlStr

import mark
import entity
from allpages import app, jinjaEnv

#---------------------------------------------------------------------

class Region(entity.Entity):
    
    docs: ClassVar[Dict[str, 'Region']] = {}
    
    @classmethod
    def makeRegion(cls, id, name, **kwargs) -> 'Region':
        r = Region(id, name, **kwargs)
        cls.docs[id] = r
        return r
    
    def blurb(self) -> HtmlStr:
        """ Text on the region from the (md) markdown """
        md = self.md
        h = martk.render(md)
        return h
    
def reg(id, name, **kwargs):
    return Region.makeRegion(id, name, **kwargs)

#---------------------------------------------------------------------

@app.route('/region/<id>')
def region(id):
    r = Region.getDoc(id)
    tem = jinjaEnv.get_template("region.html")
    h = tem.render(
        id = id,
        r = r,
    )
    return h

#---------------------------------------------------------------------

reg("scot", "Scotland", seats=6,
md="""\
**Scotland** is the only region where the SNP stands.
""")

reg("ni", "Northern Ireland", seats=3,
md="""\
**Northern Ireland** uses a different electiral system than the rest of the UK;
it uses STV whereas everyone else uses closed party lists.    
""") 

reg("nee", "NE England", seats=3,
md="""\
**North East England**
""")   

#---------------------------------------------------------------------

if __name__=='__main__':
    print(Region.docs)

#end