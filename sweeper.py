#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from game import Sweeper

def main():
    s = Sweeper(screen_size=(600, 600), field_size=(10, 10))
    s.run()

if __name__ == "__main__": 
    main()