from __future__ import division

from object import *

class Attackable(Object):
	max_hp = 1
	def __init__(self):
		super(Attackable, self).__init__()
		self.hp = self.max_hp
		self.solid = True
		
	def step(self, pos, map, player):
		if self.hp <= 0:
			self.delete = True