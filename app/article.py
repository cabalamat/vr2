# artlcle.py = articles (in markdown)

import os.path

from bozen import butil
from bozen.butil import pr, prn, dpr

from allpages import app, jinjaEnv
import mark

#---------------------------------------------------------------------

ARTICLE_DIR = butil.join(
    os.path.dirname(os.path.abspath( __file__ )), 
    "article")
prn("ARTICLE_DIR=%s", ARTICLE_DIR)

@app.route('/article/<art>')
def article(art):
    mimeType = getMimeType(art)
    if mimeType:
        pan = getPan(art)
        data = open(pan).read()
        return Response(data, mimetype=mimeType)
    
    title, contents = getArticleBody(art)
    tem = jinjaEnv.get_template("article.html")
    h = tem.render(
        art = art,
        title = title,
        wikiText = contents,
    )
    return h

MIME_TYPES = [
   ('pdf', 'application/pdf'),
   ('gif', 'image/gif'),
   ('png', 'image/png'),
   ('jpg', 'image/jpeg'),
   ('jpeg', 'image/jpeg'),
   ('xls', 'application/vnd.ms-excel'),
]

def getMimeType(pathName):
    """ Get the mime type of a pathname
    @param pathName::str
    @return::str containing mime type, or "" if none.
    """
    pnl = pathName.lower()
    for ext, mt in MIME_TYPES:
        ext2 = "." + ext
        if pnl[-len(ext2):]==ext2:
            return mt
    #//for
    return ""

#---------------------------------------------------------------------


def getArticleBody(art: str):
    """ given an article name, return the body of the article.
    @return::(str,str) = title,html
    """
    articlePan = butil.join(ARTICLE_DIR, art + ".md")
    #prvars()
    if butil.fileExists(articlePan):
        src = open(articlePan).read()
        contents = mark.render(src)
        return art, contents
    else:
        h = form("<p>({art} does not exist)</p>\n",
            art = art)
        return (pathName, h)



def getPan(art: str):
    """ return the pathname for a directory
    @param art = the article name
    @return::str = the full pathname to the article 
    """
    return butil.join(ARTICLE_DIR, art)
    return ""

#---------------------------------------------------------------------

#end