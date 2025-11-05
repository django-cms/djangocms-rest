# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source/
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean serve open dev watch live

# Custom targets for convenience
clean:
	rm -rf $(BUILDDIR)/*

serve:
	@echo "Starting documentation server at http://localhost:8000"
	@python -m http.server 8000 --directory $(BUILDDIR)/html

open:
	@echo "Opening documentation in browser..."
	@open $(BUILDDIR)/html/index.html

# Development targets
dev:
	@echo "Building documentation in development mode..."
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) -W --keep-going

watch:
	@echo "Watching for changes and rebuilding..."
	@while true; do \
		inotifywait -r -e modify,create,delete .; \
		$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS); \
	done

live:
	@echo "Starting live documentation server with auto-reload..."
	@echo "Server will be available at http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	@sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" --port 8000 --host 0.0.0.0 --open-browser

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
