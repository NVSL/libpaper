# Modify this to determine what pdfs get's built
PDF_TARGETS=arxiv.pdf acmart.pdf

-include libpaper/Make.rules
LIBPAPER=..

.PHONY: setup
setup: 
	@(if ! [ -d libpaper ]; then if [ -d $(LIBPAPER) ]; then echo "Linking to $(LIBPAPER)"; ln -sf $(LIBPAPER) ./libpaper; else echo "Couldn't link to $(LIBPAPER), since it doesn't exist.  Clone it?:  'cd ..; git clone git@github.com:NVSL/libpaper.git'"; fi; else echo  "Using this libpaper:"; ls -ld libpaper;fi)
	git config core.hooksPath libpaper/git_hooks

do-tests: libpaper-test texlint-test

.PHONY: libpaper-test
libpaper-test: $(PDF_TARGETS) arxiv-arxiv.tgz

.PHONY: texlint-test
texlint-test:
	texlint --permissive texlint/lint.tex