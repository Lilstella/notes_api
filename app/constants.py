import os

# Data bases
BASE_DIR = "storage"
MARKDOWN_BASE_DIR = os.path.join(BASE_DIR, "markdown")
CSV_BASE_DIR = os.path.join(BASE_DIR, "csv")
TXT_BASE_DIR = os.path.join(BASE_DIR, "txt")
VERSION_BASE_DIR = os.path.join(MARKDOWN_BASE_DIR, "versions")

# Files
BASE_FOR_EXTENSION = {
    ".md": MARKDOWN_BASE_DIR,
    ".csv": CSV_BASE_DIR,
    ".txt": TXT_BASE_DIR,
}
