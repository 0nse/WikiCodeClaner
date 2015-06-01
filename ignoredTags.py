#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

# These tags are dropped, keeping their content.
# handle 'a' separately, depending on keepLinks
ignoredTags = [
    'abbr', 'b', 'big', 'blockquote', 'center', 'cite', 'div', 'em',
    'font', 'h1', 'h2', 'h3', 'h4', 'hiero', 'i', 'kbd', 'nowiki',
    'p', 'plaintext', 's', 'span', 'strike', 'strong',
    'sub', 'sup', 'tt', 'u', 'var'
]

# Match ignored tags
ignored_tag_patterns = []
def ignoreTag(tag):
    left = re.compile(r'<%s\b[^>/]*>' % tag, re.IGNORECASE) # both <ref> and <reference>
    right = re.compile(r'</\s*%s>' % tag, re.IGNORECASE)
    ignored_tag_patterns.append((left, right))

def getIgnoredTags():
    for tag in ignoredTags:
        ignoreTag(tag)
    return ignored_tag_patterns
