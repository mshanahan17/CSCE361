/*
 * CSCE 361 Semester Project
 * 4-year course planner
 * 2/15/2018
 */

USE apages;

DROP TABLE IF EXISTS MajorSubject;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Major;
DROP TABLE IF EXISTS Ace;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Subject;

CREATE TABLE Subject (
	subject_key INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	subjectId VARCHAR(255) NOT NULL,
	title VARCHAR(255) NOT NULL
) collate=latin1_general_cs;

CREATE TABLE Student (
	student_key INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	username VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL,
	firstName VARCHAR(255),
	lastName VARCHAR(255)
) collate=latin1_general_cs;

CREATE TABLE Ace (
	ace_key INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	aceNum VARCHAR(2) NOT NULL,
	aceDescription TEXT NOT NULL
) collate=latin1_general_cs;

CREATE TABLE Major (
	major_key INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	uri VARCHAR(255),
	minorOffered BOOLEAN NOT NULL,
	minorOnly BOOLEAN NOT NULL
) collate=latin1_general_cs;

CREATE TABLE Course (
	course_key INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	creditHours INT,
	prerequisite VARCHAR(512),
	subject_fk INT NOT NULL,
	courseNum VARCHAR(10) NOT NULL,
	ace_1_fk INT,
	ace_2_fk INT,
	FOREIGN KEY (subject_fk) 	REFERENCES Subject (subject_key),
	FOREIGN KEY (ace_1_fk) 		REFERENCES Ace (ace_key),
	FOREIGN KEY (ace_2_fk) 		REFERENCES Ace (ace_key)
) collate=latin1_general_cs;

CREATE TABLE MajorSubject(
  majorSubject_key INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  major_fk INT NOT NULL,
  subject_fk INT NOT NULL,
  FOREIGN KEY (major_fk) REFERENCES Major (major_key),
  FOREIGN KEY (subject_fk) REFERENCES Subject (subject_key)
) collate=latin1_general_cs;
