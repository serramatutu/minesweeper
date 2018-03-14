#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pygame
from pygame.locals import * # constantes

from board import Board, BoardState, TileState # minesweeper packages


class Sweeper:
    def __init__(self, field_size=None, screen_size=None):
        pygame.init()
        if screen_size is None:
            screen_size = (400, 400)

        if field_size is None:
            field_size = (25, 25)

        self._screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Minesweeper')
        pygame.display.flip()

        self._board = Board(screen_size=self._screen.get_size(), field_size=field_size)
    
    def _mousedown(self, e):
        state = TileState.VISIBLE
        if e.button == 3:
            state = TileState.FLAGGED

        row, col = self._board.position(e.pos)
        return self._board.report(row, col, state)
        


    def run(self):
        background = pygame.Surface(self._screen.get_size())

        while True:
            end = False
            for event in pygame.event.get(): # Processa todos os eventos
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    v = not self._mousedown(event)
                    if not end:
                        end = v
                    
            mousepos = pygame.mouse.get_pos() if pygame.mouse.get_focused() else None  
                

            background.blit(self._board.surface(mousepos), (0, 0))
            self._screen.blit(background, (0, 0))
            pygame.display.flip() # atualiza tela

            if end:
                self.end(self._board.state)
                break
        
        while True:
            for event in pygame.event.get():
                if (event.type == QUIT or 
                    event.type == MOUSEBUTTONDOWN or
                    event.type == KEYDOWN):
                    return
    
    def end(self, state):
        font = pygame.font.Font(None, 30)

        text = ''
        if state is BoardState.WON:
            text = 'Very much good presentation'
        else:
            text = 'You lost 2 points'

        screen_size = self._screen.get_size()
        text_size = font.size(text)

        self._screen.blit(font.render(text, 
                                      True, 
                                      (0, 0, 0)),
                          (int((screen_size[0] - text_size[0])/2),
                          int((screen_size[1] - text_size[1])/2)))
        pygame.display.flip() # atualiza tela

