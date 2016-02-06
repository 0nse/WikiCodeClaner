# WikiCode Cleaner
This code is built upon @attardi's `WikiExtractor.py` (see down below for more information).
The existing code already did a great job on removing WikiCode syntax from text in a sophisticated manner.
However, it worked on Wikipedia dumps without processing revisions as needed for [WikiWho](https://github.com/0nse/WikiWho/tree/DiscussionsParser) project.
Thus, the needed modifications were applied and features were removed that were not needed for this project.
In more detail, `WikiExtractor.py` has been adapted as follows:

* No template expansion option.
* No compression option.
* No threading.
* No HTML output.
* No links preservation.
* Directly process text instead of working on dumps.
* Migrated the code from Python 2 to Python 3.
* Code cleanup (removed unused code and SoC).
* Replace [many symbols](removeSymbols.py) with a space.
* Remove [user and timestamp signatures](https://en.wikipedia.org/wiki/Wikipedia:Signatures) including a few customised ones.
- Split the logic into separate files. The entry point is [`clean.py`](clean.py).

## WikiExtractor.py
[WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) is a Python script that extracts and cleans text from a [Wikipedia database dump](http://download.wikimedia.org/).
The tool was written by [Giuseppe Attardi](https://github.com/attardi) and released under a GPLv3 licence.
For further information, see the [project Home Page](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) or the [Wiki](https://github.com/attardi/wikiextractor/wiki).

## Licence
This work is released under a GPLv3 licence.
It is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **without any warranty**; without even the implied warranty of **merchantability** or **fitness for a particular purpose**.

For more information, please refer to the LICENSE file which you should have received with your copy of the program.
If this is not the case, please refer to http://www.gnu.org/licenses/.
