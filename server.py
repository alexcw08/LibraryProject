
# MICRO SERVICE "parser-server.py"
# Author: Joshua Sears
# 7/26/2023

import json
import socket as s

# server setup
PORT = 10103
server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind(('', PORT))

# service requests
while True:
    server_socket.listen(1)
    print(f'Server listening on port {PORT}')

    # receive request and set timeout
    connection_socket, address = server_socket.accept()
    print('Connection established.')
    connection_socket.settimeout(2)

    # get msg length
    msg_len = connection_socket.recv(1024).decode()
    msg_len = int(msg_len)
    print(f'Receiving message length: {msg_len} characters.')

    # return length verification
    connection_socket.send(str(msg_len).encode())

    # receive full string
    full_msg = ""
    while True:
        msg = connection_socket.recv(1024).decode()
        full_msg += msg
        # print(f"Message received:\n\t{msg}")

        # when full msg length is received, parse and close
        if len(full_msg) == msg_len:
            print(f'Full Message Received:\n\t{full_msg}.')
            print(f'Parsing data.')
            json_object = json.loads(full_msg)
            parsed_object = dict()
            parsed_object["title"] = json_object["title"]
            parsed_object["authors"] = json_object["authors"]
            parsed_object["categories"] = json_object["categories"]

            # send back parsed object
            print(f"Parsed data to transmit:\n\t{parsed_object}")
            return_msg = json.dumps(parsed_object)
            connection_socket.send(return_msg.encode())

            # close and return to listening
            connection_socket.close()
            print("Connection Closed")
            break
