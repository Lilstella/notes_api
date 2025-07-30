import os

# Data bases
BASE_DIR = "storage"
MARKDOWN_BASE_DIR = os.path.join(BASE_DIR, "markdown")
CSV_BASE_DIR = os.path.join(BASE_DIR, "csv")
TXT_BASE_DIR = os.path.join(BASE_DIR, "txt")

# Files
BASE_FOR_EXTENSION = {
    "markdown": MARKDOWN_BASE_DIR,
    "csv": CSV_BASE_DIR,
    "txt": TXT_BASE_DIR,
}

FILES_EXTENSIONS = {
    "markdown": ".md",
    "csv": ".csv",
    "txt": ".txt",
}

EXTENSION_FILES = {
    ".md": "markdown",
    ".csv": "csv",
    ".txt": "txt",
}

# Versions data bases
VERSION_DIRS = {
    "markdown": os.path.join(MARKDOWN_BASE_DIR, "versions"),
    "csv": os.path.join(CSV_BASE_DIR, "versions"),
    "txt": os.path.join(TXT_BASE_DIR, "versions"),
}
