# Every immediate child with a Makefile is an independently rebuildable gun.
.DEFAULT_GOAL := all
GUNS := $(patsubst %/Makefile,%,$(wildcard */Makefile))
.PHONY: all check clean refs model render review match atlas atlas-views strips orthos extra verify check-atlas
all check clean refs model render review match atlas atlas-views strips orthos extra verify check-atlas:
	@set -e; for gun in $(GUNS); do $(MAKE) -C "$$gun" $@; done
