#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from game import Sweeper

def main():
    field_size = (80, 40)
    tile_size = (16, 16)
    s = Sweeper(screen_size=Sweeper.screen_size(field_size, tile_size), field_size=field_size)
    s.run()

if __name__ == "__main__": 
    main()