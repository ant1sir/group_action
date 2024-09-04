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

#NATIVE_MODULES=argparse contextlib itertools joblib json math sys collections.abc abc
#NATIVE_HTMLS=$(addsuffix .html, $(NATIVE_MODULES))

#all: $(HTMLS) $(NATIVE_HTMLS)
all: $(HTMLS)

#$(NATIVE_HTMLS):
#	pydoc -w $(basename $@)

%.html: %.py
	pydoc -w ../$(MODULE_NAME)/$<
 
%.py:
	@echo "Dealing with ../$(MODULE_NAME)/$@"

.PHONY: clean

clean:
	rm *.html
