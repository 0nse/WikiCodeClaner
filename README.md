# WikiCode Cleaner
This code is built upon @attardi's `WikiExtractor.py` (see down below for more information). The existing code already did a great job on removing WikiCode syntax from text in a sophisticated manner. However, it worked on Wikipedia dumps without processing revisions as needed for the [WikiParser](https://github.com/0nse/WikiParser) project. Thus, the modifications were applied and features were removed that are not needed for this project. In more detail, `WikiExtractor.py` has been stripped down as follows:

* No template expansion option.
* No compression option.
* No threading.
* No HTML output.
* No links preservation.
* Directly process text instead of working on dumps.
* Migrated the code from Python 2 to Python 3.
* Code cleanup (removed unused code and SoC).
* Replace [many symbols](removeSymbols.py) with a space.

## WikiExtractor.py
[WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) is a Python script that extracts and cleans text from a [Wikipedia database dump](http://download.wikimedia.org/). The tool was written by [Giuseppe Attardi](https://github.com/attardi) and released under a GPLv3 licence. For further information, see the [project Home Page](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) or the [Wiki](https://github.com/attardi/wikiextractor/wiki).
