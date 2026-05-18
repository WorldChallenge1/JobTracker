# features/environment.py
"""
Behave hooks — run before/after scenarios and the full suite.
"""

import subprocess
import time
import requests

BASE_URL = "http://localhost:8000"


def before_all(context):
    """Start the FastAPI test server once before all scenarios."""
    context.server = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000",
         "--env-file", ".env.test"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Wait until the server is ready (max 10 s)
    for _ in range(20):
        try:
            if requests.get(f"{BASE_URL}/health").status_code == 200:
                break
        except requests.ConnectionError:
            pass
        time.sleep(0.5)
    else:
        raise RuntimeError("Test server did not start in time")


def after_all(context):
    """Terminate the FastAPI test server after all scenarios finish."""
    context.server.terminate()
    context.server.wait()


def before_scenario(context, scenario):
    """Reset the database before every scenario."""
    requests.post(f"{BASE_URL}/test/reset")
    # Reset shared context attributes
    context.response = None
    context.application = None
    context.application_id = None
    context.interview = None
    context.interview_id = None
