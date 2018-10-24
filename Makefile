
include Make.rules

.PHONY: setup
setup:
	git config core.hooksPath ./git_hooks

.PHONY: test
test:
	$(MAKE) -C test libpaper-test