import mysql.connector # mysql-connector-python
import time
#import logging

from datetime import date
# setup logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# log to terminal
# handler = logging.StreamHandler()
# handler.setFormatter(fmt)
# logger.addHandler(handler)

DATABASE_HOST = '185.221.132.115'
DATABASE_USER = 'root'
DATABASE_PASS = 'mogumogu'
DATABASE_TABLE = 'yummy'

clients_list = {}
db_sw = 0

db_config = {
    'host': DATABASE_HOST,
    'user': DATABASE_USER,
    'password': DATABASE_PASS,
    'database': DATABASE_TABLE
    
}

def update_list():
    global db_sw
    while 1:
        try:
            conn = mysql.connector.connect(**db_config)
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            if db_sw == 0:
                db_sw += 1
                print("[DB] Connected to database")
                
            db_users = set(clients_list.keys())

            for user in users:
                username = user['username']
                if username not in clients_list:
                    clients_list[username] = user
                    print(f"[DB] User {username} added to list")
                # else:
                #     print(f"[DB] User {username} already in list")

            # check if user still in db
            deleted_users = db_users - set([user['username'] for user in users])
            for deleted_user in deleted_users:
                del clients_list[deleted_user]
                print(f"[DB] User {deleted_user} deleted from database")

        except Exception as e:
            print(f"[DB] {e}")
            exit()
        # close db connection
        finally:
            if conn.is_connected():
                cur.close()
                conn.close()
        time.sleep(2)

def add_user(username, password, role_id, user_id, duration, cooldown, endtime, clients, api_key):
    if username in clients_list: # check first before making a connection
        print(f"[DB] User {username} already in database")
        return
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        values = (username, password, role_id, user_id, duration, cooldown, endtime, clients, api_key)

        # check if user already exists in db
        cur.execute("SELECT * FROM users WHERE username = %s", (username,)) # dont use f string
        if cur.fetchone():
            print(f"[DB] User {username} already in database")
            return

        cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", values)
        print(f"[DB] User {username} added to database")
        conn.commit()

    except Exception as e:
        print(f"[DB] {e}")
    # close db connection
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()

def del_user(username):
    try:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        #check if user exists in db
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        if not cur.fetchone():
            print(f"[DB] User {username} does not exist in database")
            return
        
        # if user exists, delete from db
        cur.execute("DELETE FROM users WHERE username = %s", (username,))
        print(f"[DB] User {username} deleted from database")

        conn.commit()
    
    except Exception as e:
        print(f"[DB] {e}")
    finally:
        if conn.is_connected():
            cur.close()
            conn.close()

# add_user('neko', 'uwu', 1, 123, 0, 10, date(2040, 6, 18), -1, '')
# #del_user('neko')

def db_init():
    update_list()