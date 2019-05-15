# front.py = front page

from bozen.butil import pr, prn, form

from allpages import app, jinjaEnv
from ht import boolH
import config
import region
import party

#---------------------------------------------------------------------

@app.route('/')
def front():
    tem = jinjaEnv.get_template("front.html")
    h = tem.render(
        adminSiteExists = config.CREATE_ADMIN_SITE,
        adminSitePrefix = config.ADMIN_SITE_PREFIX,
    )
    return h

#---------------------------------------------------------------------

@app.route('/regions')
def regions():
    tem = jinjaEnv.get_template("regions.html")
    h = tem.render(
        table = regionTable(),
    )
    return h

def regionTable():
    h = """<table class='bz-report-table'>
<tr>
    <th>Region</th>
    <th>Seats</th>
</tr>
"""
    totSeats = 0
    rs = sorted(region.Region.all(), key = lambda r: r.ix)
    for r in rs:
        h += form("""<tr>
    <td>{a}</td>
    <td style='text-align:right'>{seats}</td>
</tr>""",
            a = r.a(),
            seats = r.seats,
        )
        totSeats += r.seats
    #//for r  
    h += form("""<tr style='font-weight:bold'>
    <td>TOTAL</td>
    <td style='text-align:right'>{seats}</td>
</tr>""",
            seats = totSeats,
    )
    h += "</table>"
    return h

#---------------------------------------------------------------------

@app.route('/gbparties')
def gbparties():
    tem = jinjaEnv.get_template("gbparties.html")
    h = tem.render(
        table=gbPartyTable(),
    )
    return h

def gbPartyTable() -> str:
    h = """<table class='bz-report-table'>
<tr>
    <th>Abbrev</th>
    <th>Party<br>Name</th>
    <th>% Vote,<br>2014</th>
    <th>Seats,<br>2014</th>
    <th>Regions</th>
    <th>Remain<br>in EU?</th>
    <th>Notes</th>
</tr>
"""
    totSeats = 0
    ps = sorted(party.Party.all(), key = lambda p: p.ix)
    for p in ps:
        h += form("""<tr>
    <td>{a}</td>
    <td><span style='color:{col}'><i class='fa fa-certificate'></i></span>
        {longName}</td>
    <td style='text-align:right'>{votes14:.1f}</td>
    <td style='text-align:right'>{seats14}</td>
    <td>{regs}</td>
    <td>{isRemain}</td>
    <td></td>
</tr>""",
            a = p.a(),
            col = p.col,
            longName = p.getLongNameH(),
            votes14 = p.votes14,
            seats14 = p.seats14,
            regs = p.regs,
            isRemain = boolH(p.isRemain),
        )

    #//for p
    h += "</table>"
    return h
    

#---------------------------------------------------------------------

@app.route('/niparties')
def niparties():
    tem = jinjaEnv.get_template("niparties.html")
    h = tem.render(
        table="",
    )
    return h

#---------------------------------------------------------------------

@app.route('/links')
def links():
    tem = jinjaEnv.get_template("links.html")
    h = tem.render(
    )
    return h

#---------------------------------------------------------------------

@app.route('/robots.txt')
def robotsTxt():
    h = """\
User-agent: *
Disallow:
"""    
    return h

#---------------------------------------------------------------------


# end
