CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username varchar(30) NOT NULL, 
    name varchar(60), 
    email varchar(60), 
    password_hash varchar(128), 
    salt varchar(128), 
    profile_picture LONGBLOB,
    UNIQUE (username)
);