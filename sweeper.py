#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from game import Sweeper
import argparse

def main(args):
    field_size = (args.field_size, args.field_size)
    tile_size = (args.tile_size, args.tile_size)
    s = Sweeper(screen_size=Sweeper.screen_size(field_size, tile_size), 
                field_size=field_size,
                mine_ratio=args.mine_ratio)
    s.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--field-size', 
                        help="the field size", 
                        type=int, 
                        default=16,
                        dest='field_size')
    parser.add_argument('--tile-size', 
                        help="the tile size", 
                        type=int, 
                        default=32,
                        dest='tile_size')
    parser.add_argument('--mine-ratio', 
                        help="the ratio of mines in the field", 
                        type=float, 
                        default=0.125,
                        dest='mine_ratio')

    main(parser.parse_args())