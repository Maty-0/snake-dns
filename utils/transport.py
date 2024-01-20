
def sendTo_client(dns_query, og_question, db_search, server_socket, address):
    dns_query.generate_answerClient()
    answer_req = dns_query.generate_answer(og_question, db_search[0])
    if answer_req != None:
        server_socket.sendto(answer_req, address)