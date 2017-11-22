import traceback
import rethinkdb as r

INFO = 'info'                       # DB
UE = 'ue'                           # TABLE - UE info table
USER_ID = 'user_id'                # COLUMN
USER_ID_TYPE = 'user_id_type'      # COLUMN
STATE = 'state'                    # COLUMN
BEARER_ID = 'bearer_id'            # COLUMN - TODO:Multiple bearer ids possible

'''
msg = {
    "user_id" : 
}
'''
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

# def attach_mme(conn, event):


def attach_mme():
    #attach_msg = event['msg']
    attach_msg = 'hello'
    info = parse(attach_msg)
    conn = r.connect("localhost", 28015)
    # Read the data base for this user_id
    value = r.db(INFO).table(UE).get(info.user_id).run(conn)
    if value is not None:
        oldState = value['STATE']
        # For attach request in ID_KNOWN state, ignore, else
    else:
        # if no entry for this UE, then insert this entry and call CreateSession
        r.db(INFO).table(UE).insert({USER_ID: info.user_id,
                                 USER_ID_TYPE:  info.user_id_type,
                                 STATE: ID_KNOWN,
                                 BEARER_ID: info.bearer_id}).run(conn)
    return 'Inserted UE info'


def get_mme_state(conn):
    cursor = r.db(INFO).table(UE).run(conn)
    for document in cursor:
        print document
    return 'Printed UEs'


def main():
    print 'hello attach'
    attach_mme()


'''
def msg(conn, event):
    ts = time.time()
    r.db(CHAT).table(MSGS).insert({MSG: event['msg'],
                                   TS:  ts}).run(conn)
    return 'insert %f complete' % ts

def updates(conn, event):
    ts = event.get('ts', 0)
    rows = list(r.db(CHAT).table(MSGS).filter(r.row[TS] > ts).run(conn))
    if len(rows) == 0:
        wait(conn, ts)
        rows = list(r.db(CHAT).table(MSGS).filter(r.row[TS] > ts).run(conn))
        assert(len(rows) > 0)
    
    rows.sort(key=lambda row: row[TS])
    return rows
'''


def handler(conn, event):
    fn = {'attach':     attach_mme,
          'get_state': get_mme_state}.get(event['op'], None)
    if fn != None:
        try:
            result = fn(conn, event)
            return {'result': result}
        except ValueError:
            return {'error': traceback.format_exc()}
    else:
        return {'error': 'bad op'}


if __name__ == '__main__':
    main()
