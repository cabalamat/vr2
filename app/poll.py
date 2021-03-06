# poll.py

from typing import Iterator, Union, ClassVar, List, Tuple
import json

import bozen
from bozen.butil import pr, prn, dpr, form, htmlEsc
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
    chartData, partyStrengths = pollChartData()
    partyLegend = getPartyLegend(partyStrengths)
    h = tem.render(
        table = pollTable(),
        chartData = json.dumps(chartData, 
            sort_keys=True, indent=4),
        chartOptions = json.dumps(pollChartOptions(), 
            sort_keys=True, indent=4),
        partyLegend = partyLegend,
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
    <th>Sample<br>Size</th>
    {partyCols}
</tr>
""", 
    partyCols = partyCols)
    allPolls = sorted(Poll.polls, key=lambda po: po.dateInt)
    for po in allPolls:
        partyCells = ""  
        for p in POLL_PARTIES:
            pa = party.Party.docs[p]
            partyCells += ("<td style='text-align:right;color:%s'"
                ">%.1f</td>\n" 
                % (pa.col, po.__dict__[p],))
        h += form("""<tr>
    <td>{date}</td>
    <td style='text-align:right'>{dateInt}</td>
    <td>{org}</td>
    <td style='text-align:right'>{sample}</td>
    {partyCells}
</tr>""",
            date = htmlEsc(po.date),
            dateInt = po.dateInt,
            org = htmlEsc(po.org),
            sample = htmlEsc(str(po.sample)),
            partyCells = partyCells)


    #//for    
    
    h += "</table>"
    return h

PARTY_X_ADJ = [-0.25, 0.0, 0.25, -0.25, 0.0, 0.0, 0.0]

def pollChartData() -> dict:
    """ return data for poll chart, in format for Flot charting
    application
    """
    # polls, sorted earliest first
    allPolls = sorted(Poll.polls, key=lambda po: po.dateInt)
    j = []
    partyStrengths = []
    for p, xAdj in zip(POLL_PARTIES, PARTY_X_ADJ):
        pa = party.Party.docs[p]
        xySeries = []
        dataForTrend = []
        trendSeries = []
        for po in allPolls:
            xySeries.append([po.dateInt+xAdj, po.__dict__[p]])
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
        j.append({
            'data': [[0,0]],
            #'points': {'show': True}
        })    
        partyStrengths.append({
            'name': pa.getNameH(),    
            'color': pa.col,
            'strength': trendSeries['data'][-1][1]
        })    
    #//for pa   
    j.append({
        'data': [[0,0]],
        #'points': {'show': True}
    })  
    dpr("partyStrengths=%r", partyStrengths)
    return j, partyStrengths

DECAY_HL = 3.0 # half-life, days

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
        weight = sample*decay
        #weight = (sample**0.5)*decay
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

def getPartyLegend(partyStrengths) -> str:
    """ return HTML to go at the top of the chart showing 
    parties, in order of their trend strength, with percentage 
    and color.
    """
    # sort, largest 1st
    ps2 = sorted(partyStrengths, key=lambda ps: ps['strength'])[::-1]
    
    dpr("ps2=%r", ps2)
    h = ""
    for ps in ps2:
        dpr("ps=%r", ps)
        name = ps['name']
        color = ps['color']
        strength = ps['strength']
        h += form("""<span style='color:{color}'>
            {strength:.1f}% {name}</span>&nbsp; """,
            color = color,
            strength = strength,
            name = name)       
    #//for   
    dpr("h=%s", h)
    return h

def pollChartOptions() -> dict:
    j = {
        'yaxis': {'min': 0},
        'xaxis': {'max': 0,
                  'tickSize': 7}
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

#===== 22 May
addPoll(
    date="2019-05-22",
    org="Survation",
    sample=2029,
    ukip=3,
    lab=23,
    con=14,
    ld=12,
    grn=7,
    brex=31,
    chuk=4,
)
addPoll(
    date="2019-05-22",
    org="BMG",
    sample=1601,
    ukip=2,
    lab=18,
    con=12,
    ld=17,
    grn=8,
    brex=35,
    chuk=4,
)
addPoll(
    date="2019-05-22",
    org="Ipsos MORI",
    sample=1527,
    ukip=3,
    lab=15,
    con=9,
    ld=20,
    grn=10,
    brex=35,
    chuk=3,
)

#===== 21 May
addPoll(
    date="2019-05-21",
    org="YouGov",
    sample=3864,
    vs="3 13 7 19 12 37 4"
)
addPoll(
    date="2019-05-21",
    org="Number Cruncher",
    sample=1005,
    ukip=2,
    lab=19,
    con=15,
    ld=16,
    grn=7,
    brex=33,
    chuk=4,
)
addPoll(
    date="2019-05-21",
    org="Kantar",
    sample=2316,
    ukip=4,
    lab=24,
    con=13,
    ld=15,
    grn=8,
    brex=27,
    chuk=5,
)
addPoll(
    date="2019-05-21",
    org="Panelbase",
    sample=2033,
    vs="3 25 12 15 7 30 3"
)

#===== 20 May
addPoll(
    date="2019-05-20",
    org="Opinium",
    sample=1000,
    ukip=2,
    lab=17,
    con=12,
    ld=15,
    grn=7,
    brex=38,
    chuk=3,
)

#===== 17 May
addPoll(
    date="2019-05-17",
    org="Survation",
    sample=1000,
    vs="3 24 14 12 4 30 3"
)
addPoll(
    date="2019-05-17",
    org="ComRes",
    sample=4161,
    vs="3 22 12 14 7 32 5"
)
addPoll(
    date="2019-05-17",
    org="YouGov",
    sample=9260,
    vs="3 15 9 17 11 34 4"
)

addPoll(
    date="2019-05-16",
    org="ComRes",
    sample=2041,
    vs="2 23 9 16 9 31 4"
)
addPoll(
    date="2019-05-16",
    org="Opinium",
    sample=2009,
    vs="2 20 12 15 6 34 3"
)
addPoll(
    date="2019-05-16",
    org="YouGov",
    sample=7192,
    vs="3 15 9 16 10 35 5"
)
addPoll(
    date="2019-05-13",
    org="Hanbury",
    sample=2000,
    vs="3 25 13 14 6 30 6"
)

#===== 12 May
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




    



#end
