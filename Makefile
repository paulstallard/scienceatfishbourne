.PHONEY: default check clean veryclean

default:
	python scripts/talkpages.py

check:
	quarto render

clean:
	rm -rf _site/*
	find . -type d -name '*_files' -exec rm -rf {} +

veryclean: clean
	rm -f previous/*.qmd.2025*Z
