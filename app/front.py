# front.py = front page

from bozen.butil import pr, prn, form

from allpages import app, jinjaEnv
import config
import region

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
    for r in region.Region.all():
        h += form("""<tr>
    <td>{a}</td>
    <td>{seats}</td>
</tr>""",
            a = r.a(),
            seats = r.seats,
        )
    #//for r  
    h += "</table>"
    return h

#---------------------------------------------------------------------

@app.route('/links')
def links():
    tem = jinjaEnv.get_template("links.html")
    h = tem.render(
    )
    return h


# end
