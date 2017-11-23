## Steps:
### 1. Start the rethinkdb server:
`rethinkdb &`

### 2. Initialise the database:
`python init_mme.py <op_num>`

    op_num : 
    0. Initialise database
    1. Clear the UE table
    2. Dump info about the UE table

### 3. Start the attach procedure. attach_request will internally invoke other functions.
For now, it calls attach_accept:

`python attach_request.py '{"user_id":1234, "user_id_type":"guti", "bearer_id":1}'`
