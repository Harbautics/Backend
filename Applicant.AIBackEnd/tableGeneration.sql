CREATE TABLE Organizations (
	org_id BIGINT NOT NULL AUTO_INCREMENT,
	name VARCHAR(50) UNIQUE,
	location VARCHAR(100),
	email VARCHAR(50),
	link VARCHAR(100),
	orgType ENUM('Professional', 'Social', 'School Club', 'Business'),
	description VARCHAR(200),
	PRIMARY KEY (org_id)
);

CREATE TABLE Postings (
	post_id BIGINT NOT NULL AUTO_INCREMENT,
	org_id BIGINT NOT NULL,
	name VARCHAR(40),
	status ENUM('OPEN', 'CLOSED'),
	description VARCHAR(200),
	PRIMARY KEY (post_id),
	FOREIGN KEY (org_id) REFERENCES Organizations(org_id),
	UNIQUE KEY (org_id, name)
);

CREATE TABLE Users (
	user_id BIGINT NOT NULL AUTO_INCREMENT,
	name VARCHAR(40),
	email VARCHAR(80) UNIQUE,
	password VARCHAR(64),
	PRIMARY KEY (user_id)
);

CREATE TABLE Questions (
	question_id BIGINT NOT NULL,
	post_id BIGINT NOT NULL,
	question VARCHAR(400),
	FOREIGN KEY (post_id) REFERENCES Postings(post_id),
	PRIMARY KEY (post_id, question_id)
);

/*CREATE TABLE DropdownOption (
	question_id BIGINT NOT NULL AUTO_INCREMENT,
	post_id BIGINT NOT NULL,
	dropdown_text VARCHAR(40),
	FOREIGN KEY (post_id) REFERENCES Postings(post_id),
	FORIEGN KEY (question_id) REFERENCES Questions(question_id),
	PRIMARY KEY (post_id, question_id)
);*/

CREATE TABLE Answers (
	user_id BIGINT NOT NULL,
	post_id BIGINT NOT NULL,
	question_id BIGINT NOT NULL,
	answer VARCHAR(400),
	FOREIGN KEY (post_id, question_id) REFERENCES Questions(post_id, question_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id),
	PRIMARY KEY (post_id, user_id, question_id)
);


CREATE TABLE Applicants (
	user_id BIGINT NOT NULL,
	post_id BIGINT NOT NULL,
	status ENUM('ACCEPT', 'REJECT', 'INTERVIEW', 'PENDING'),
	FOREIGN KEY (post_id) REFERENCES Postings(post_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id),
	PRIMARY KEY (post_id, user_id)
);

CREATE TABLE Members (
	user_id BIGINT NOT NULL,
	org_id BIGINT NOT NULL,
	FOREIGN KEY (org_id) REFERENCES Organizations(org_id),
	FOREIGN KEY (user_id) REFERENCES Users(user_id),
	PRIMARY KEY (org_id, user_id)
);
