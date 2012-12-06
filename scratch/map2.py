import json

mapdata = json.loads(open('../assets/maps/world_map.json', 'r').read())

#print mapdata['layers'][0]['name']

class Pos:
	def __init__(self, pos):
		self.pos = pos

	def __add__(self, p):
		return self.__class__(map(operator.add, self, p))

	def __repr__(self):
		return repr(self.pos)

	def x(self):
		return self.pos[0]

	def y(self):
		return self.pos[1]


class MapLayer:
	def __init__(self, data, width, height, opacity, name):
		self.data = data
		self.width = width
		self.height = height
		self.opacity = opacity
		self.name = name

	def get_data_at(self, pos):
		pass

	def pos_to_offset(self, pos):
		return ((pos.y() - 1) * self.width) + (pos.x() - 1)

ml = MapLayer([], 32, 32, 1, 'test')
print ml.pos_to_offset(Pos((2,1)))