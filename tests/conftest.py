import subprocess
import pytest
from app.constants import BASE_DIR

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    empty_storage = subprocess.run(["bash", "scripts/check_empty.sh", BASE_DIR], capture_output=True, text=True, encoding="utf-8")

    if empty_storage.returncode == 0:
        print("💬 Initial cleaning of tempory files and empty storage before the tests...")
        subprocess.run(["bash", "scripts/clean.sh", "tempory_and_storage"], check=True, encoding="utf-8")
    elif empty_storage.returncode == 1:
        print("💬 Initial cleaning of tempory files before the tests...")
        subprocess.run(["bash", "scripts/clean.sh", "tempory"], check=True, encoding="utf-8")
    
@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    empty_storage = subprocess.run(["bash", "scripts/check_empty.sh", BASE_DIR], capture_output=True, text=True, encoding="utf-8")

    if empty_storage.returncode == 0:
        print("💬 Cleaning of tempory files and empty storage after the tests...")
        subprocess.run(["bash", "scripts/clean.sh", "tempory_and_storage"], check=True, encoding="utf-8")
    elif empty_storage.returncode == 1:
        print("💬 Cleaning of tempory files after the tests...")
        subprocess.run(["bash", "scripts/clean.sh", "tempory"], check=True, encoding="utf-8")
