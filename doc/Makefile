.SUFFIXES:
.SUFFIXES: .py .html

# Check if either 'command -v' or 'which' exists and set CHECK_CMD accordingly
CHECK_CMD := $(shell if command -v command >/dev/null 2>&1; then echo 'command -v'; else echo 'which'; fi)

# Rule to check if pydoc exists, and install Python if not
ifeq ($(shell $(CHECK_CMD) pydoc),)
	$(error "pydoc is not installed")
endif

MODULE_NAME=group_action

SRCS=$(wildcard ../$(MODULE_NAME)/*.py)
MODULES=$(notdir $(SRCS))
HTMLS=$(MODULES:.py=.html)

all: $(HTMLS)

%.html: ../$(MODULE_NAME)/%.py
	pydoc -w $<
 
.PHONY: clean

clean:
	rm *.html
