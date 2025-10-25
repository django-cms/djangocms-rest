# djangocms-rest Documentation

This directory contains the documentation for djangocms-rest, built with Sphinx.

## Setup

### Using Poetry (Recommended)

```bash
# From project root, install all dependencies including docs
poetry install --with dev

# Navigate to the docs directory
cd docs

# Build the documentation
make html
```

### Alternative: Using pip

```bash
# From project root, install development dependencies
pip install -e ".[dev]"

# Navigate to the docs directory
cd docs

# Build the documentation
make html
```

## Building Documentation

### Build HTML Documentation

```bash
# Build the documentation
make html

# Or use sphinx-build directly
sphinx-build -b html . _build/html
```

### View Documentation Locally

```bash
# Build and serve documentation
make serve

# Or build and open in browser
make html
make open
```

### Development Mode with Live Reload

```bash
# Start live documentation server with auto-reload (recommended)
sh live.sh

# Or run sphinx-autobuild directly
poetry run sphinx-autobuild . _build/html --port 8000 --host 0.0.0.0 --open-browser

# Build with warnings treated as errors
make dev

# Watch for changes and rebuild automatically
make watch
```

## Available Make Targets

- `make html` - Build HTML documentation
- `make clean` - Clean build directory
- `make serve` - Serve documentation on http://localhost:8000
- `make open` - Open documentation in browser
- `make live` - Start live server with auto-reload (recommended for development)
- `make dev` - Build in development mode with warnings
- `make watch` - Watch for changes and rebuild automatically
- `make help` - Show all available targets

## Documentation Structure

The documentation is organized into logical sections:

### Tutorial
- `tutorial/01-quickstart.rst` - Quick start guide
- `tutorial/02-installation.rst` - Installation guide  
- `tutorial/03-openapi-documentation.rst` - OpenAPI documentation guide

### How-to Guides
- `how-to/01-use-multi-site.rst` - Multi-site configuration guide
- `how-to/02-plugin-creation.rst` - Plugin creation guide

### Reference
- `reference/index.rst` - API overview
- `reference/pages.rst` - Pages API reference
- `reference/languages.rst` - Languages API reference
- `reference/placeholders.rst` - Placeholders API reference
- `reference/plugins.rst` - Plugins API reference
- `reference/menu.rst` - Menu API reference
- `reference/breadcrumbs.rst` - Breadcrumbs API reference
- `reference/submenu.rst` - Submenu API reference

### Additional
- `contributing.rst` - Contributing guide
- `changelog.rst` - Version history

## Configuration

The documentation is configured in `conf.py`. Key settings include:

- **Theme**: Furo theme (modern, clean design with sidebar navigation)
- **Extensions**: autodoc, intersphinx, napoleon, sphinx-tabs, sphinx-copybutton, etc.
- **Intersphinx**: Links to Python, Django, DRF, and django CMS documentation
- **Mock imports**: Django and django CMS modules are mocked for autodoc
- **GitHub Integration**: Source repository links and GitHub icon in footer

## Contributing to Documentation

1. Make changes to the `.rst` files
2. Build the documentation to check for errors: `make html`
3. Test locally: `make serve`
4. Submit a pull request

## Troubleshooting

### Common Issues

**ImportError: No module named 'django'**
- This is expected when building documentation without Django installed
- The `conf.py` file includes mock imports for Django modules

**Sphinx build errors**
- Check that all dependencies are installed: `poetry install --with dev` or `pip install -e ".[dev]"`
- Ensure you're in the `docs` directory when running commands
- Check the build output for specific error messages

**Missing intersphinx links**
- The documentation links to external documentation (Python, Django, etc.)
- These links may not work offline
- This is normal behavior

### Getting Help

- Check the [Sphinx documentation](https://www.sphinx-doc.org/)
- Review the [Read the Docs theme documentation](https://sphinx-rtd-theme.readthedocs.io/)
- Open an issue on the project repository 