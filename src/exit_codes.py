from enum import Enum

## Error codes
class Err_kind(Enum):
    NO_DATA_DIR = 1
    NO_NETWORK_DIR = 2
    NO_SRC_DIR = 3
    NO_DATA_FILE_PASSED = 4
    READ_DATA_FAILED = 5
    UNKNOWN_OPTION = 6
    TH_IS_NOT_NUMBER = 7
