def removeSymbols(text):
    """Removes all symbols as they serve no
    semantical purpose for us."""

    # string.punctuation also includes "-" which we want to treat differently.
    # Furthermore, we also want to remove some additional symbols. The end
    # of the following string consists of different typographical sorts of
    # dashes:
    for c in "<>|[]{}()@#$€£%&*_=+…,.?!\"«»“”‘’;:/\\~`0123456789—‒–―":
        # it's faster to determine this first instead of blindly replacing:
        if c in text:
            text = text.replace(c, " ")
    # Remove apostrophes so that we end up with "dont", "wont", "im"
    # "isnt", "arent", "peters" and so forth:
    text = text.replace("'", "")
    # Remove typographic hyphen to create words such as "nonnotable":
    text = text.replace("-", "")

    return text
