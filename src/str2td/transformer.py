from calendar import weekday
from collections.abc import Iterable
from datetime import date, datetime, time, tzinfo
from datetime import timedelta as Δ
from functools import reduce
from http.client import TOO_MANY_REQUESTS

import lark

from . import segments
from .error import TooManySegmentsOfTypeError


class _SegmentSorter(lark.Transformer):
	def start(self, items):
		def get_priority(item: lark.Tree):
			return {
				"date_segment": 0,
				"weekday_segment": 1,
				"time_segment": 2,
				"robostr_segment": 3,
			}[item.data]

		sorted_items = sorted(items, key=get_priority)
		return lark.Tree("start", sorted_items)


class Transformer(lark.Transformer):
	now: datetime
	tz: tzinfo
	sorter: _SegmentSorter

	def __init__(
		self,
		now: datetime,
		*,
		parser_tz: tzinfo = datetime.now().astimezone().tzinfo,
	):
		if now.tzinfo is None:
			raise ValueError("`now` must be timezone-aware")

		self.now = now
		self.tz = parser_tz
		self.sorter = _SegmentSorter()

	def transform(self, tree: lark.Tree):
		self.n_date_segments = 0
		self.n_time_segments = 0

		tree = self.sorter.transform(tree)
		return super().transform(tree)

	def start(self, δs: Iterable[Δ]):
		return reduce(lambda a, b: a + b, δs)  # noqa: FURB118

	if True:  # robostr_segment

		def robostr_pair(self, amount_unit) -> tuple[float, str]:
			return float(amount_unit[0]), str(amount_unit[1])

		def robostr_segment(self, pairs: tuple[tuple[float, str]]):
			try:
				return segments.robostr.calculate_pairs(pairs)
			except KeyError as e:
				raise ValueError(f"Unknown unit: {e}") from e

	if True:  # weekday_segment

		def _find_next_weekday(self, weekday_: str) -> Δ:
			return Δ(days=((segments.weekday.WEEKDAYS.index(weekday_) - self.now.weekday()) % 7) or 7)  # or 7 -> when the day is today, assume user meant oh the next week's wednesday or whateverday

		def weekday_segment(self, weekday_str_it: Iterable[str]):
			(weekday_str,) = weekday_str_it

			return self._find_next_weekday(str(weekday_str))

	if True:  # time_segment
		n_time_segments: int

		def _next_time_δ(self, target_time: time) -> Δ:
			dt_in_target_tz = self.now.astimezone(target_time.tzinfo)

			candidate = dt_in_target_tz.replace(
				hour=target_time.hour,
				minute=target_time.minute,
				second=target_time.second,
				microsecond=target_time.microsecond,
			)

			if candidate <= dt_in_target_tz and not self.n_date_segments:  # ensure no date is specified if adjusting time
				candidate += Δ(days=1)

			candidate_in_dt_tz = candidate.astimezone(self.now.tzinfo)

			return candidate_in_dt_tz - self.now

		def time_segment(self, args: list[str]):
			self.n_time_segments += 1

			if self.n_time_segments >= 2:
				raise TooManySegmentsOfTypeError("Too many `time` segments (max: 1/expr)")

			h, m, s, *_ = [int(a) for a in args] + [0, 0]

			ti = time(h, m, s, 0, tzinfo=self.tz)

			return self._next_time_δ(ti)

	if True:  # date segment
		n_date_segments: int

		def _next_date_δ(self, /, day: int, month: int | None, year: int | None) -> Δ:
			"""Given a timezone-aware datetime `dt` and a target day/month/year (some of which may be None), return a timedelta (in whole days) to the next date matching the specified values.

			- If year is fixed: returns (target_date - dt.date()), which may be negative.
			- If year is None but month is fixed: finds the next year ≥ dt.year where month/day exists
			and produces the first date > dt.date().
			- If both month and year are None: finds the next month ≥ dt.month where day exists,
			rolling over year as needed.

			Raises ValueError for impossible locked date combinations.
			"""

			if self.now.tzinfo is None:
				raise ValueError("`dt` must be timezone-aware")
			today = self.now.date()

			# Full specification: day/month/year all fixed
			if month is not None and year is not None:
				try:
					target = date(year, month, day)
				except ValueError as e:
					raise ValueError(f"Invalid date {day:02d}-{month:02d}-{year}") from e
				return Δ(days=(target - today).days)

			# Month fixed, year free: find next year where (year, month, day) > today
			if month is not None:
				# test from this year onward
				y = today.year
				while True:
					try:
						cand = date(y, month, day)
					except ValueError:
						# this year has no such day in that month → skip to next year
						y += 1
						continue
					# if it's today or in the past, roll to next year
					if cand <= today:
						y += 1
						continue
					target = cand
					break
				return Δ(days=(target - today).days)

			# Month and year free: find next month (possibly same) where day exists
			# scan up to 12 months maximum
			start_m = today.month
			start_y = today.year
			for offset in range(13):
				m = ((start_m - 1 + offset) % 12) + 1
				y = start_y + ((start_m - 1 + offset) // 12)
				try:
					cand = date(y, m, day)
				except ValueError:
					# this month/year has no such day → try next month
					continue
				# if same month as today but day ≤ today.day, skip
				if offset == 0 and cand <= today:
					continue
				target = cand
				break
			else:
				# if we exit the loop without break, something is really wrong
				raise ValueError(f"Could not find any future date with day={day}")

			return Δ(days=(target - today).days)

		def date_segment(self, args: list[str]):
			self.n_date_segments += 1

			if self.n_date_segments >= 2:
				raise TooManySegmentsOfTypeError("Too many `date` segments (max: 1/expr)")

			if args.__len__() >= 2:
				if args[1] is not None and not args[1].isnumeric():
					try:
						args[1] = (segments.date.MONTH_WORDS.index(args[1]) % 12) + 1
					except ValueError as e:
						raise ValueError(f"Unknown month name or number: {args[1]!r}") from e

			try:
				d, m, y, *_ = [int(a) for a in args] + [None, None]
			except ValueError as e:
				raise ValueError(f"Invalid date: {args!r}") from e

			if y is not None and y < 100:
				y = 2000 + y  # 25 -> 2025

			return self._next_date_δ(d, m, y)
