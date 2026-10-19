import dotenv

from cost_tracker import display_total_usage, reset_cost_file
from patch_agent import patch_agent_run

dotenv.load_dotenv()

patch_agent_run()


def pytest_sessionstart(session):
    reset_cost_file()


def pytest_sessionfinish(session, exitstatus):
    display_total_usage()
