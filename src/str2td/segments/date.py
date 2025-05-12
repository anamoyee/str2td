# fmt: off
MONTH_WORDS: list[str] = [
	# Polish with diacritics
	"styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień",

	# Polish without diacritics
	"styczen", "luty", "marzec", "kwiecien", "maj", "czerwiec", "lipiec", "sierpien", "wrzesien", "pazdziernik", "listopad", "grudzien",

	# English
	"january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
]
# fmt: on


# === Append 3-letter abbreviations with uniqueness rule ===
@lambda f: f()
def _():
	from collections import Counter

	lines = len(MONTH_WORDS) // 12
	new_entries = []

	for line_idx in range(lines):
		base = MONTH_WORDS[line_idx * 12 : (line_idx + 1) * 12]

		# Generate 3-letter prefixes
		prefixes_3 = [m[:3] for m in base]
		counts_3 = Counter(prefixes_3)
		line_3 = [p if counts_3[p] == 1 else None for p in prefixes_3]
		new_entries.extend(line_3)

	MONTH_WORDS.extend(new_entries)
