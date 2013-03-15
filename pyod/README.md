PYOD
====
pyod, print your own deck, is a small python utility that can be used to produce printable svg files.

usage
-----
the first stage of development is mostly a proof of concept:
* choose the deck you prefer
* decide how many cards per deck you want
* invoke pyod informing it of your choices

this produces some svg files, you can print them on A4 paper using inkscape or something else.

options
-------
initially many choices are hard coded:
* output is on A4
* how many cards per page depends on how many cards you ask
* which cards will be printed depends on how many cards you ask
 * 8: AKQJ, 7-10 (3x3)
 * 9: AKQJ, 6-10 (3x3)
 * 10: AJQK, 2-7 (4x3)
 * 12: AJQK, 2-9 (4x3)
 * 13: AJQK, 2-9 (4x3), plus a fifth page with four rows of 10s.
 * 15: AJQK, 2-9 (4x3), plus a fifth page with three rows of 10s and one row of jokers.

developers' info
----------------

install virtualenv
~~~~~~~~~~~~~~~~~~
* sudo apt-get install curl
* curl -O http://python-distribute.org/distribute_setup.py
* sudo python distribute_setup.py 
* sudo easy_install pip
* sudo pip install virtualenv

setup virtualenv
~~~~~~~~~~~~~~~~
* virtualenv venv
* source venv/bin/activate

install dependencies
~~~~~~~~~~~~~~~~~~~~
* sudo aptitude install python-dev libxml2-dev libxslt-dev
* pip install pyquery
