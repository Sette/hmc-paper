# Build the paper: main.tex -> main.pdf (latexmk tracks cross-references,
# so no explicit dependencies or multiple passes are needed here).

LATEXMK ?= latexmk
MAIN    ?= main

.PHONY: all pdf check watch clean distclean

all: pdf

# ── Build ───────────────────────────────────────────────────────────

pdf:
	@echo "--> Building $(MAIN).pdf"
	@$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex

# Fails if the last build left unresolved \ref/\cite warnings behind.
check: pdf
	@if grep -q "undefined" $(MAIN).log; then \
		echo "!! undefined references in $(MAIN).log:"; \
		grep -n "undefined" $(MAIN).log; \
		exit 1; \
	fi
	@echo "--> No undefined references"

# Rebuild on every source change (Ctrl-C to stop).
watch:
	@echo "--> Watching $(MAIN).tex (Ctrl-C to stop)"
	@$(LATEXMK) -pdf -pvc -interaction=nonstopmode $(MAIN).tex

# ── Clean ───────────────────────────────────────────────────────────

clean:
	@echo "--> Removing auxiliary files"
	@$(LATEXMK) -c $(MAIN).tex

distclean:
	@echo "--> Removing auxiliary files and $(MAIN).pdf"
	@$(LATEXMK) -C $(MAIN).tex
