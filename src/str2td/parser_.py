import pathlib as p

import lark

GRAMMAR_FILE = p.Path(__file__).parent / "grammar.lark"

if __GENERATE_SCRIPTS := True:
	from . import generate as _

parser = lark.Lark(GRAMMAR_FILE.read_text(encoding="utf-8"))
