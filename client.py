import socket
import threading

stop_thread = False
nickname = input("nickname: ")
if nickname == 'admin':
    password = input('password:')

host = '127.0.0.1' #localhost
port = 55555

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            msg = client.recv(1024).decode('ascii')
            print(msg)
            if msg == 'NICK':
                client.send(nickname.encode('ascii'))
                nextmsg = client.recv(1021).decode('ascii')
                print(nextmsg == 'PASS')
                if nextmsg == 'PASS':
                    print(password)
                    client.send(password.encode('ascii'))
                    
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print('connection refused - wrong password')
                        stop_thread = True
            elif nextmsg == 'BAN':
                print('connection refused because this username is banned')
                
            else:
                pass
        except:
            print('An error occurred')
            client.close()
            break

def write():
    while True:
        global stop_thread
        if stop_thread:
            break
        msg = f"{nickname}: {input('')}"
        if msg[len(nickname)+2:].startswith('/'):
            print('yes1')
            
            if nickname == 'admin':
                print('yes2')
                
                if msg[len(nickname)+2:].startswith('/kick'):
                    print('yes3')
                    client.send(f'KICK {msg[len(nickname)+8:]}'.encode('ascii'))
                    
                if msg[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {msg[len(nickname)+7:]}'.encode('ascii'))
            else:
                print('commands can only be executed by the admin!')
        else:
            client.send(msg.encode('ascii'))
    
recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()