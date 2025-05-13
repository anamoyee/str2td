from datetime import datetime, tzinfo
from datetime import timedelta as Δ

from .parser_ import parser
from .transformer import Transformer


def str2td(s: str, *, now: datetime, tz: tzinfo = datetime.now().astimezone().tzinfo) -> Δ:
	tree = parser.parse(s.lower())

	return Transformer(now=now, parser_tz=tz).transform(tree)
