CREATE DATABASE IF NOT EXISTS speakeasy;

USE speakeasy;

CREATE TABLE IF NOT EXISTS keyboards(
	keyboard_id INT PRIMARY KEY AUTO_INCREMENT,
    phrase1 VARCHAR(255),
    phrase2 VARCHAR(255),
    phrase3 VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    passwd VARCHAR (255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_keyboards(
	relation_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    keyboard_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    
/*populate dummy data*/
INSERT INTO users (username, email, passwd) VALUES 
('rakhadjo', 'rakhadjo@gmail.com', 'urmkoomgay');
INSERT INTO keyboards (phrase1, phrase2, phrase3) VALUES
('obla di', 'obla da', 'life goes on');
INSERT INTO user_keyboards (user_id, keyboard_id) VALUES
('1', '1');

/*arbitrary select users*/
SELECT * FROM users;