import lark


class TooManySegmentsOfTypeError(lark.ParseError):
	"""Raised when more segments of the same time were asked to be parsed than allowed. (eg. `'10:!20:'`)."""
