
all: setup-py nvsl.json

.PHONY: setup-py
setup-py:
	if ! [ -d venv ]; then python3 -m venv venv; . venv/bin/activate; pip install -e .; git clone https://github.com/aclements/biblib.git; cd biblib; pip install -e .;fi
	@echo "do '. venv/bin/activate' to run bib2json.py'"

nvsl.json: ../nvsl.bib
	. venv/bin/activate; bib2json ../nvsl.bib -o nvsl.json

.PHONY: upload
push:
	rm -f nvsl.json
	make nvsl.json
	scp nvsl.json swanson+nvsl-homepage@ssh.getflywheel.com:/www/data/bib/nvsl.json
	rsync -e ssh -ur pdfs  swanson+nvsl-homepage@ssh.getflywheel.com:/www/data/bib/
	lftp -f sync.lftp
