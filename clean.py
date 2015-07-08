#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from MagicWords import magicWordsRE
from compact import compact
from dropNested import *
from ignoredTags import getIgnoredTags
from links import replaceInternalLinks, replaceExternalLinks
from removeSymbols import removeSymbols
from signature import removeSignature
from unescape import unescape

selfClosingTags = [ 'br', 'hr', 'nobr', 'ref', 'references', 'nowiki' ]

# Match selfClosing HTML tags
selfClosing_tag_patterns = [
    re.compile(r'<\s*%s\b[^>]*/\s*>' % tag, re.DOTALL | re.IGNORECASE) for tag in selfClosingTags
]

placeholder_tags = {'math':'formula', 'code':'codice'}

# Match HTML placeholder tags
placeholder_tag_patterns = [
    (re.compile(r'<\s*%s(\s*| [^>]+?)>.*?<\s*/\s*%s\s*>' % (tag, tag), re.DOTALL | re.IGNORECASE),
     repl) for tag, repl in placeholder_tags.items()
]

syntaxhighlight = re.compile('&lt;syntaxhighlight .*?&gt;(.*?)&lt;/syntaxhighlight&gt;', re.DOTALL)

# Matches space
spaces = re.compile(r' {2,}')

# Drop these elements from article text
discardElements = [
        'gallery', 'timeline', 'noinclude', 'pre', 'includeonly',
        'table', 'tr', 'td', 'th', 'caption', 'div',
        'form', 'input', 'select', 'option', 'textarea',
        'ul', 'li', 'ol', 'dl', 'dt', 'dd', 'menu', 'dir',
        'ref', 'references', 'img', 'imagemap', 'source', 'small'
        ]

# Matches bold/italic
bold_italic = re.compile(r"'''''(.*?)'''''")
bold = re.compile(r"'''(.*?)'''")
italic_quote = re.compile(r"''\"([^\"]*?)\"''")
italic = re.compile(r"''(.*?)''")
quote_quote = re.compile(r'""([^"]*?)""')

# Match HTML comments
# The buggy template {{Template:T}} has a comment terminating with just "->"
comment = re.compile(r'<!--.*?-->', re.DOTALL)

# Compute regular expression patterns for all ignored tags once
ignored_tag_patterns = getIgnoredTags()

def clean(text, hasDebugFlag=False):
    """
    Transforms wiki markup.
    @see https://www.mediawiki.org/wiki/Help:Formatting
    """
    # Drop transclusions (template, parser functions)
    text = dropNested(text, r'{{', r'}}')

    # Drop tables
    text = dropNested(text, r'{\|', r'\|}')

    # Remove any found signatures and timestamps
    text = removeSignature(text)

    # replace external links
    text = replaceExternalLinks(text)

    # replace internal links
    text = replaceInternalLinks(text)

    # drop MagicWords behavioral switches
    text = magicWordsRE.sub('', text)

    ################ Process HTML ###############

    # turn into HTML, except for the content of <syntaxhighlight>
    res = ''
    cur = 0
    for m in syntaxhighlight.finditer(text):
        end = m.end()
        res += unescape(text[cur:m.start()]) + m.group(1)
        cur = end
    text = res + unescape(text[cur:])

    # Handle bold/italic/quote
    text = bold_italic.sub(r'\1', text)
    text = bold.sub(r'\1', text)
    text = italic_quote.sub(r'"\1"', text)
    text = italic.sub(r'"\1"', text)
    text = quote_quote.sub(r'"\1"', text)
    # residuals of unbalanced quotes
    text = text.replace("'''", '').replace("''", '"')

    # Collect spans
    spans = []
    # Drop HTML comments
    for m in comment.finditer(text):
            spans.append((m.start(), m.end()))

    # Drop self-closing tags
    for pattern in selfClosing_tag_patterns:
        for m in pattern.finditer(text):
            spans.append((m.start(), m.end()))

    # Drop ignored tags
    for left, right in ignored_tag_patterns:
        for m in left.finditer(text):
            spans.append((m.start(), m.end()))
        for m in right.finditer(text):
            spans.append((m.start(), m.end()))

    # Bulk remove all spans
    text = dropSpans(spans, text)

    # Drop discarded elements
    for tag in discardElements:
        text = dropNested(text, r'<\s*%s\b[^>/]*>' % tag, r'<\s*/\s*%s>' % tag)

    # Turn into text what is left (&amp;nbsp;) and <syntaxhighlight>
    text = unescape(text)

    # Expand placeholders
    for pattern, placeholder in placeholder_tag_patterns:
        index = 1
        for match in pattern.finditer(text):
            text = text.replace(match.group(), '%s_%d' % (placeholder, index))
            index += 1

    text = text.replace('<<', u'«').replace('>>', u'»')

    #############################################

    # Cleanup text
    text = text.replace('\t', ' ')
    text = re.sub(u' (,:\.\)\]»)', r'\1', text)
    text = re.sub(u'(\[\(«) ', r'\1', text)
    text = re.sub(r'\n\W+?\n', '\n', text, flags=re.U) # lines with only punctuations

    # Remove lists, tables and such
    text = compact(text)

    # Remove symbols and reduce multiple successive spaces to one
    text = removeSymbols(text)
    text = spaces.sub(' ', text)

    if hasDebugFlag:
        print(text)
    return text


def printLicence():
    """Print the licence if the file exists/is readable."""
    visualSeparator = '=' * 72
    print("""%s
This program was released under a GPLv3 licence. It should have been
bundled with the appropriate licence which will be printed next. If this
is not the case, please refer to <http://www.gnu.org/licenses/>.
%s""" % (visualSeparator, visualSeparator))
    try:
        licenceFile = open('LICENSE', 'r')
        print(licenceFile.read())
    except:
        pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Clean text from WikiCode and other symbols, leaving only space separated words.',
                                     epilog="""
                                     WikiCodeCleaner, Copyright (C) 2015 Giuseppe Attardi, Michael Ruster.
                                     WikiCodeCleaner comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions. Launch this program with `licence' for details.
                                     """)
    subparsers = parser.add_subparsers(help='Decide between cleaning or showing the software licence.', dest='option')
    subparsers.required=True

    parser_clean = subparsers.add_parser('clean', help='Parse the provided text and clean it from WikiCode and other symbols.')
    parser_clean.add_argument('text', metavar='"some text"', type=str,
                        help='A text as string that should be cleaned.')

    parser_clean.add_argument('-d', '--debug', dest='hasDebugFlag', action='store_true',
                        help='If this parameter is passed, the result is also printed to stdout.')


    parser_licence = subparsers.add_parser('licence', help='Prints the GPL licence under which this program was released.')

    args = parser.parse_args()
    if args.option == 'clean':
        clean(args.text, args.hasDebugFlag)
    else:
        printLicence()
