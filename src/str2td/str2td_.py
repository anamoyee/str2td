from datetime import datetime, timedelta, tzinfo

from .parser_ import parser
from .transformer import Transformer


def str2td(s: str, *, now: datetime, parser_tz: tzinfo = datetime.now().astimezone().tzinfo) -> timedelta:
	tree = parser.parse(s)

	return Transformer(now=now, parser_tz=parser_tz).transform(tree)
