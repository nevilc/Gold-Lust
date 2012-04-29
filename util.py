import operator
import random

def merge_dict(d1, d2):
	assert(d1 != d2)
	for k, v in d2.iteritems():
		if k in d1:
			d1[k].extend(v)
		else:
			d1[k] = v
			
	return d1

def addt(t1, t2):
	return tuple(map(operator.add, t1, t2))

def astar_heuristic(pos1, pos2):
	return (pos2[0] - pos1[0]) + (pos2[1] - pos1[1])
	
def astar(map, pos1, pos2):
	closed = []
	open = [pos1]
	path = []
	
	g = {pos1: 0}
	h = {pos1: astar_heuristic(pos1, pos2)}
	f = {pos1: astar_heuristic(pos1, pos2)}
	
	prev = {}
	
	while len(open):
		current = open[0]
		for o in open:
			if f[o] < f[current]:
				current = o
		
		if current ==  pos2:
			temp = current
			path = [temp]
			while temp in prev:
				temp = prev[temp]
				path.insert(0, temp)
			return path
			
		open = [x for x in open if x != current]
		closed.append(current)
		
		l = [(current[0] + 1, current[1]), (current[0] - 1, current[1]), (current[0], current[1] + 1), (current[0], current[1] - 1)]
		random.shuffle(l)
		
		for p in l:
			if p[0] < 0 or p[1] < 0 or p[0] >= map.w or p[1] >= map.h or map.tile[p[0]][p[1]].solid:
				continue
			if p in map.objs:
				solid = False
				for o in map.objs[p]:
					if o.solid:
						solid = True
						break;
				if p in map.objs_temp:
					for o in map.objs_temp[p]:
						if o.solid:
							solid = True
							break;
				if solid:
					continue
			if p in closed:
				continue
			maybe_g = g[current] + 1
			
			if not p in open:
				open.append(p)
				h[p] = astar_heuristic(p, pos2)
				better = True
			elif maybe_g < g[p]:
				better = True
			else:
				better = False
				
			if better:
				prev[p] = current
				g[p] = maybe_g
				f[p] = maybe_g + h[p]
	return []
		