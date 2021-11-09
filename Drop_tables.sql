-- DROP 25 TABLES
-- Group 1: Tables referring to group 2 tables
DROP TABLE Bill;
DROP TABLE Doc_belong;
DROP TABLE Nur_belong;
DROP TABLE Include;
DROP TABLE Report;
DROP TABLE Dis_treatment;
DROP TABLE Cure;
DROP TABLE Get_disease;
DROP TABLE Do_test;
DROP TABLE Operate;
DROP TABLE Consult;
DROP TABLE Admit;
DROP TABLE Care;
-- Group 2: Tables referred by group 1 tables and referring to group 3 tables
DROP TABLE Patient;
-- Group 3: Tables referred by group 2 tables
DROP TABLE Insurance_company;
DROP TABLE Accountant;
DROP TABLE Department;
DROP TABLE Doctor;
DROP TABLE Medicine;
DROP TABLE Disease;
DROP TABLE Test;
DROP TABLE Operation;
DROP TABLE Appointment;
DROP TABLE Room;
DROP TABLE Nurse;