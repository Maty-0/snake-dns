import sqlite3

def db_lookup(data):
    print(data)
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
    #Tip: in the database you will find: 1.0.0.127.in-addr.arpa. This is the ip of your dns server, 
    #you want to fill in the address part with your domain name: this will allow the reverse search to work.
    #watch out the address is from right to left (ex: 127.0.0.1 -> 1.0.0.127)
