from __future__ import division

from monster import *
from effect import *

class Leprechaun(Monster):
	sprite = pygame.image.load('gfx/leprechaun.png').convert_alpha()
	
	max_hp = 2
	
	damage = 0
	
	def __init__(self):
		super(Leprechaun, self).__init__()
		
		self.did_move = False
		self.poofed = False
		
	def step(self, pos, map, player):
		if (self.did_move):
			self.did_move = False
			return
			
		self.did_move = True
	
		super(Leprechaun, self).step(pos, map, player)
	
		path = astar(map, pos, map.player_xy)
		
		if path:
			if path[1] == map.player_xy:
				#attack
				player.gold = int(player.gold / 2)
				#map.add_obj(pos, SmokeCloud)
				self.poofed = True
				self.delete = True
			else:
				map.move_obj(path[1], self)
		else:
			pass

		if self.delete and not self.poofed:
			map.add_obj(pos, SmokeCloud())