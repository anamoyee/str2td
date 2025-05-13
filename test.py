from datetime import datetime

from str2td import Transformer, parser, str2td

try:
	from tcrutils.console import c
except Exception:
	c = print

tz = datetime.now().astimezone().tzinfo
now = datetime.now(tz=tz)

transformer = Transformer(now, parser_tz=tz)

print()
c(tree := parser.parse("1h30m!25m!10:30:40"))

print()
print(tree.pretty())

print()
c("δ ->", δ := transformer.transform(tree))
c("dt ->", now + δ)
print()


for expr in [
	*(  # robostr
		"0s",
		"1s",
		"1m",
		"1h",
		"1.h",
		".1h",
		"-.1h",
		"-1.h",
		None,
		"1h30m55s",
		"1h!30m!55s",
		"ver1"[::-1],  # obfuscation budget ran out during testing :c
		"noitulover1"[::-1],
	),
	None,
	*(  # time
		"0:01",
		"10:",
		"10:30",
		"10:30:59",
		# "10:30:60",  # error
		# "24:",  # error
	),
	None,
	*(  # date
		"1-",
		"1-7",
		"1-07",
		"1-7-25",
		"1-7-2025",
		"1-7-2026",
		"1-5-2026",
		"20-5-2025",
		"20-may-2025",
	),
	None,
	*(  # weekday
		"mon",
		"tue",
		"wed",
		"thu",
		"fri",
		"sat",
		"sun",
	),
	None,
	*(  # compound
		# "10:!10:", # error
		"10:",
		"10:!11-",
		"10:!15-",
	),
]:
	if expr is None:
		print()
		continue

	try:
		c(f"str2td({expr!r})=", (δ := str2td(expr, now=now, tz=tz), now + δ)[::-1][0])
	except Exception as e:
		c(f"str2td({expr!r})=", e)
		raise
