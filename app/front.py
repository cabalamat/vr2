# front.py = front page

from allpages import app, jinjaEnv
from bozen.butil import pr, prn

import config

prn("*** front.py ***")

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
    )
    return h


#---------------------------------------------------------------------

@app.route('/links')
def links():
    tem = jinjaEnv.get_template("links.html")
    h = tem.render(
    )
    return h


# end
