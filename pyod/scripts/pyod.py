#!/usr/env python

import argparse
from pyquery import PyQuery as pq


## global definitions
SUITS = ['club', 'spade', 'heart', 'diamond']
SUIT_OFFSET = {'club': 0, 'spade': 369, 'heart': 246, 'diamond': 123}
CARD_OFFSET = dict(("%d" % (i + 1), i * 79) for i in range(10))
CARD_OFFSET.update({'jack': 790, 'queen': 869, 'king': 948})
CARDS_PER_LINE = {0: ['king', 'queen', 'jack'],
                  1: ['1', '10', '9'],
                  2: ['8', '7', '6'],
                  }


## indexed by page_code, the structure of each value is: the template for
## the svg document, the printable layer, then a list of lists, each is a
## page, in each page: lines, in each line: cards.
TEMPLATES = { 0: ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="744.09448" height="1052.3622" viewBox="-2 -2 756.65304 1063.7699" id="svg10047"/>',
                  '<g transform="matrix(2.7166153,0,0,2.7166153,54.407601,28.669419)" id="printable-layer">',
                  [[['1_club', '7_club', '8_club'],
                    ['9_club', '10_club', 'joker_black'],
                    ['jack_club', 'queen_club', 'king_club']],
                   [['1_spade', '7_spade', '8_spade'],
                    ['9_spade', '10_spade', 'joker_black'],
                    ['jack_spade', 'queen_spade', 'king_spade']],
                   [['1_heart', '7_heart', '8_heart'],
                    ['9_heart', '10_heart', 'joker_red'],
                    ['jack_heart', 'queen_heart', 'king_heart']],
                   [['1_diamond', '7_diamond', '8_diamond'],
                    ['9_diamond', '10_diamond', 'joker_red'],
                    ['jack_diamond', 'queen_diamond', 'king_diamond']],
                   ]
                  ),
              1: ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="1052.3622" height="1488.189" viewBox="-2 -2 1070.1236 1504.3211" id="svg10047"/>',
                  '<g transform="matrix(2.3455654,0,0,2.3455654,72.334116,28.899189)" id="printable-layer">',
                  [[['1_club', '7_club', '8_club', '9_club', '10_club'],
                    ['1_club', '7_club', '8_club', '9_club', '10_club'],
                    ['1_club', '7_club', '8_club', '9_club', '10_club'],
                    ['jack_club', 'jack_club', 'queen_club', 'king_club', 'king_club'],
                    ['jack_club', 'queen_club', 'queen_club', 'king_club', 'joker_black']],
                   [['1_spade', '7_spade', '8_spade', '9_spade', '10_spade'],
                    ['1_spade', '7_spade', '8_spade', '9_spade', '10_spade'],
                    ['1_spade', '7_spade', '8_spade', '9_spade', '10_spade'],
                    ['jack_spade', 'jack_spade', 'queen_spade', 'king_spade', 'king_spade'],
                    ['jack_spade', 'queen_spade', 'queen_spade', 'king_spade', 'joker_black']],
                   [['1_heart', '7_heart', '8_heart', '9_heart', '10_heart'],
                    ['1_heart', '7_heart', '8_heart', '9_heart', '10_heart'],
                    ['1_heart', '7_heart', '8_heart', '9_heart', '10_heart'],
                    ['jack_heart', 'jack_heart', 'queen_heart', 'king_heart', 'king_heart'],
                    ['jack_heart', 'queen_heart', 'queen_heart', 'king_heart', 'joker_red']],
                   [['1_diamond', '7_diamond', '8_diamond', '9_diamond', '10_diamond'],
                    ['1_diamond', '7_diamond', '8_diamond', '9_diamond', '10_diamond'],
                    ['1_diamond', '7_diamond', '8_diamond', '9_diamond', '10_diamond'],
                    ['jack_diamond', 'jack_diamond', 'queen_diamond', 'king_diamond', 'king_diamond'],
                    ['jack_diamond', 'queen_diamond', 'queen_diamond', 'king_diamond', 'joker_red']],
                   ]
                  ),
              2: ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="1052.3622" height="744.09448" viewBox="0 0 1052.3622 744.09448" id="svg10047"/>',
                  '<g transform="matrix(1.4379555,0,0,1.4379555,71.787154,18.310181)" id="printable-layer">',
                  [[['1_club', '7_club', '8_club', '9_club', '10_club', 'jack_club', 'queen_club', 'king_club', ],
                    ['1_spade', '7_spade', '8_spade', '9_spade', '10_spade', 'jack_spade', 'queen_spade', 'king_spade', ],
                    ['1_heart', '7_heart', '8_heart', '9_heart', '10_heart', 'jack_heart', 'queen_heart', 'king_heart', ],
                    ['1_diamond', '7_diamond', '8_diamond', '9_diamond', '10_diamond', 'jack_diamond', 'queen_diamond', 'king_diamond']]]),
              }


def main(page_code, deck_name):
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

   ## now iterate on the pages as in TEMPLATES...
   for page_no, page in enumerate(TEMPLATES[page_code][2]):
      ## each page is a new svg document
      result = pq(TEMPLATES[page_code][0])

      ## put defs at their place
      result.append(defs)

      ## rescale the printable area, all this works if the cards are 79x123
      ## pixels and you are printing on A4.
      result.append(TEMPLATES[page_code][1])

      ## we add elements to the printable layer
      print_area = result('#printable-layer')

      ## put a white background, it's not strictly necessary, but makes viewing easier.
      print_area.append('<rect x="0" y="0" width="237" height="369" fill="#ffffff"/>')

      ## cards are 'use' of definitions, translated to their new position..
      for line_no, line in enumerate(page):
         for i, card_suit in enumerate(line):
            card, suit = card_suit.split('_')
            print_area.append('<use xlink:href="#%s" transform="translate(%s,%s)"/>' % (card_suit, i * 79 - CARD_OFFSET.get(card, {'black': 0, 'red': 79}.get(suit, 0)), line_no * 123 - SUIT_OFFSET.get(suit, 492)))

      ## write the document
      result.root.write("/tmp/%s.svg" % page_no)


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description='print your own deck.')
   parser.add_argument('cards', type=int, help='amount of cards per deck.')
   parser.add_argument('deck', type=str, help='the name of the deck.')
   args = parser.parse_args()
   main(args.cards, args.deck)
