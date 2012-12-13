import operator

class Pos(tuple):
	def __init__(self, pos):
		self.pos = pos

	def __add__(self, p):
		return self.__class__(tuple(map(operator.add, self, p)))
		#return self.__class__(map(lambda x, y:x + y, self.pos, p))

	def __sub__(self, p):
		return self.__class__(tuple(map(operator.sub, self, p)))

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
		offset = self.pos_to_offset(pos)
		return self.data[offset]

	def pos_to_offset(self, pos):
		#clamp the position
		y = pos.y() % self.height
		x = pos.x() % self.width

		return ((y) * self.width) + (x)

	def generate(self, pos, width, height):
		for y in xrange(0, height):
			for x in xrange(0, width):
				yield self.get_data_at(Pos((x, y)) + pos)

	def slice(self, pos, width, height):
		x, s, sx = 0, [], []
		for t in self.generate(pos, width, height):
			sx.append(t)
			x += 1
			if (x % width == 0):
				s.append(sx)
				sx = []
		return s

	def __getitem__(self, p):
		return self.get_data_at(p)


class Map:
	def __init__(self, width, height, layers):
		self.width = width
		self.height = height
		self.layers = layers