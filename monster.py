from __future__ import division

from attackable import *
from util import *
from player import *

class Monster(Attackable):
	damage = 1

	def __init__(self):
		super(Monster, self).__init__()
		

	def attack(self, map, pos, attackable):
		if isinstance(attackable, Player):
			attackable.damage(map, pos, self.damage)
		else:
			attackable.hp -= 1
		map.add_obj(pos, Slash())