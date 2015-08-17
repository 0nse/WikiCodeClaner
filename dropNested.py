#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
# Extract Template definition

templates = {}
redirects = {}

def dropSpans(spans, text):
    """
    Drop from text the blocks identified in :param spans:, possibly nested.
    """
    spans.sort()
    res = ''
    offset = 0
    # s=position openDelim, e=position closeDelim:
    for s, e in  spans:
        if offset <= s:
            if offset < s: # add text between two templates
                res += text[offset:s]
            offset = e
    res += text[offset:]
    return res

regexSubstitutionPlaceholderString = 'SUBSTITUTED_TEMPLATE_FOR_REGEX_MATCHING'

def replaceSpansWithRePattern(spans, text):
    """
    Drop from text the blocks identified in :param spans:, possibly nested.
    """
    spans.sort()
    res = ''
    offset = 0
    # s=position openDelim, e=position closeDelim:
    for s, e in  spans:
        if offset <= s:
            if offset < s: # add text between two templates
                res += regexSubstitutionPlaceholderString + text[offset:s]
            offset = e
    res += regexSubstitutionPlaceholderString + text[offset:]
    return res

def dropNested(text, openDelim, closeDelim, handleSpans=dropSpans):
    """
    A matching function for nested expressions, e.g. namespaces and tables.
    """
    openRE = re.compile(openDelim)
    closeRE = re.compile(closeDelim)
    # partition text in separate blocks { } { }
    spans = []                  # pairs (s, e) for each partition
    nest = 0                    # nesting level
    start = openRE.search(text, 0)
    if not start:
        return text
    end = closeRE.search(text, start.end())
    next = start
    while end:
        next = openRE.search(text, next.end())
        if not next:            # termination
            while nest:         # close all pending
                nest -= 1
                end0 = closeRE.search(text, end.end())
                if end0:
                    end = end0
                else:
                    break
            spans.append((start.start(), end.end()))
            break
        while end.end() < next.start():
            # { } {
            if nest:
                nest -= 1
                # try closing more
                last = end.end()
                end = closeRE.search(text, end.end())
                if not end:     # unbalanced
                    if spans:
                        span = (spans[0][0], last)
                    else:
                        span = (start.start(), last)
                    spans = [span]
                    break
            else:
                spans.append((start.start(), end.end()))
                # advance start, find next close
                start = next
                end = closeRE.search(text, next.end())
                break           # { }
        if next != start:
            # { { }
            nest += 1

    # collect text outside partitions
    return handleSpans(spans, text)

