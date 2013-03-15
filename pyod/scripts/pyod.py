#!/usr/env python

import argparse
from pyquery import PyQuery as pq

SUITS = ['club', 'spade', 'heart', 'diamond']
SUIT_OFFSET = {'club': 0, 'spade': 369, 'heart': 246, 'diamond': 123}
CARD_OFFSET = dict(("%d" % (i + 1), i * 79) for i in range(10))
CARD_OFFSET.update({'jack': 790, 'queen': 869, 'king': 948})
CARDS_PER_LINE = {0: ['king', 'queen', 'jack'],
                  1: ['1', '10', '9'],
                  2: ['8', '7', '6'],
                  }

def main(how_many_cards, deck_name):
   """print the desired cards of the deck

   locate the deck, read its definitions and all of its cards, decide which
   cards are required, then create as many svg files as the suits, including
   the desired cards in the definitions and using them moving them to the
   correct location.
   """

   ## read the deck
   d = pq(filename="/usr/share/aisleriot/cards/deutschschweizerblatt.svg")

   ## the namespace for svg files
   ns = {'ns': 'http://www.w3.org/2000/svg'}

   ## get the definitions - will be repeated in each of our output files
   defs = d('ns|defs', namespaces=ns)

   for suit in SUITS:
      for card in ['1', '7', '8', '9', '10', 'jack', 'queen', 'king']:
         card_group = d("#%s_%s" % (card, suit))
         defs.append(card_group)

   ## remove card frame: you have a real piece of paper!
   defs.append('<g id="cf"/>')

   ## per suit, create a new svg document
   for suit in SUITS:

      print('''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="1027" height="615" viewBox="0 0 1027 615" id="svg10047">
  <metadata id="metadata16869">
    <rdf:RDF>
      <cc:Work rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>''')

      ## put defs at their place
      print('''<defs>''')
      print defs.html()
      print "</defs>"

      ## now use the cards
      for line in range(3):
         for i, card in enumerate(CARDS_PER_LINE[line]):
            print '<use xlink:href="#%s_%s" transform="translate(%s,%s)"/>' % (card, suit, i * 79 - CARD_OFFSET[card], line * 123 - SUIT_OFFSET[suit])

      ## and close the document
      print "</svg>"
      1/0


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='print your own deck.')
   parser.add_argument('cards', type=int, help='amount of cards per deck.')
   parser.add_argument('deck', type=str, help='the name of the deck.')
   args = parser.parse_args()
   main(args.cards, args.deck)
