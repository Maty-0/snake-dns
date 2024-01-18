import struct
from .models import dns_query

def splice(data):

    #print(data)
    transaction_id, flags, qdcount, ancount, nscount, arcount = struct.unpack('!HHHHHH', data[:12])
    
    qr = (flags & 0x8000) == 0x8000  # Query/Response
    opcode = (flags >> 11) & 0b1111  # Operation Code
    aa = (flags & 0x0400) == 0x0400  # Authoritative Answer
    tc = (flags & 0x0200) == 0x0200  # TrunCation
    rd = (flags & 0x0100) == 0x0100  # Recursion Desired
    ra = (flags & 0x0080) == 0x0080  # Recursion Available
    z = (flags >> 4) & 0b1111        # Reserved
    rcode = flags & 0x000F           # Response Code

    #question data
    question_section_start = 12      #12th byte is where the question starts
    question_data = b""
    current_index = question_section_start

    question_asked = data[12 : len(data)]

    while data[current_index] != 0x00:
        label_length = data[current_index]
        current_index += 1
        label = data[current_index : current_index + label_length]
        question_data += label + b"."
        current_index += label_length
    
    question_data = question_data.rstrip(b".")
    qtype, qclass = struct.unpack('!HH', data[current_index + 1 : current_index + 5]) #this val floats depending on how long the request is

    query_data = dns_query(transaction_id,qdcount,ancount,nscount,arcount,qr,opcode,aa,tc,rd,ra,z,rcode, question_data.decode("utf-8"),qtype,qclass)
    print (query_data.question_data)
    #print(transaction_id,flags,qdcount,ancount,nscount,arcount,qr,opcode,aa,tc,rd,ra,z,rcode,question_data,qtype,qclass)
    return (
        query_data,
        question_asked
    )
