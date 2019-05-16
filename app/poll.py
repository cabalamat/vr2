# poll.py

from typing import Iterator, Union, ClassVar, List, Tuple
import json

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
        chartData = json.dumps(pollChartData(), 
            sort_keys=True, indent=4),
        chartOptions = json.dumps(pollChartOptions(), 
            sort_keys=True, indent=4),
    )
    return h


def pollTable() -> str:
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
    allPolls = sorted(Poll.polls, key=lambda po: po.dateInt)
    for po in allPolls:
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

def pollChartData() -> dict:
    """ return data for poll chart, in format for Flot charting
    application
    """
    # polls, sorted earliest first
    allPolls = sorted(Poll.polls, key=lambda po: po.dateInt)
    j = []
    for p in POLL_PARTIES:
        pa = party.Party.docs[p]
        xySeries = []
        dataForTrend = []
        trendSeries = []
        for po in allPolls:
            xySeries.append([po.dateInt, po.__dict__[p]])
            dataForTrend.append(
                (po.dateInt, po.sample, po.__dict__[p]))
            trendSeries.append([po.dateInt, calcTrend(dataForTrend)])
        #//for po 
        series = {
            'label': p,
            'color': pa.col,
            'data': xySeries,
            'points': {'show': True}
        }    
        trendSeries = {
            'color': pa.col,
            'data': removeDuplicateDates(trendSeries),
            'lines': {'show': True, 'lineWidth': 2}
        }    
        j.append(series)
        j.append(trendSeries)
    #//for pa   
    return j

DECAY_HL = 3.5 # half-life, days

def calcTrend(trendData) -> float:
    """
    @param trendData: List[TrendItem]
    TrendItem = Tuple[dateInt:int, sample:int, pollValue]
    """
    currentDate = trendData[-1][0]
    valuesWeights = []
    for trendItem in trendData:
        dateInt, sample, pollValue = trendItem
        value = pollValue
        decayTime = abs(dateInt - currentDate)
        decay = 0.5 ** (decayTime*1.0 / DECAY_HL)
        weight = (sample**0.5)*decay
        valuesWeights.append((value, weight))
    #//for trendItem
    trend = weightedAverage(valuesWeights)
    return trend
    
def weightedAverage(valuesWeights:List[Tuple[float,float]]) -> float:
    total = 0.0
    totalWeight = 0.0
    for value, weight in valuesWeights:
        total += value*weight
        totalWeight += weight
    #//for    
    return total/totalWeight

def removeDuplicateDates(trendSeries):
    """ remove duplicate dates from a trend series """
    result = []
    for dateInt, trend in trendSeries:
        if len(result)>0 and result[-1][0]==dateInt:
            result = result[:-1]
        result.append((dateInt, trend))
    #//for    
    return result

def pollChartOptions() -> dict:
    j = {
        'yaxis': {'min': 0}
    }
    return j



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

#===== latest
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

#===== 9 May:
addPoll(
    date="2019-05-09",
    org="ComRes",
    sample=2034,
    vs="3 25 13 14 8 27 6"
)
addPoll(
    date="2019-05-09",
    org="Survation",
    sample=1303,
    vs="4 24 12 11 6 30 4"
)
addPoll(
    date="2019-05-09",
    org="YouGov",
    sample=2212,
    vs="3 16 10 15 11 34 5"
)

#===== 7 May:
addPoll(
    date="2019-05-07",
    org="Opinium",
    sample=2000,
    vs="4 26 14 12 6 29 2"
)
addPoll(
    date="2019-05-07",
    org="ComRes",
    sample=4060,
    vs="2 26 14 11 6 28 8"
)


#===== before locals:
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

#===== 24 April
addPoll(
    date="2019-04-24",
    org="PanelBase",
    sample=1149,
    vs="5 33 20 7 4 20 5"
)
addPoll(
    date="2019-04-23",
    org="Opinium",
    sample=2004,
    vs="3 28 14 7 6 28 7"
)
addPoll(
    date="2019-04-17",
    org="YouGov",
    sample=1755,
    vs="6 22 17 9 10 23 8"
)

#===== 16 April
addPoll(
    date="2019-04-16",
    org="ComRes",
    sample=1061,
    vs="5 33 18 9 5 17 9"
)
addPoll(
    date="2019-04-16",
    org="YouGov",
    sample=1855,
    vs="7 22 15 9 10 27 6"
)

#===== 12 April
addPoll(
    date="2019-04-12",
    org="Opinium",
    sample=2007,
    vs="13 29 17 10 6 12 4"
)
addPoll(
    date="2019-04-11",
    org="YouGov",
    sample=1843,
    vs="14 24 16 8 8 15 7"
)
addPoll(
    date="2019-04-08",
    org="Hanbury",
    sample=2000,
    vs="7 38 23 8 4 10 4"
)

#===== 30 Mar
addPoll(
    date="2019-03-30",
    org="Opinium",
    sample=2008,
    vs="18 30 24 10 8 0 0"
)


    



#end
