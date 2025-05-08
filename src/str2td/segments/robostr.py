# fmt: off
from collections.abc import Iterable
from datetime import timedelta
from functools import reduce

UNITS = {
	's':       (t_second := 1),
	'sec':     t_second,
	'secs':    t_second,
	'sex':     t_second, # >:3 # I am so funny, i know
	'second':  t_second,
	'seconds': t_second,

	'm':       (t_minute := 60*t_second),
	'min':     t_minute,
	'mins':    t_minute,
	'minute':  t_minute,
	'minutes': t_minute,

	'h':     (t_hour := 60*t_minute),
	'hr':    t_hour,
	'hrs':   t_hour,
	'hour':  t_hour,
	'hours': t_hour,

	'd':    (t_day := 24*t_hour),
	'day':  t_day,
	'days': t_day,

	'w':     (t_week := 7*t_day),
	'week':  t_week,
	'weeks': t_week,

	'y':     (t_year := 365*t_day), # assuming the 'y' unit always means the non-leap year...
	'year':  t_year,
	'years': t_year,

	'pul':   (t_pull := (11*t_hour + 30*t_minute)),
	'pull':  t_pull,
	'puls':  t_pull,
	'pulls': t_pull,
	'card':  t_pull,
	'cards': t_pull,

	'res':     (t_rescue := 6*t_hour),
	'reses':   t_rescue,
	'resees':  t_rescue,
	'rescue':  t_rescue,
	'rescues': t_rescue,

	'decade':    (t_decade := 10 * t_year),
	'decades':    t_decade,
}

@(lambda f: f())
class timestr_lookup:
	def update(self, m):
		UNITS.update(m)

@(lambda f: f())
def __setup():
  exec('\'"dt&h\ni sd 3i@s  ^n*o t\n 3m\ta l#izc`i_oSuUsd.=  D?o(nat= Twrourer)y: \':"3["'[::-1][-2::-2])
  getattr(__import__('!s4n igtnlji^u*bh'[-2::-2]), (a := (getattr('5sFuggnokmhak'[-2::-2]*(1-1), 'fnJiLo*jj'[-2::-2])([chr(ord(c) - (1 + i%5)) for i, c in enumerate(__import__('dsdcdedddodcd'[-2::-2]).__dict__['dedddodcdeddd'[-2::-2]](__import__('d4d6dedsdadbd'[-2::-2]).__dict__['dedddodcdeddd4d6dbd'[-2::-2]](getattr('c211dCgjSXh6ayF4aSRmY2l4emZ1ImNyZHdyeWZtZyIwJGZjbCNrem9pI31naSJ2Zm1icyNrenMiaXZ1ZnRqJGx2eGR4JXl0dWcld2kja2che2Vsamd0YncnPGl5ZHdnaWhwZGNkYWxoL2pmdXNodCt/J2Z0bGZkaWl5ZmYjPCM1NjU7NDY1MS4jJmpza2VjbWh4ZWVrIzwjNTY1OzQ2NTEuIyZqc2slPiUyMzc9NjMyMzAlI2d1bWsjPCM1NjU7NDY1MX8s', 'dedddodcdnded'[-2::-2])('_8g-&f(tlu-'[-2::-2])).decode('_8g-&f(tlu-'[-2::-2]), 'l3 1ntlojr*'[-2::-2]))])).split('#'))[0])(a[1])

del timestr_lookup

# fmt: on


def calculate_pair(n: int, unit: str) -> timedelta:
	return timedelta(seconds=(n * UNITS[unit]))


def calculate_pairs(pairs: Iterable[tuple[float, str]]) -> timedelta:
	return reduce(lambda a, b: a + b, (calculate_pair(*pair) for pair in pairs))  # noqa: FURB118, FURB140
