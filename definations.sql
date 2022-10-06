CREATE TABLE question_stats(
    question_id SERIAL PRIMARY KEY,
    resolved boolean,
    date_assessed TIMESTAMP default now()
);


CREATE TABLE feedbacks(
    feedback_id SERIAL PRIMARY KEY,
    feedback VARCHAR(225),
    resolved boolean default false,
    date_posted TIMESTAMP default now()
);

CREATE TABLE questions(
    question_id SERIAL PRIMARY KEY,
    question VARCHAR(225),
    resolved boolean default false,
    date_posted TIMESTAMP default now()
);

CREATE TABLE feedbacks(
    feedback_id SERIAL PRIMARY KEY,
    feedback VARCHAR(225),
    resolved boolean default false,
    date_posted TIMESTAMP default now()
);

INSERT INTO questions(question) VALUES(N'ክፍል አለምግባት ችግር አለው?');  
INSERT INTO questions(question) VALUES(N'ዉጤት እንዴት ነው የሚሰላው?'); 
INSERT INTO questions(question, resolved) VALUES(N'ለዲግሪ ዝቅተኛ ክሬዲት ስንት ነው','true'); 
INSERT INTO questions(question, resolved) VALUES(N'ለዲግሪ ዝቅተኛ ክሬዲት ስንት ነው','true'); 

INSERT INTO feedbacks(feedback) VALUES(N'It is a good app'); 
INSERT INTO feedbacks(feedback) VALUES(N'ይህ የኔ አስተያየት ነው።'); 
INSERT INTO feedbacks(feedback) VALUES(N'ይህ የኔ አስተያየት ነው።'); 
INSERT INTO feedbacks(feedback) VALUES(N'ይህ የኔ አስተያየት ነው።'); 
INSERT INTO feedbacks(feedback, resolved) VALUES(N'ይህ የኔ አስተያየት ነው።','true'); 
INSERT INTO feedbacks(feedback, resolved) VALUES(N'ይህ የኔ አስተያየት ነው።','true');
INSERT INTO feedbacks(feedback, resolved) VALUES(N'ይህ የኔ አስተያየት ነው።','true');
INSERT INTO feedbacks(feedback, resolved) VALUES(N'ይህ የኔ አስተያየት ነው።','true');
INSERT INTO feedbacks(feedback, resolved) VALUES(N'ይህ የኔ አስተያየት ነው።','true');


CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(225),
    last_name VARCHAR(225),
    email VARCHAR(225), 
    password VARCHAR(225),
    password_hidden VARCHAR(225),
    date_created TIMESTAMP DEFAULT now()
);

INSERT INTO users(first_name, last_name, email, password) VALUES('Bereket','Tusa','beckyta@gmail.com', 'Admin##@&');

CREATE TABLE update_points(
    update_id SERIAL PRIMARY KEY,
    user_id INT,
    bus_id INT,
    post_time TIMESTAMP
);


