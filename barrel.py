from __future__ import division

import pygame
import random

from attackable import *
from gold import *

class Barrel(Attackable):
	max_hp = 1
	
	sprite = pygame.image.load('gfx/barrel.png').convert_alpha()
	
	def __init__(self):
		super(Barrel, self).__init__()
		
	def step(self, pos, map, player):
		super(Barrel, self).step(pos, map, player)
		
		if self.delete and random.random() <= 0.5:
			map.add_obj(pos, random.choice((Gold(), Gold(), GoldPile(), GoldPile(), GoldStacks())))