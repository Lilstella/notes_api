import os

# Data bases
BASE_DIR = "storage"
MARKDOWN_BASE_DIR = os.path.join(BASE_DIR, "markdown")
CSV_BASE_DIR = os.path.join(BASE_DIR, "csv")
VERSION_BASE_DIR = os.path.join(MARKDOWN_BASE_DIR, "versions")

# Files
VALID_EXTENSIONS = [".md", ".csv"]
MARKDOWN = ".md"
