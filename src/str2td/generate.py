from json import dumps
from pathlib import Path

from .segments import weekday


def replace_lark_segment(tag: str, replacement: str, filename: str = "./grammar.lark"):
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


replace_lark_segment(
	"WEEKDAY",
	"|".join(
		f'"{repr(s)[1:-1]}"'
		for s in sorted(
			set(weekday.WEEKDAYS),
			key=len,
			reverse=True,
		)
	),
)
