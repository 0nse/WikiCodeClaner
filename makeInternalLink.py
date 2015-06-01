#!/usr/bin/python
# -*- coding: utf-8 -*-
from findBalanced import findBalanced
import re

# WikiLinks
# See https://www.mediawiki.org/wiki/Help:Links#Internal_links

# Can be nested [[File:..|..[[..]]..|..]], [[Category:...]], etc.
# Also: [[Help:IPA for Catalan|[andora]]]

def replaceInternalLinks(text):
    """
    Replaces external links of the form:
    [[title |...|label]]trail

    with title concatenated with trail, when present, e.g. 's' for plural.
    """
    # call this after removal of external links, so we need not worry about
    # triple closing ]]].
    cur = 0
    res = ''

    # Match tail after wikilink
    tailRE = re.compile('\w+')

    for s,e in findBalanced(text, ['[['], [']]']):
        m = tailRE.match(text, e)
        if m:
            trail = m.group(0)
            end = m.end()
        else:
            trail = ''
            end = e
        inner = text[s+2:e-2]
        # find first |
        pipe = inner.find('|')
        if pipe < 0: # omit if only a link
            label = ""
        else:
            title = inner[:pipe].rstrip()
            # find last |
            curp = pipe+1
            for s1,e1 in findBalanced(inner, ['[['], [']]']):
                last = inner.rfind('|', curp, s1)
                if last >= 0:
                    pipe = last # advance
                curp = e1
            label = inner[pipe+1:].strip()
        res += text[cur:s] + label + trail
        cur = end
    return res + text[cur:]
