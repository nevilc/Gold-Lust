from __future__ import division

import pygame

from object import *

class Stair(Object):
	def __init__(self):
		super(Stair, self).__init__()
		
class StairUp(Stair):
	sprite = pygame.image.load('gfx/stairup.png').convert_alpha()
	
	def __init__(self):
		super(StairUp, self).__init__()
		
	def on_player(self, player):
		pass
		
class StairDown(Stair):
	sprite = pygame.image.load('gfx/stairdown.png').convert_alpha()
	
	def __init__(self):
		super(StairDown, self).__init__()
		
	def on_player(self, player):
		pass