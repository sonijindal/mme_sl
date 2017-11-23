from enum import Enum

# DB constants
INFO = 'info'                       # DB
UE = 'ue'                           # TABLE - UE info table
USER_ID = 'user_id'                # COLUMN
USER_ID_TYPE = 'user_id_type'      # COLUMN
STATE = 'state'                    # COLUMN
BEARER_ID = 'bearer_id'            # COLUMN - TODO:Multiple bearer ids possible

DB_ADDRESS = 'localhost'
DB_PORT = 28015

class State(Enum):
    ID_KNOWN = 1
    ID_UNKNOWN = 2
    ATTACHING = 3
    ATTACHED = 4

class user_info:
    def __init__(self):
        self.user_id = 0
        self.user_id_type = 0
        self.state = 0
        self.bearer_id = 0

def parse(msg):
    s = user_info()
    s.user_id = msg['user_id']
    s.user_id_type = msg['user_id_type']
    s.bearer_id = msg['bearer_id']
    return s