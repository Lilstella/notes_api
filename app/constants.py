import os

# Data bases
BASE_DIR = "storage"
MARKDOWN_BASE_DIR = os.path.join(BASE_DIR, "markdown")
CSV_BASE_DIR = os.path.join(BASE_DIR, "csv")
TXT_BASE_DIR = os.path.join(BASE_DIR, "txt")
HTML_BASE_DIR = os.path.join(BASE_DIR, "html")
TSV_BASE_DIR = os.path.join(BASE_DIR, "tsv")
TEX_BASE_DIR = os.path.join(BASE_DIR, "latex")

# Files
BASE_FOR_EXTENSION = {
    "markdown": MARKDOWN_BASE_DIR,
    "csv": CSV_BASE_DIR,
    "txt": TXT_BASE_DIR,
    "html": HTML_BASE_DIR,
    "tsv": TSV_BASE_DIR,
    "latex": TEX_BASE_DIR,
}

FILES_EXTENSIONS = {
    "markdown": ".md",
    "csv": ".csv",
    "txt": ".txt",
    "html": ".html",
    "tsv": ".tsv",
    "latex": ".tex",
}

EXTENSION_FILES = {
    ".md": "markdown",
    ".csv": "csv",
    ".txt": "txt",
    ".html": "html",
    ".tsv": "tsv",
    ".tex": "latex",
}

# Versions data bases
VERSION_DIRS = {
    "markdown": os.path.join(MARKDOWN_BASE_DIR, "versions"),
    "csv": os.path.join(CSV_BASE_DIR, "versions"),
    "txt": os.path.join(TXT_BASE_DIR, "versions"),
    "html": os.path.join(HTML_BASE_DIR, "versions"),
    "tsv": os.path.join(TSV_BASE_DIR, "versions"),
    "latex": os.path.join(TEX_BASE_DIR, "versions"),
}
