from datetime import datetime

from lark import LarkError
from str2td import str2td

now = datetime.now().astimezone()
tz = now.tzinfo  # can be different if the string's timezone is different than your calculation timezone.

print(f"{now=:%Y-%m-%d %H:%M:%S (%Z)}\n")

try:
	string = input("Set a reminder in: ")
	td = str2td(string, now=now, tz=tz)
	print(f"Setting reminder at {now + td:%Y-%m-%d %H:%M:%S} ({td} from now).\n")

	string = input("When's your birthday? ")
	td = str2td(string, now=now, tz=tz)
	print(f"Great! Your nearest birthday is at: {now + td:%Y-%m-%d %H:%M:%S}, in {td.days} days.\n")

	string = input("[Seconds calculator]: ")
	td = str2td(string, now=now, tz=tz)
	print(f"{string} = {td.total_seconds()} seconds")
except LarkError as e:
	print("\nInvalid Syntax!")
	print("=" * 50)
	print(e)
	print("=" * 50)
