# poll.py

from typing import Iterator, Union, ClassVar, List

import bozen
from bozen.butil import pr, prn, form, htmlEsc
from bozen import BzDate

from allpages import app, jinjaEnv
from ht import boolH
import config
import region
import party

#---------------------------------------------------------------------

@app.route('/polls')
def polls():
    tem = jinjaEnv.get_template("polls.html")
    h = tem.render(
        table = pollTable(),
    )
    return h


def pollTable():
    partyCols = ""
    for p in POLL_PARTIES:
        pa = party.Party.docs[p]
        partyCols += form("<th>{partyName}<br>{logo}</th>", 
            partyName = pa.getNameH(), 
            logo = pa.logo())
    #//for    
    h = form("""<table class='bz-report-table'>
<tr>
    <th>End<br>Date</th>
    <th>Days<br>to Poll</th>
    <th>Polling<br>Org</th>
    {partyCols}
</tr>
""", 
    partyCols = partyCols)
    for po in Poll.polls:
        partyCells = ""  
        for p in POLL_PARTIES:
            partyCells += ("<td style='text-align:right'>%.1f</td>\n" 
                % (po.__dict__[p],))
        h += form("""<tr>
    <td>{date}</td>
    <td style='text-align:right'>{dateInt}</td>
    <td>{org}</td>
    {partyCells}
</tr>""",
            date = htmlEsc(po.date),
            dateInt = po.dateInt,
            org = htmlEsc(po.org),
            partyCells = partyCells)


    #//for    
    
    h += "</table>"
    return h

#---------------------------------------------------------------------

POLL_PARTIES = [
    'ukip',
    'lab',
    'con',
    'ld',
    'grn',
    'brex',
    'chuk'
]
POLLING_DATE = BzDate("2019-05-23")
POLLING_DATE_INT = POLLING_DATE.to_dayInt()

class Poll:
    #========== class stuff ==========
    polls: ClassVar[List['Poll']] = []

    
    #========== instance ==========
    date: BzDate # end date of poll
    dateInt: int # date as integer
    org: str = "" # polling org
    sample: int = 1000 # sample size
    note: str = "" # note on this poll
    
    # vote shares of parties:
    ukip: float = 0
    lab: float = 0
    con: float = 0
    ld: float = 0
    grn: float = 0
    brex: float = 0
    chuk: float = 0
    
    def __init__(self, **kwargs):
        self.decodeArgs(**kwargs)
        self.ix = len(self.polls)
        self.polls.append(self)
        
    def __str__(self):
        s = "(%d) %s %s:" % (self.ix, self.org, self.date)
        for p in POLL_PARTIES:
            s += " %s=%s" % (p, self.__dict__[p])
        return s    
        
    def decodeArgs(self, **kwargs):
        self.date = BzDate(kwargs['date']) # compulsory
        self.dateInt = self.date.to_dayInt() - POLLING_DATE_INT
        self.org = kwargs.get('org', "")
        self.sample =  kwargs.get('sample', 1000)
        self.note = kwargs.get('note', "")
        
        for p in POLL_PARTIES:
            self.__dict__[p] = kwargs.get(p, 0)
        #//for
        
        voteShares = kwargs.get('vs', None)
        if voteShares is not None:
            self.decodeVoteShares(voteShares)
            
    def decodeVoteShares(self, voteShares):
        """ get the vote shares for the pareties from a string """
        vs = voteShares.split()
        if len(vs) != len(POLL_PARTIES): return
        for i in range(len(POLL_PARTIES)):
            p = POLL_PARTIES[i]
            self.__dict__[p] = float(vs[i])
           

def addPoll(**kwargs):
    """ add a new poll """
    po = Poll(**kwargs)
    return po

#---------------------------------------------------------------------

addPoll(
    date="2019-05-12",
    org="ComRes",
    sample=2028,
    vs="3 25 15 13 7 27 6"
)
addPoll(
    date="2019-05-10",
    org="Opinium",
    sample=2004,
    vs="4 21 11 12 8 34 3"
)
addPoll(
    date="2019-05-10",
    org="BMG",
    sample=1541,
    vs="3 22 12 19 10 26 3"
)

# before locals:
addPoll(
    date="2019-04-30",
    org="YouGov",
    sample=1630,
    vs="4 21 13 10 9 30 9"
)
addPoll(
    date="2019-04-26",
    org="YouGov",
    sample=5412,
    vs="5 22 13 7 10 28 10"
)
addPoll(
    date="2019-04-25",
    org="Survation",
    sample=1999,
    vs="7 27 16 8 4 27 10"
)


    



#end
