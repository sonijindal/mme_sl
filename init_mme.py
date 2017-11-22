#!/usr/bin/env python
import os, sys, argparse
import rethinkdb as r
from lambda_func import *
from common import *

def main():
    print 'Initializing %s table' % INFO

    parser = argparse.ArgumentParser()
    parser.add_argument('--cluster', '-c', default='cluster')
    args = parser.parse_args()

    #root_dir = os.path.join(SCRIPT_DIR, '..', '..')
    #cluster_dir = os.path.join(root_dir, 'util', args.cluster)
    #worker0 = rdjs(os.path.join(cluster_dir, 'worker-0.json'))
    #conn = r.connect(worker0['ip'], 28015)
    conn = r.connect( "localhost", 28015)
    # try to drop table (may or may not exist)
    rv = ''
    try:
        r.db_drop(INFO).run(conn)
        print 'dropped old table'
    except:
        print "couldn't drop old table"
        pass
    print r.db_create(INFO).run(conn);
    print r.db(INFO).table_create(UE).run(conn);
    print r.db(INFO).table(UE).index_create(USER_ID).run(conn)

if __name__ == '__main__':
    main()
