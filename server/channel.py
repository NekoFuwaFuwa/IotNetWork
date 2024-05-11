import socket
import threading
import paramiko
import main
import database
import cli
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='/dev/null')

class startSSH(paramiko.ServerInterface):
    def __init__(self, addr) -> None:
        self.event = threading.Event()
        self.addr = addr[0]
    
    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        #return super().check_channel_request(kind, chanid)

    def check_auth_password(self, username: str, password: str) -> int:
        users = database.clients_list
        for key, value in users.items():
            if value["username"] == username and value["password"] == password:
                self.username = username
                print(f"[channel] SSH - User {self.username} successfully logged in {self.addr}")
                return paramiko.AUTH_SUCCESSFUL
        print(f"[channel] SSH - Failed Login Attempt: {self.addr} {username}:{password}")
        return paramiko.AUTH_FAILED
        #return super().check_auth_password(username, password)
    
    def check_channel_shell_request(self, channel: paramiko.Channel) -> bool:
        self.event.set()
        return True
        #return super().check_channel_shell_request(channel)
    
    def check_channel_pty_request(self, channel: paramiko.Channel, term: bytes, width: int, height: int, pixelwidth: int, pixelheight: int, modes: bytes) -> bool:
        return True
        #return super().check_channel_pty_request(channel, term, width, height, pixelwidth, pixelheight, modes)

def handle_connection(client:socket.socket, addr):
    print(f"[channel] SSH - Incoming connection: {addr[0]}:{addr[1]}")
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(main.HOST_KEY)
        transport.local_version = "SSH-2.0-OpenSSH_8.2p1 Watame did nothing wrong!"
        server = startSSH(addr)

        try:
            transport.start_server(server=server)
        except Exception as e:
            if "Error reading SSH protocol banner" in str(e):
                print(f"[channel] SSH - {addr[0]} reading SSH banner")
                raise Exception("SSH negotiation failed")
            print(f"[channel] SSH - Failed to start server: {e}")
        
        channel = transport.accept(10)
        if channel is None:
            print(f"[channel] SSH - No channel received from {addr[0]}")
            raise Exception("No channel")
        
        #channel.settimeout(5)
        if transport.remote_version != '':
            print("[channel] SSH - Client SSH: {}: {}".format(addr[0], transport.remote_version))
            #logging.info('Client SSH version ({}): {}'.format(addr[0], transport.remote_version))
        
        server.event.wait(10)
        if not server.event.is_set():
            print(f"[channel] SSH - Event not received from {addr[0]}")
            raise Exception("No shell request")
        
        try:
            cli.main_cmds(channel, server.username, addr)
        except Exception as e:
            if "Socket is closed" in str(e):
                print(f"[channel] SSH - User {server.username} logged out {addr[0]}")
            else:
                print(e)
                pass

        channel.close()

    except Exception as e:
        #print(f"[channel] SSH - Error {e}")
        try:
            transport.close()
        except Exception:
            pass

def start_ssh(addr, port):
    try:
        ssh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssh.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssh.bind((addr, port))
    except Exception as e:
        print("[channel] Failed to bind")
        exit()
    
    threads = []
    print(f"[channel] SSH server listening on port {port}")
    while 1:
        try:
            ssh.listen(100)
            client, addr = ssh.accept()
        except Exception as e:
            print(f"[channel] Error occurred: {e}")
            continue
        
        new_thread = threading.Thread(target=handle_connection, args=(client, addr)) # start SSH server
        new_thread.start()
        threads.append(new_thread)
    