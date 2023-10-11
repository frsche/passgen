from abc import ABC, abstractmethod
from collections.abc import Iterable
import itertools
from functools import reduce

def g(f):
	return Generator.new(f)

class Generator(ABC):
	@abstractmethod
	def __iter__(self):
		pass

	def new(f):
		if isinstance(f, Generator):
			return f
		elif isinstance(f, str):
			return Single(f)
		elif isinstance(f, int):
			return Single(f)
		elif isinstance(f, Iterable):
			return reduce(lambda x,y: x | y, map(lambda x: Generator.new(x), f))
		else:
			throw

	def __add__(self, other):
		return Concat(self, other)

	def __or__(self, other):
		return Alternative(self, other)

	def optional(self):
		return Optional(self)

class Single(Generator):
	def __init__(self, value):
		self.value = str(value)

	def __iter__(self):
		yield self.value

class Alternative(Generator):
	def __init__(self, lhs, rhs):
		self.lhs = Generator.new(lhs)
		self.rhs = Generator.new(rhs)

	def __iter__(self):
		for t1 in self.lhs:
			yield t1
		for t2 in self.rhs:
			yield t2

class Concat(Generator):
	def __init__(self, lhs, rhs):
		self.lhs = Generator.new(lhs)
		self.rhs = Generator.new(rhs)

	def __iter__(self):
		for t1 in self.lhs:
			for t2 in self.rhs:
				yield t1 + t2

class Optional(Generator):
	def __init__(self, g):
		self.g = Generator.new(g)

	def __iter__(self):
		yield ""
		for t in self.g:
			yield t

def identity(x):
	return x

def uppercase(x):
	return x.upper()

def lowercase(x):
	return x.lower()

def capitalize(x):
	return x.capitalize()

class Chain(Generator):
	def __init__(self, children, sep=[""], map_each=[identity]):
		self.children = list(map(lambda x: Generator.new(x), children))
		self.sep = sep
		self.map_each = map_each

	def __iter__(self):
		for v in itertools.product(*self.children):
			for sep in self.sep:
				for m in self.map_each:
					yield sep.join(filter(lambda x: x, map(lambda x: m(x), v)))

class Permutation(Generator):
	def __init__(self, children, sep=[""], map_each=[identity]):
		self.children = list(map(lambda x: Generator.new(x), children))
		self.sep = sep
		self.map_each = map_each
	
	def __iter__(self):
		for v in itertools.permutations(self.children):
			for t in Chain(v, sep=self.sep, map_each=self.map_each):
				yield t

# the password started with "pw", then either "abc" or "123"
prefix = g("pw") + ["abc", "123"]

# i remember the year 2011 was in the password (either "2011" or "11")
year = g("20").optional() + "11"
day = ["01", "1"]
month = ["june", "06", "6"]
# the birthday is either day.month.year, day-month-year or month/day/year
birthday = Chain([day ,month, year], sep=["-", "."]) | Chain([month, day, year], sep=["/"])

# there was a special symbol inside the password (either ? or !)
special_symbol = ["?", "!"]

# there were also the two words "hello world" in the password. But either all lowercase, or capitalized. (either "helloworld" or "HelloWorld")
good_morning = Chain(["hello", "world"], map_each=[lowercase, capitalize])

# I know the password started with prefix, but i don't know the order of birthday, special_symbol and good_morning.
password = prefix + Permutation([birthday, special_symbol, good_morning])

count = 0
with open("wordlist.txt", "w") as f:
	for t in password:
		f.write(t + "\n")
		count += 1
print("Generated", count, "words.")