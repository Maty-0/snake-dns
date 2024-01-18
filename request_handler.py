from utils import splicer
from database import db
import socket
import struct

def handler(data):
    transaction_id,flags,qdcount,ancount,nscount,arcount,qr,opcode,aa,tc,rd,ra,z,rcode,question_data,qtype,qclass,question_asked = splicer.splice(data)
    
    if qr or tc: 
        return #todo dns error handeling messages
    #we cant handle responses to the server yet, I will add this soon for recursion
    #tuncation is not allowed/ tcp connection is not setup

    if opcode != 0: #Only standard querries for now
        return

    search = db.db_lookup(question_data)
    if search:
        return sendTo_client(transaction_id, rd, z, search,question_asked)

def sendTo_client(transaction_id, rd, z, question_data, request):
    qr = 1 #its a response
    opcode = 0x000
    aa = 0
    tc = 0
    ra = 0 #for now we cant do recursion
    rcode = 0x0000

    flags = (qr << 15) | (opcode << 11) | (aa << 10) | (tc << 9) | (rd << 8) | (ra << 7) | (z << 4) | rcode

    qdcount = 0x0001 #one question
    ancount = 0x0001 #one answer 
    nscount = 0x0000
    arcount = 0x0000

    qtype = 0x0001 #ipv4
    qclass = 0x0001 #using the internet
    ttl = 600 #for now hardcoded, this should be in the database

    question_data = question_data[0]
    print(question_data)
    addr_data = socket.inet_aton(question_data) #ipv4 to bytes
    answer_data = b'\xc0\x0c'  # Name Pointer (compression), static from what I can see?
    answer_data += struct.pack('!HHIH', 0x0001, 0x0001, ttl, len(addr_data)) 
    answer_data += addr_data

    response_header = struct.pack('!HHHHHH', transaction_id, flags, qdcount, ancount, nscount, arcount)
    response_body = request + answer_data

    response = response_header + response_body
    return(response)
