import subprocess
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    print("💬 Initial cleaning of tempory files before the tests...")
    subprocess.run(["bash", "scripts/clean.sh"], check=True)

@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    print("💬 Cleaning of tempory files after the tests...")
    subprocess.run(["bash", "scripts/clean.sh"], check=True)
