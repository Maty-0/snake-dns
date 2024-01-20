from utils import splicer
from database import db
from utils.transport import sendTo_client

def handler(data, server_socket, address):
    dns_query,question_asked = splicer.splice(data)
    
    if dns_query.qr or dns_query.tc: 
        return #todo dns error handeling messages
    #we cant handle responses to the server yet, I will add this soon for recursion
    #tuncation is not allowed/ tcp connection is not setup

    if dns_query.opcode != 0: #Only standard querries for now
        return

    search = db.db_lookup(dns_query.question_data)
    if search:
        sendTo_client(dns_query,question_asked,search,server_socket, address)

