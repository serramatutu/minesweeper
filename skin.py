#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import abc

class Skin:
    @abc.abstractmethod
    def background(self, row, col, state, value):
        pass

    @abc.abstractmethod
    def font(self, row, col, state, value):
        pass

class JsonSkin(Skin):
    def __init__(self, path):
        pass

    def background(self, row, col, state, value):
        pass

    def font(self, row, col, state, value):
        pass

