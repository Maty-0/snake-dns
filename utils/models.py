import socket
import struct

class dns_query:
    def __init__(self,transaction_id,qdcount,ancount,nscount,arcount,qr,opcode,aa,tc,rd,ra,z,rcode,question_data,qtype,qclass):
        self.transaction_id  = transaction_id
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.z = z
        self.rcode = rcode
        self.question_data = question_data
        self.qtype = qtype
        self.qclass = qclass

class dns_answerClient:
    def __init__(self,transaction_id,qr,opcode,aa,tc,rd,ra,z,rcode,question_data):
        self.transaction_id  = transaction_id
        self.qdcount = 0x0001 #one question
        self.ancount = 0x0001 #one answer 
        self.nscount = 0x0000
        self.arcount = 0x0000
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.z = z
        self.rcode = rcode
        self.question_data = question_data
        self.qtype = 0x0001 #ipv4
        self.qclass = 0x0001 #using the internet
        self.ttl = 600 #for now hardcoded, this should be in the database
    
    def generate_awnser(self, question_asked, db_search):
        flags = (self.qr << 15) | (self.opcode << 11) | (self.aa << 10) | (self.tc << 9) | (self.rd << 8) | (self.ra << 7) | (self.z << 4) | self.rcode
        
        if (self.question_data.endswith('in-addr.arpa')): #only needed for reverse search
            parts = db_search.split('.')
            addr_data = b''

            for part in parts:
                length_byte = bytes([len(part)])
                addr_data += length_byte + part.encode('utf-8')
            addr_data += b'\x00'
        else:
            addr_data = socket.inet_aton(db_search) #ipv4 to bytes

        answer_data = b'\xc0\x0c'  # Name Pointer (compression), static from what I can see?
        answer_data += struct.pack('!HHIH', 0x0001, 0x0001, self.ttl, len(addr_data)) 
        answer_data += addr_data

        response_header = struct.pack('!HHHHHH', self.transaction_id, flags, self.qdcount, self.ancount, self.nscount, self.arcount)
        response_body = question_asked + answer_data

        response = response_header + response_body
        return response