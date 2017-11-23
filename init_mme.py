#!/usr/bin/env python
import os, sys, argparse
import rethinkdb as r
from lambda_func import *
from common import *

def db_init(db_name, table_name):
    print 'Initializing %s table' % INFO
    conn = r.connect(host=DB_ADDRESS, port=DB_PORT)

    try:
        r.db_drop(db_name).run(conn)
    except:
        print "couldn't drop old table"
        pass
    r.db_create(db_name).run(conn)
    r.db(db_name).table_create(table_name).run(conn)
    r.db(db_name).table(table_name).index_create(USER_ID).run(conn)
    return 'DB initialized'

def db_clear_table(db_name, table_name):
    conn = r.connect(DB_ADDRESS, DB_PORT)
    r.db(db_name).table(table_name).delete().run(conn)
    return 'Deleted table'

def db_table_status(db_name, table_name):
    conn = r.connect(DB_ADDRESS, DB_PORT)
    cursor = r.db(db_name).table(table_name).run(conn)
    for document in cursor:
        print document
    return 'Printed UEs'

OPTIONS = {
    0 : db_init,
    1 : db_clear_table,
    2 : db_table_status,
}
if __name__ == '__main__':
    ret = OPTIONS[int(sys.argv[1])](INFO, UE)
    print ret
