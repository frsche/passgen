import itertools
from abc import ABC, abstractmethod
from collections.abc import Iterable
from functools import reduce


def identity(x):
    return x


def uppercase(x):
    return x.upper()


def lowercase(x):
    return x.lower()


def capitalize(x):
    return x.capitalize()


class Generator(ABC):
    @abstractmethod
    def __iter__(self):
        ...

    @staticmethod
    def new(value):
        if isinstance(value, Generator):
            return value
        if isinstance(value, (str, int)):
            return Single(value)
        if isinstance(value, Iterable):
            return reduce(lambda a, b: a | b, map(Generator.new, value), Nothing())
        raise TypeError(f"cannot build a Generator from {type(value).__name__}")

    def __add__(self, other):
        return Concat(self, other)

    def __radd__(self, other):
        return Concat(other, self)

    def __or__(self, other):
        return Alternative(self, other)

    def __ror__(self, other):
        return Alternative(other, self)

    def optional(self):
        return Optional(self)


class Nothing(Generator):
    def __iter__(self):
        return iter(())


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
        yield from self.lhs
        yield from self.rhs


class Concat(Generator):
    def __init__(self, lhs, rhs):
        self.lhs = Generator.new(lhs)
        self.rhs = Generator.new(rhs)

    def __iter__(self):
        for a in self.lhs:
            for b in self.rhs:
                yield a + b


class Optional(Generator):
    def __init__(self, child):
        self.child = Generator.new(child)

    def __iter__(self):
        yield ""
        yield from self.child


class Chain(Generator):
    def __init__(self, children, sep=("",), map_each=(identity,)):
        self.children = [Generator.new(c) for c in children]
        self.sep = list(sep)
        self.map_each = list(map_each)

    def __iter__(self):
        for combo in itertools.product(*self.children):
            for sep in self.sep:
                for transform in self.map_each:
                    parts = (transform(x) for x in combo)
                    yield sep.join(p for p in parts if p)


class Permutation(Generator):
    def __init__(self, children, sep=("",), map_each=(identity,)):
        self.children = [Generator.new(c) for c in children]
        self.sep = list(sep)
        self.map_each = list(map_each)

    def __iter__(self):
        for order in itertools.permutations(self.children):
            yield from Chain(order, sep=self.sep, map_each=self.map_each)


DEFAULT_LEET = {
    "a": ["@", "4"],
    "b": ["8"],
    "e": ["3"],
    "g": ["9"],
    "i": ["1", "!"],
    "l": ["1"],
    "o": ["0"],
    "s": ["$", "5"],
    "t": ["7"],
}


class Leet(Generator):
    def __init__(self, child, subs=None):
        self.child = Generator.new(child)
        self.subs = DEFAULT_LEET if subs is None else subs

    def __iter__(self):
        for word in self.child:
            options = [[c] + list(self.subs.get(c, ())) for c in word]
            for combo in itertools.product(*options):
                yield "".join(combo)


def g(value):
    return Generator.new(value)
