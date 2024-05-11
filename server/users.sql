CREATE USER 'root'@'%' IDENTIFIED BY 'mogumogu';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
--SET PASSWORD FOR 'root'@'%' = 'sqlpasswd';
FLUSH PRIVILEGES;

CREATE DATABASE yummy;
/* USE mysql;
UPDATE user SET plugin='mysql_native_password' WHERE User='root';
FLUSH PRIVILEGES; */
USE yummy;

CREATE TABLE users (
    username VARCHAR(255) NOT NULL, -- username
    password VARCHAR(255) NOT NULL, -- password
    role_id INT NOT NULL, -- role ID (admin role is 0)
    user_id INT NOT NULL, -- user ID number uwu
    duration INT NOT NULL, -- maximum time (no time limit is 0)
    cooldown INT NOT NULL, -- cooldown
    endtime DATE NOT NULL, -- delete from database on date (stay on database forever is 0)
    clients INT NOT NULL, -- number of access to clients (get access to all clients is -1)
    api_key VARCHAR(255) -- default API key for admins is 'ilovehololive'
);
-- for admins
INSERT INTO users VALUES ('admin', 'admin', 0, 1, 0, 0, "2040-06-18", -1, '');

-- for clients
INSERT INTO users VALUES ('neko', 'uwu', 1, 1024, 10, 10, "2029-04-27", -1, '');

-- delete nigga using ID
DELETE FROM users WHERE user_id = 1024;
