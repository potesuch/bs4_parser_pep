from pathlib import Path

BASE_DIR = Path(__file__).parent
MAIN_DOC_URL = 'https://docs.python.org/3/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
PEP_URL = 'https://peps.python.org/'
EXPECTED_STATUS = {
    'A': ['Accepted', 'Active'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn']
}
