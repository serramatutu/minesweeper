from array import array
import math
import random
from enum import Enum
    
import pygame

class TileState(Enum):
    INVISIBLE = 0
    FLAGGED = 1
    VISIBLE = 2
    
MINE = -1

class Tile:
    def __init__(self, value=0, state=TileState.INVISIBLE):
        self._value=value
        self._state=state
        
    def __str__(self):
        if self._state is TileState.INVISIBLE:
            return ''
        elif self._state is TileState.FLAGGED:
            return 'F'
        
        if self._value >= 0:
            return str(self._value)
            
        return 'M'
        
    def setMine(self):
        self._value = MINE
        
    @property
    def hasMineNeighbors(self):
        return self._value > 0
        
    @property
    def isMine(self):
        return self._value == MINE
    
    @property
    def value(self):
        return self._value;
    
    @value.setter
    def value(self, v):
        if self.isMine: 
            raise ValueError("Tile is mine and cannot be changed")
        
        self._value = v
        
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, s):
        if self._state is not TileState.VISIBLE:
            self._state = s

            
            
            
            
class Board:
    def __init__(self, screen_size, field_size=(20, 20), mine_ratio=0.15625):
        self._width = field_size[0]
        self._height = field_size[1]
        self._screen_size = screen_size
        
        self._board = []
        for i in range(0, self._height):
            l = []
            for i in range(0, self._width):
                l.append(Tile())
            self._board.append(l)
        
        mines = math.floor(mine_ratio * self._width * self._height) # quantidade de minas
        
        for i in range(0, mines):
            # inicializa a mina em posição aleatória
            while True:
                row, col = random.randint(0, self._height - 1), random.randint(0, self._width - 1)
                
                if (not self._board[row][col].isMine):
                    break
            
            self._board[row][col].setMine()
            
            for i in range(0, 9):
                nrow = row + i % 3 - 1
                ncol = col + i // 3 - 1
                
                if (nrow < 0 or nrow >= self._height or # porco mas caguei
                    ncol < 0 or ncol >= self._width):
                    continue
                    
                if not self._board[nrow][ncol].isMine:
                    self._board[nrow][ncol].value += 1
        
        # inicializa superfície para desenho
        self._surface = pygame.Surface(screen_size)
        self._surface.convert()
        self._font = pygame.font.Font(None, 20)
        
        w = math.floor(screen_size[0]/self._width)
        h = math.floor(screen_size[1]/self._height)
        for row in range(0, self._height):
            for col in range(0, self._width):
                pygame.draw.rect(self._surface, 
                                 self._get_background_color(row, col), 
                                 pygame.Rect(col * w, 
                                             row * h, 
                                             w, 
                                             h)) # desenha o fundo
        
    def _get_background_color(self, row, col):
        return (230, 230, 230) if (col - row) % 2 == 0 else (200, 200, 200)
            
        
    def report(self, row, col, state):                       
        tile = self._board[row][col]
        tile.state = state
        
        text = str(tile)

        size = self._font.size(text)

        # cor do tile
        color = (0, 180, 0)
        if tile.state is TileState.FLAGGED:
            color = (0, 0, 0)
        elif 1 <= tile.value <= 2:
            color = (255, 128, 0)
        elif tile.value > 2:
            color = (255, 0, 0)
        elif tile.isMine:
            color = (0, 0, 255)

        w = math.floor(self._screen_size[0]/self._width)
        h = math.floor(self._screen_size[1]/self._height)
        self._surface.blit(self._font.render(text,
                                             True,
                                             color,
                                             self._get_background_color(row, col)),
                           (col * w + (w - size[0])/2, 
                            row * h + (h - size[1])/2)
                          )

    @property
    def surface(self):
        s = pygame.Surface(self._screen_size)
        s.blit(self._surface, (0, 0))
        return s