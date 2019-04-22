# mark.py = interface to python markdown

import sys
import re
from typing import List, Tuple

import markdown
from markdown.extensions import extra, sane_lists

from bozen.butil import dpr

#---------------------------------------------------------------------

markdownProcessor = markdown.Markdown(extensions=[
    'extra',
    'sane_lists',
    'toc',
    ])

def render(s: str) -> str:
    """ Render markup into HTML also return tags
    (this version doesn't process tags)
    @return:str = rendered html
    """
    markdownProcessor.reset()
    h = markdownProcessor.convert(s)
    return h

#end
