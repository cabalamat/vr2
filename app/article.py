# artlcle.py = articles (in markdown)

import os.path

from bozen import butil
from bozen.butil import pr, prn, dpr, form

from allpages import app, jinjaEnv
import mark

#---------------------------------------------------------------------

ARTICLE_DIR = butil.join(
    os.path.dirname(os.path.abspath( __file__ )), 
    "article")

#---------------------------------------------------------------------


@app.route('/articles')
def articles():
    """ return list of articles """
    tem = jinjaEnv.get_template("articles.html")
    h = tem.render(
        articleList = getArticles(),
    )
    return h

def getArticles():
    articleFns = butil.getFilenames(ARTICLE_DIR, "*.md")
    dpr("ARTICLE_DIR=%r", ARTICLE_DIR)
    dpr("articleFns=%r", articleFns)
    h = ""
    for afn in articleFns:
        title = getTitle(butil.join(ARTICLE_DIR, afn))
        dpr("afn=%r title=%r", afn, title)
        h += form("<p><a href='/article/{art}'>"
            "<i class='fa fa-file-text-o'></i> {title}</a></p>\n",
            art = afn[:-3],
            title = title)
    #//for
    return h

#---------------------------------------------------------------------

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

def getTitle(pan: str) -> str:
    """ get the title of an article
    @param pan = full pathname to the article
    """
    src = open(pan).read()
    lines = src.split("\n")
    if len(lines)==0: return ""
    t = mark.render(lines[0].strip(" #"))
    if t.startswith("<p>"): t = t[3:]
    if t.endswith("</p>"): t = t[:-4]
    return t

#---------------------------------------------------------------------

#end
