import struct
import socket
from .models import dns_answerClient, dns_query

def sendTo_client(dns_query, og_question, db_search, server_socket, address):
    answerObj = dns_answerClient(dns_query.transaction_id, dns_query.qr,dns_query.opcode,dns_query.aa,dns_query.tc,dns_query.rd,dns_query.ra,dns_query.z,dns_query.rcode,dns_query.question_data)
    answer_req = answerObj.generate_awnser(og_question, db_search[0])
    if answer_req != None:
        server_socket.sendto(answer_req, address)