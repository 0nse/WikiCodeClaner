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

    Furthermore, link texts' of links referring to Category:Relisted AfD Debates
    will be ignored.
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
            label = processPotentialWikiLink(inner, '').strip()
        else:
            title = inner[:pipe].rstrip()
            # find last |
            curp = pipe+1
            if not inner[:pipe].lower() == "category:relisted afd debates":
                for s1,e1 in findBalanced(inner, ['[['], [']]']):
                    last = inner.rfind('|', curp, s1)
                    if last >= 0:
                        pipe = last # advance
                    curp = e1
                label = inner[pipe+1:].strip()

                label = processPotentialWikiLink(inner[:pipe], label)
            else:
                label = ""
        res += " ".join([text[cur:s], label, trail])
        cur = end
    return res + text[cur:]

def processPotentialWikiLink(link, label):
    """
    If we deal with a link to a Wikipedia meta page (starting with 'WP:'
    or 'Wikipedia:', we want to be able to analyse this later. Hence,
    we add this link (without colon) to the label iff a later alt text
    (if any) does not already contains it. Otherwise, we would count it
    twice.
    """
    linkLowered = link.lower()
    if linkLowered.startswith('wp:') or linkLowered.startswith('wikipedia:'):
        linkMerged = link.replace(':', '').replace(' ', '')

        # Test e.g. for [[WP:CIVIL|see WP:CIVIL]]:
        position = label.lower().find(linkLowered)
        if not label or position < 0: # both are different, thus important:
            label = '%s %s' % (linkMerged, label)
        else: # Link text contains WikiLink; remove first colon:
            endPosition = position + len(link)
            label = ' '.join([ label[:position], linkMerged, label[endPosition:] ])
    return label

# ----------------------------------------------------------------------
# External links

# from: https://doc.wikimedia.org/mediawiki-core/master/php/DefaultSettings_8php_source.html

wgUrlProtocols = [
     'bitcoin:', 'ftp://', 'ftps://', 'geo:', 'git://', 'gopher://', 'http://',
     'https://', 'irc://', 'ircs://', 'magnet:', 'mailto:', 'mms://', 'news:',
     'nntp://', 'redis://', 'sftp://', 'sip:', 'sips:', 'sms:', 'ssh://',
     'svn://', 'tel:', 'telnet://', 'urn:', 'worldwind://', 'xmpp:', '//'
]

# from: https://doc.wikimedia.org/mediawiki-core/master/php/Parser_8php_source.html

# Constants needed for external link processing
# Everything except bracket, space, or control characters
# \p{Zs} is unicode 'separator, space' category. It covers the space 0x20
# as well as U+3000 is IDEOGRAPHIC SPACE for bug 19052
EXT_LINK_URL_CLASS = r'[^][<>"\x00-\x20\x7F\s]'
ExtLinkBracketedRegex = re.compile('\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)\s*([^\]\x00-\x08\x0a-\x1F]*?)\]', re.S | re.U)
EXT_IMAGE_REGEX = re.compile(
    r"""^(http://|https://)([^][<>"\x00-\x20\x7F\s]+)
    /([A-Za-z0-9_.,~%\-+&;#*?!=()@\x80-\xFF]+)\.((?i)gif|png|jpg|jpeg)$""",
    re.X | re.S | re.U)

def replaceExternalLinks(text):
    textBeforeURI = label = ''
    cur = 0

    for m in ExtLinkBracketedRegex.finditer(text):
        textBeforeURI += text[cur:m.start()]
        cur = m.end()

        url = m.group(1)
        label = m.group(3)

        # # The characters '<' and '>' (which were escaped by
        # # removeHTMLtags()) should not be included in
        # # URLs, per RFC 2396.
        # m2 = re.search('&(lt|gt);', url)
        # if m2:
        #     link = url[m2.end():] + ' ' + link
        #     url = url[0:m2.end()]

        # If the link text is an image URL, replace it with an <img> tag
        # This happened by accident in the original parser, but some people used it extensively
        m = EXT_IMAGE_REGEX.match(label)
        if m: # external image, remove it
            label = ''

    textAfterURI = text[cur:]
    return " ".join([textBeforeURI, (label if label else ''), textAfterURI])
