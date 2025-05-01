.PHONEY: default clean veryclean

default:
	python scripts/talkpages.py

clean:
	rm -rf _site/*
	find . -type d -name '*_files' -exec rm -rf {} +

veryclean: clean
	rm -f previous/*.qmd.2025*Z
