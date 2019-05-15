# party.py = stuff for parties

from typing import ClassVar, Dict, Any

from bozen.bztypes import HtmlStr
from bozen.butil import pr, prn, form, htmlEsc
from bozen import butil

import mark
import entity
from allpages import app, jinjaEnv

#---------------------------------------------------------------------

class Party(entity.Entity):
    #========== class stuff ==========
    
    docs: ClassVar[Dict[str, 'Party']] = {}
    
    @classmethod
    def makeParty(cls, id, name, **kwargs) -> 'Party':
        r = Party(id, name, **kwargs)
        r.ix = len(cls.docs) + 1
        cls.docs[id] = r
        return r
    
    #========== instance ==========
    isRemain: bool = False
    regs: str = "" # gb|ni|scot|wales
    votes14: float = 0.0 # vote % in 2014
    seats14: int = 0 # seats in 2014
    col: str = "#666" # colour (from wikipedia)
    notes: str = "" # notes
    
    def logo(self) -> str:
        """ return the party's logo """
        s = form("<span style='color:{col}'>"
            "<i class='fa fa-certificate'></i></span> ",
            col = self.col)
        return s
    
def par(id, name, **kwargs):
    return Party.makeParty(id, name, **kwargs)

#---------------------------------------------------------------------
# Parties

par("grn", "Grn", longName="Greens", 
    isRemain=True,
    regs="gb",
    col="#6AB023",
    votes14=7.6, seats14=3,
    md="""\
*Green* refers to the Green Party of England and Wales, and the 
Scottish Green Party, separate parties that share the Green ideology.
""")

par("lab", "Lab", longName="Labour Party", 
    isRemain=False,
    regs="gb",
    col="#DC241f",
    votes14=24.4, seats14=20,
    md="""\
The Labour Party [manifesto](https://labour.org.uk/issue/negotiating-brexit/) 
(accessed 25 April 2019) says:

> Labour accepts the referendum result and a Labour government 
> will put the national interest first.

Labour is thus a leave party.
""")

par("ld", "LD", longName="Liberal Democrats", 
    isRemain=True,
    regs="gb",
    col="#FAA61A",
    votes14=6.6, seats14=1,
    md="""\
""")

par("chuk", "ChUK", longName="Change UK", 
    isRemain=True,
    regs="gb",
    col="#3C3C3B",
    votes14=0, seats14=0,
    md="""\
""")

par("con", "Con", longName="Conservative Party", 
    isRemain=False,
    regs="gb",
    col="#0087DC",
    votes14=23.1, seats14=19,
    md="""\
""")

par("brex", "Brex", longName="Brexit Party", 
    isRemain=False,
    regs="gb",
    col="#12B6CF",
    votes14=0, seats14=0,
    md="""\
The **Brexit Party** was founded in 2019 by Nigel Farage.    
""")

par("ukip", "UKIP", longName="United Kingdom Independence Party", 
    isRemain=False,
    regs="gb",
    col="#70147A",
    votes14=26.6, seats14=24,
    md="""\
""")

par("snp", "SNP", longName="Scottish National Party", 
    isRemain=True,
    regs="scot",
    col="#FEF987",
    votes14=2.4, seats14=2,
    md="""\
""")

par("pc", "PC", longName="Plaid Cymru", 
    isRemain=True,
    regs="wales",
    col="#008142",
    votes14=0.7, seats14=1,
    md="""\
""")


#---------------------------------------------------------------------


#end

