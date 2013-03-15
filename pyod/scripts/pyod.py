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
TEMPLATE = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="744.09448" height="1052.3622" viewBox="-2 -2 756.65304 1063.7699" id="svg10047">
  <metadata id="metadata16869">
    <rdf:RDF>
      <cc:Work rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
</svg>'''

def main(how_many_cards, deck_name):
   """print the desired cards of the deck

   locate the deck, read its definitions and all of its cards, decide which
   cards are required, then create as many svg files as the suits, including
   the desired cards in the definitions and using them moving them to the
   correct location.
   """

   ## read the deck
   d = pq(filename=deck_name)

   ## the namespace for svg files
   ns = {'ns': 'http://www.w3.org/2000/svg'}

   ## get the definitions - will be repeated in each of our output files
   defs = d('ns|defs', namespaces=ns)

   for suit in SUITS:
      for card in CARD_OFFSET.keys():
         card_group = d("#%s_%s" % (card, suit))
         defs.append(card_group)

   ## you have a real piece of paper and you must cut it, so let's redefine
   ## the card frame as a set of four thin crosses.
   defs.append('<path d="m 2,0 -4,0 m 2,2 0,-4 m 0,2 m 79,0 m 2,0 -4,0 m 2,2 0,-4 m 0,2 m 0,123 m 2,0 -4,0 m 2,2 0,-4 m 0,2 m -79,0 m 2,0 -4,0 m 2,2 0,-4 m 0,2 " id="cf" style="color:#000000;fill:none;stroke:#000000;stroke-width:0.3px;stroke-opacity:1" />')

   ## per suit, create a new svg document
   for suit in SUITS:

      result = pq(TEMPLATE)

      ## put defs at their place
      result.append(defs)

      ## rescale the printable area, all this works if the cards are 79x123
      ## pixels and you are printing on A4.
      result.append('<g transform="matrix(2.8595951,0,0,2.8595951,6.1012654,3.4189498)" id="printable-layer">')

      ## we add elements to the printable layer
      print_area = result('#printable-layer')

      ## put a white background, it's not strictly necessary, but makes viewing easier.
      print_area.append('<rect x="0" y="0" width="237" height="369" fill="#ffffff"/>')

      ## cards are 'use' of definitions, translated to their new position..
      for line in range(3):
         for i, card in enumerate(CARDS_PER_LINE[line]):
            print_area.append('<use xlink:href="#%s_%s" transform="translate(%s,%s)"/>' % (card, suit, i * 79 - CARD_OFFSET[card], line * 123 - SUIT_OFFSET[suit]))

      ## write the document
      result.root.write("/tmp/%s.svg" % suit)


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='print your own deck.')
   parser.add_argument('cards', type=int, help='amount of cards per deck.')
   parser.add_argument('deck', type=str, help='the name of the deck.')
   args = parser.parse_args()
   main(args.cards, args.deck)
