# region.py = stuff for regions

from typing import ClassVar, Dict, Any

from bozen.bztypes import HtmlStr
from bozen import butil
from bozen import (FormDoc, IntField, StrField, TextAreaField)

import mark
import entity
from allpages import app, jinjaEnv

#---------------------------------------------------------------------

class Region(entity.Entity):
    #========== class stuff ==========
    docs: ClassVar[Dict[str, 'Region']] = {}
    
    @classmethod
    def makeRegion(cls, id, name, **kwargs) -> 'Region':
        r = Region(id, name, **kwargs)
        r.ix = len(cls.docs) + 1
        cls.docs[id] = r
        return r
    
    #========== instance ==========
    #_id = StrField(desc="unique identifier of entity")
    name = StrField(desc="short name of entity")
    longName = StrField(desc="long name of entity")
    seats = IntField(desc="number of seats in region")
    md = TextAreaField(desc="markdown source for text description")
    
    
    def blurb(self) -> HtmlStr:
        """ Text on the region from the (md) markdown """
        md = butil.exValue(lambda: self.md, "")
        h = mark.render(md)
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
**Northern Ireland** uses a different electoral system than the rest of the UK;
it uses STV whereas everyone else uses closed party lists. 

Furthermore, different parties stand in Northern Ireland, compared with
the rest of the UK.
""") 

reg("nee", "NE England", longName="North East England", seats=3,
md="""\
**North East England**
""")   

reg("nwe", "NW England", longName="North West England", seats=8)
reg("york", "Yorkshire", longName="Yorkshire and the Humber", seats=6)

reg("wales", "Wales", seats=4,
md="""**Wales** is the only region where Plaid Cymru stands.
""")

reg("em", "East Midlands", seats=5)
reg("wm", "West Midlands", seats=7)
reg("ee", "East of England", seats=7)
reg("swe", "SW England", longName="South West England", seats=6)
reg("see", "SE England", longName="South East England", seats=10)
reg("london", "London", seats=8)

'''
makeRegion("nee", "NE England", "North East England")
makeRegion("nwe", "NW England", "North West England")
makeRegion("york", "Yorkshire", "Yorkshire and the Humber")
makeRegion("em", "East Midlands")
makeRegion("wm", "West Midlands")
makeRegion("ee", "East of England")
makeRegion("see", "SE England", "South East England")
makeRegion("swe", "SW England", "South West England")
makeRegion("london", "London")
'''

#---------------------------------------------------------------------

if __name__=='__main__':
    print(Region.docs)

#end