#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

# skip level 1, it is page name level
section = re.compile(r'(==+)\s*(.*?)\s*\1')

listOpen = { '*': '<ul>', '#': '<ol>', ';': '<dl>', ':': '<dl>' }
listClose = { '*': '</ul>', '#': '</ol>', ';': '</dl>', ':': '</dl>' }
listItem = { '*': '<li>%s</li>', '#': '<li>%s</<li>', ';': '<dt>%s</dt>',
             ':': '<dd>%s</dd>' }

# Match preformatted lines
preformatted = re.compile(r'^ .*?$')

def appendSpace(title):
    """End the title with a period if it does not end in ? or !"""
    if title and title[-1] not in ' ':
        title += ' '
    return title

def compact(text):
    """Deal with headers, lists, empty sections, residuals of tables.
    :param toHTML: convert to HTML
    """

    out = ""                    # list of paragraph
    isEmptySection = False      # empty sections are discarded
    listLevel = ''              # nesting of lists

    for line in text.split('\n'):

        if not line:
            continue
        # Handle section titles
        m = section.match(line)
        if m:
            title = m.group(2)
            lev = len(m.group(1))
            title = appendSpace(title)
            isEmptySection = True
            out += title
            continue
        # Handle page title
        if line.startswith('++'):
            title = line[2:]
            if line.endswith('++'):
                title = line[:-2]
            title = appendSpace(title)
            out += title
            continue
        # handle indents
        elif line[0] == ':':
            out += line.lstrip(':*#;')
            continue
        # handle lists
        elif line[0] in '*#;:':
                continue
        elif len(listLevel):
            for c in reversed(listLevel):
                out += listClose[c]
            listLevel = []

        # Drop residuals of lists
        elif line[0] in '{|' or line[-1] == '}':
            continue
        # Drop irrelevant lines
        elif (line[0] == '(' and line[-1] == ')') or line.strip('.-') == '':
            continue
        elif isEmptySection:
            out += line # first line
            isEmptySection = False
        elif not isEmptySection:
            out += line
        # dangerous
        # # Drop preformatted
        # elif line[0] == ' ':
        #     continue

    return out
