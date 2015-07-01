import re

# ([[User talk:Any text|Any text]]) -- User_talk is also possible
talk = "\[\[User[ |_]talk:[^\]]+\]\]"
talkRe = re.compile(r"(?i)" + talk)

contribsRe = re.compile(r"(?i)\[\[Special:Contributions/[^\]]+\]\]")
# [[User:Any text|Any text]] talkRe -- the mid bar is optional:
userRe = re.compile(r"(?i)\[\[User:[^\]]+\]\] \(" + talk + "\)")
# e.g. 13:41, 9 June 2015 (UTC) -- the spaces after the comma and before the bracket are optional:
timestampRe = re.compile(r"\d{2}:\d{2}, {0,1}\d{1,2} (?i)[(January),(February),(March),(April),(May),(June),(July),(August),(October),(November),(December)]+ \d{4} {0,1}\(\w+\)")

def removeSignature(text):
    """ Removes different forms of signatures. This includes timestamps,
    uncustomised signatures as well as talk and contribution link.
    For the later two, we assume that it is rather unlikely that they would
    be used for expressing relevant text in the label part of the link.
    @see https://en.wikipedia.org/wiki/Wikipedia:Signatures
    """
    text = userRe.sub("", text)
    text = timestampRe.sub("", text)
    text = talkRe.sub("", text)
    text = contribsRe.sub("", text)

    return text
