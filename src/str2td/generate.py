from collections.abc import Iterable
from json import dumps
from pathlib import Path

from . import segments


def replace_lark_segment(tag: str, replacement: str, *, filename: str = "./grammar.lark"):
	path = (Path(__file__).parent / filename).resolve()
	lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

	tag_comment = f"//@{tag}"

	for i, line in enumerate(lines):
		if line.strip() == tag_comment:
			if i + 1 < len(lines):
				lines[i + 1] = f"{tag}: {replacement}".rstrip("\n") + "\n"  # noqa: B909
			else:
				raise ValueError(f"Tag '{tag_comment}' found, but no line exists after it to replace.")
			break
	else:
		raise ValueError(f"Tag '{tag_comment}' not found in file.")

	path.write_text("".join(lines), encoding="utf-8")


from tcrutils.console import c


def replace_lark_segment_with_orlist(tag: str, it: Iterable[str], *, filename: str = "./grammar.lark"):
	return replace_lark_segment(
		tag,
		"|".join(
			f'"{repr(s)[1:-1]}"'
			for s in (
				sorted(
					it,
					key=lambda x: (len(x), x),
					reverse=True,
				)
			)
		),
		filename=filename,
	)


replace_lark_segment_with_orlist(
	"WEEKDAY",
	set(segments.weekday.WEEKDAYS),
)

replace_lark_segment_with_orlist(
	"MONTH_WORDS",
	set(segments.date.MONTH_WORDS),
)
