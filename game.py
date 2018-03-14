#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pygame
from pygame.locals import * # constantes

from board import Board, TileState # minesweeper packages


class Sweeper:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption('Minesweeper')
        pygame.display.flip()

        self._board = Board(screen_size=self._screen.get_size())
    
    def _mousedown(self, e):
        state = TileState.VISIBLE
        if e.button == 3:
            state = TileState.FLAGGED

        row, col = self._board.position(e.pos)
        self._board.report(row, col, state)
        


    def run(self):
        background = pygame.Surface(self._screen.get_size())

        while True:
            for event in pygame.event.get(): # Processa todos os eventos
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    self._mousedown(event)
                    
            mousepos = pygame.mouse.get_pos() if pygame.mouse.get_focused() else None  
            
            background.blit(self._board.surface(mousepos), (0, 0))
            self._screen.blit(background, (0, 0))
            pygame.display.flip() # atualiza tela