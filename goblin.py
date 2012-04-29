from __future__ import division

from monster import *

class Goblin(Monster):
	sprite = pygame.image.load('gfx/goblin.png').convert_alpha()
	
	max_hp = 2
	
	damage = 1
	
	def __init__(self):
		super(Goblin, self).__init__()
		
	def step(self, pos, map, player):
		super(Goblin, self).step(pos, map, player)
	
		path = astar(map, pos, map.player_xy)
		
		if path:
			if path[1] == map.player_xy:
				#attack
				self.attack(map, path[1], player)
				pass
			else:
				map.move_obj(path[1], self)
		else:
			pass
