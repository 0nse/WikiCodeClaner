def removeSymbols(text):
    """Removes all symbols as they serve no
    semantical purpose for us."""

    # string.punctuation also includes "-" which we want to keep.
    # Furthermore, we also want to remove some additional symbols:
    for c in "<>|[]{}()@#$€£%&*_=+,.?!'\"«»“”;:/\\~`":
        # it's faster to determine this first instead of blindly replacing:
        if c in text:
            text = text.replace(c, " ")
    return text
