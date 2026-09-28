# Build the paper: main.tex -> main.pdf (latexmk tracks cross-references,
# so no explicit dependencies or multiple passes are needed here).
#
#   make deps    install latexmk and every LaTeX package main.tex needs
#   make pdf     build main.pdf
#   make check   build and fail on unresolved \ref/\cite
#   make watch   rebuild on every change
#
# The build targets first run `check-deps`, so a missing package is reported
# with a pointer to `make deps` instead of a cryptic TeX error.

LATEXMK ?= latexmk
MAIN    ?= main
SUDO    ?= sudo

# Packages main.tex loads (directly or through another package): tlmgr names,
# plus cm-super so the T1 EC fonts are embedded as vectors instead of bitmaps.
TEX_PKGS = microtype booktabs enumitem geometry xcolor multirow caption \
           pgf tools amsmath amsfonts hyperref cm-super

# Fedora counterparts (texlive-<package>).  dnf skips whatever is already
# installed, so on a machine with a partial texlive this pulls only the gaps;
# on a bare machine use texlive-scheme-medium instead.  latexmk requires
# perl(File::Find), which is what latexmk and tlmgr both need to run at all.
FEDORA_PKGS = texlive-latex texlive-tools texlive-amsmath texlive-amsfonts \
              texlive-graphics texlive-hyperref texlive-xcolor texlive-geometry \
              texlive-microtype texlive-booktabs texlive-enumitem \
              texlive-multirow texlive-caption texlive-pgf texlive-cm-super \
              latexmk

# Files check-deps looks for; one per functional package above.
TEX_FILES = microtype.sty booktabs.sty enumitem.sty geometry.sty xcolor.sty \
            multirow.sty caption.sty tikz.sty array.sty amsmath.sty \
            amssymb.sty hyperref.sty

.PHONY: all pdf check watch deps check-deps clean distclean

all: pdf

# ── Build ───────────────────────────────────────────────────────────

pdf: check-deps
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
watch: check-deps
	@echo "--> Watching $(MAIN).tex (Ctrl-C to stop)"
	@$(LATEXMK) -pdf -pvc -interaction=nonstopmode $(MAIN).tex

# ── Dependencies ────────────────────────────────────────────────────

# Installs the toolchain with whichever TeX installer is available, then
# verifies it.  Fedora's latexmk package pulls the Perl modules it needs
# (File::Find, used by latexmk and tlmgr); a TinyTeX without them fails
# `tlmgr --version` and falls through to dnf/apt/brew below.
deps:
	@echo "--> Installing LaTeX dependencies for $(MAIN).tex"
	@tlmgr_bin=$$(command -v tlmgr 2>/dev/null || true); \
	user_texlive=false; \
	case "$$tlmgr_bin" in "$$HOME"/*) user_texlive=true;; esac; \
	if [ "$$user_texlive" = true ] && tlmgr --version >/dev/null 2>&1; then \
		echo "    using tlmgr (user-managed TeX Live at $$tlmgr_bin)"; \
		tlmgr install $(TEX_PKGS) latexmk; \
	elif command -v dnf >/dev/null 2>&1; then \
		echo "    using dnf (Fedora); tlmgr here belongs to the system TeX Live"; \
		$(SUDO) dnf install -y $(FEDORA_PKGS); \
	elif command -v apt-get >/dev/null 2>&1; then \
		echo "    using apt-get (Debian/Ubuntu)"; \
		$(SUDO) apt-get update && $(SUDO) apt-get install -y --no-install-recommends \
			texlive-latex-recommended texlive-latex-extra \
			texlive-fonts-recommended texlive-pictures cm-super latexmk; \
	elif command -v brew >/dev/null 2>&1; then \
		echo "    using Homebrew (macOS): BasicTeX"; \
		brew list --cask basictex >/dev/null 2>&1 || brew install --cask basictex; \
		echo "    NOTE: open a new shell so tlmgr is on PATH, then re-run make deps"; \
		$(SUDO) tlmgr install $(TEX_PKGS) latexmk; \
	else \
		echo "!! no supported TeX installer found (need tlmgr, dnf, apt-get or brew)"; \
		exit 1; \
	fi
	@$(MAKE) --no-print-directory check-deps

# Verifies toolchain + packages without installing anything.
check-deps:
	@command -v kpsewhich >/dev/null 2>&1 || { \
		echo "!! no TeX distribution found -- run 'make deps'"; exit 1; }; \
	problems=""; for f in $(TEX_FILES); do \
		kpsewhich $$f >/dev/null 2>&1 || problems="$$problems $$f"; \
	done; \
	for exe in $(LATEXMK) pdflatex; do \
		command -v $$exe >/dev/null 2>&1 && $$exe --version >/dev/null 2>&1 \
			|| problems="$$problems $$exe"; \
	done; \
	if [ -n "$$problems" ]; then \
		echo "!! missing:$$problems"; \
		echo "   run 'make deps' to install them"; exit 1; \
	fi

# ── Clean ───────────────────────────────────────────────────────────

clean:
	@echo "--> Removing auxiliary files"
	@$(LATEXMK) -c $(MAIN).tex

distclean:
	@echo "--> Removing auxiliary files and $(MAIN).pdf"
	@$(LATEXMK) -C $(MAIN).tex
