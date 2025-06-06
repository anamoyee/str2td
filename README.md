# str2td

Easily express a timedelta in a succinct and human-readable way.

## Usage example
```python
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

```
<details>
<summary>Successful inputs</summary>

```
now=2025-05-13 21:01:41 (Central European Summer Time)

Set a reminder in: 3d!10:
Setting reminder at 2025-05-17 10:00:00 (3 days, 12:58:18.493712 from now).

When's your birthday? 10-10
Great! Your nearest birthday is at: 2025-10-10 21:01:41, in 150 days.

[Seconds calculator]: 3d-.25d5.5h1s
3d-.25d5.5h1s = 257401.0 seconds.
```
</details>

<details>
<summary>Erroring inputs</summary>

```
now=2025-05-13 21:12:22 (Central European Summer Time)

Set a reminder in: 1huj
Invalid Syntax!
Error trying to process rule "robostr_segment":

Unknown unit: 'huj'
```
</details>
