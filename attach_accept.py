import traceback
import rethinkdb as r
import sys
import json
from common import *

# SJ: Use some invoker for call to another lambda function
import os

def attach_accept(msg):
    info = parse(msg)
    print info.user_id
    conn = r.connect(DB_ADDRESS, DB_PORT)
    # Read the data base for this user_id
    value = r.db(INFO).table(UE).get(info.user_id).run(conn)
    if value is not None:
        oldstate = value['STATE']
        print oldstate
        # For attach request in ID_KNOWN state, ignore, else
    else:
        # if no entry for this UE, then insert this entry and call CreateSession
        r.db(INFO).table(UE).insert({USER_ID: info.user_id,
                                    USER_ID_TYPE:  info.user_id_type,
                                    STATE: State.ATTACHED.name,
                                    BEARER_ID: info.bearer_id}).run(conn)
    return 'Attach accepted'


def handler(event):
    print event
    try:
        result = attach_accept(event)
        return {'result': result}
    except ValueError:
        return {'error': traceback.format_exc()}

if __name__ == '__main__':
    #DATA = {'user_id':'1234', 'user_id_type':'guti', 'bearer_id':'1'}
    print sys.argv[1]
    DATA = json.loads(sys.argv[1])
    print DATA
    print handler(DATA)
