import sqlite3

def db_lookup(data):
    con = sqlite3.connect("database/domains.sqlite")
    db_con = con.cursor()
    query = 'SELECT address FROM domains WHERE domain = ?' 
    db_con.execute(query, (data,))
    address = db_con.fetchone()
    con.close()

    print(address)
    if address:
        return address
    else:
        return #todo: recursive search needed here

def db_store(domain, address):
    con = sqlite3.connect("database/domains.sqlite")
    db_con = con.cursor()
    query = 'INSERT INTO domains (domain, address) VALUES (?, ?)' 
    vars = (domain, address)
    db_con.execute(query, vars)
    con.commit()
    con.close()