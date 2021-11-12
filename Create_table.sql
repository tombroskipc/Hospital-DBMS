-- CREATE a Hospital schema
CREATE SCHEMA Hospital;

-- USE Hospital schema
USE Hospital;

-- CREATE 25 TABLES
CREATE TABLE Insurance_company (
    InsCo_id INT NOT NULL AUTO_INCREMENT,
    InsCo_name VARCHAR(50) NOT NULL,
    Address VARCHAR(100) NOT NULL,
    Tel_no VARCHAR(10) NOT NULL,
    PRIMARY KEY (InsCo_id)
);

CREATE TABLE Patient (
    Ssn INT NOT NULL,
    Pat_name VARCHAR(50) NOT NULL,
    Sex VARCHAR(1) NOT NULL,
    DOB DATE NOT NULL,
    Age INT NOT NULL,
    Address VARCHAR(100),
    Tel_no VARCHAR(10),
    Email VARCHAR(50),
    InsCo_id INT,
    Start_date DATE,
    End_date DATE,
    PRIMARY KEY (Ssn),
    FOREIGN KEY (InsCo_id) REFERENCES Insurance_company(InsCo_id) ON DELETE SET NULL
);

CREATE TABLE Accountant (
    Acct_id INT NOT NULL AUTO_INCREMENT,
    Acct_name VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Tel_no VARCHAR(10) NOT NULL,
    PRIMARY KEY (Acct_id)
);
-- Set up starting value
ALTER TABLE Accountant AUTO_INCREMENT = 130001;

CREATE TABLE Bill (
    Bill_no INT NOT NULL,
    Created_date DATE NOT NULL,
    Service_charge INT NOT NULL,
    Total_fee INT NOT NULL,
    InsCo_id INT,
    Discount INT,
    Ssn INT NOT NULL,
    Pur_date DATE NOT NULL,
    Pur_type VARCHAR(10) NOT NULL,
    Acct_id INT NOT NULL,
    PRIMARY KEY (Bill_no),
    FOREIGN KEY (InsCo_id) REFERENCES Insurance_company(InsCo_id),
    FOREIGN KEY (Ssn) REFERENCES Patient(Ssn) ON DELETE CASCADE,
    FOREIGN KEY (Acct_id) REFERENCES Accountant(Acct_id)
);

CREATE TABLE Department (
    Dept_id INT NOT NULL AUTO_INCREMENT,
    Dept_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (Dept_id)
);

CREATE TABLE Doctor (
    Doc_id INT NOT NULL AUTO_INCREMENT,
    Doc_name VARCHAR(50) NOT NULL,
    Doc_type VARCHAR(20) NOT NULL,
    Age INT,
    Address VARCHAR(100),
    Tel_no VARCHAR(10) NOT NULL,
    PRIMARY KEY (Doc_id)
);
-- Set up starting value
ALTER TABLE Doctor AUTO_INCREMENT = 110001;

CREATE TABLE Doc_belong (
    Dept_id INT NOT NULL,
    Doc_id INT NOT NULL,
    PRIMARY KEY (Dept_id, Doc_id),
    FOREIGN KEY (Dept_id) REFERENCES Department(Dept_id) ON DELETE CASCADE,
    FOREIGN KEY (Doc_id) REFERENCES Doctor(Doc_id) ON DELETE CASCADE
);

CREATE TABLE Report (
    Re_id INT NOT NULL,
    Category VARCHAR(20),
    Description VARCHAR(100),
    Date DATE NOT NULL,
    Doc_id INT NOT NULL,
    Ssn INT NOT NULL,
    PRIMARY KEY (Re_id),
    FOREIGN KEY (Doc_id) REFERENCES Doctor(Doc_id),
    FOREIGN KEY (Ssn) REFERENCES Patient(Ssn) ON DELETE CASCADE
);

CREATE TABLE Medicine (
    Mdc_id INT NOT NULL AUTO_INCREMENT,
    Mdc_name VARCHAR(50) NOT NULL,
    Price INT,
    MFG DATE NOT NULL,
    EXP DATE NOT NULL,
    Quantity INT NOT NULL,
    Manufacturer VARCHAR(50),
    PRIMARY KEY (Mdc_id)
);
-- Set up starting value
ALTER TABLE Medicine AUTO_INCREMENT = 10001;

CREATE TABLE Include (
    Re_id INT NOT NULL,
    Mdc_id INT NOT NULL,
    Mdc_quantity INT NOT NULL,
    PRIMARY KEY (Re_id, Mdc_id),
    FOREIGN KEY (Re_id) REFERENCES Report(Re_id) ON DELETE CASCADE,
    FOREIGN KEY (Mdc_id) REFERENCES Medicine(Mdc_id)
);

CREATE TABLE Disease (
    Dis_id INT NOT NULL AUTO_INCREMENT,
    Dis_name VARCHAR(50) NOT NULL,
    Dis_description VARCHAR(100),
    PRIMARY KEY (Dis_id)
);

CREATE TABLE Dis_treatment (
    Dis_id INT NOT NULL,
    Treatment VARCHAR(50),
    PRIMARY KEY (Dis_id, Treatment),
    FOREIGN KEY (Dis_id) REFERENCES Disease(Dis_id) ON DELETE CASCADE
);

CREATE TABLE Cure (
    Mdc_id INT NOT NULL,
    Dis_id INT NOT NULL,
    PRIMARY KEY (Mdc_id, Dis_id),
    FOREIGN KEY (Mdc_id) REFERENCES Medicine(Mdc_id) ON DELETE CASCADE,
    FOREIGN KEY (Dis_id) REFERENCES Disease(Dis_id) ON DELETE CASCADE
);

CREATE TABLE Get_disease (
    Ssn INT NOT NULL,
    Dis_id INT NOT NULL,
    Start DATE,
    End DATE,
    PRIMARY KEY (Ssn, Dis_id),
    FOREIGN KEY (Ssn) REFERENCES Patient(Ssn) ON DELETE CASCADE,
    FOREIGN KEY (Dis_id) REFERENCES Disease(Dis_id) ON DELETE CASCADE
);

CREATE TABLE Test (
    Test_id INT NOT NULL AUTO_INCREMENT,
    Test_name VARCHAR(50) NOT NULL,
    Test_room_no INT NOT NULL,
    PRIMARY KEY (Test_id)
);

CREATE TABLE Do_test (
    Test_id INT NOT NULL,
    Doc_id INT NOT NULL,
    Ssn INT NOT NULL,
    Date DATE NOT NULL,
    Fee INT,
    PRIMARY KEY (Test_id, Doc_id, Ssn),
    FOREIGN KEY (Test_id) REFERENCES Test(Test_id) ON DELETE CASCADE,
    FOREIGN KEY (Doc_id) REFERENCES Doctor(Doc_id),
    FOREIGN KEY (Ssn) REFERENCES Patient(Ssn) ON DELETE CASCADE
);

CREATE TABLE Operation (
    Op_id INT NOT NULL AUTO_INCREMENT,
    Op_name VARCHAR(50) NOT NULL,
    Op_room_no INT NOT NULL,
    Duration TIME,
    PRIMARY KEY (Op_id)
);

CREATE TABLE Operate (
    Op_id INT NOT NULL,
    Doc_id INT NOT NULL,
    Ssn INT NOT NULL,
    Start DATETIME NOT NULL,
    End DATETIME,
    Fee INT,
    PRIMARY KEY (Op_id, Doc_id, Ssn),
    FOREIGN KEY (Op_id) REFERENCES Operation(Op_id) ON DELETE CASCADE,
    FOREIGN KEY (Doc_id) REFERENCES Doctor(Doc_id),
    FOREIGN KEY (Ssn) REFERENCES Patient(Ssn) ON DELETE CASCADE
);

CREATE TABLE Appointment (
    Appt_id INT NOT NULL AUTO_INCREMENT,
    Duration TIME,
    PRIMARY KEY (Appt_id)
);

CREATE TABLE Consult (
    Appt_id INT NOT NULL,
    Doc_id INT NOT NULL,
    Ssn INT NOT NULL,
    Date DATE,
    Fee INT,
    PRIMARY KEY (Date, Doc_id, Ssn),
    FOREIGN KEY (Appt_id) REFERENCES Appointment(Appt_id) ON DELETE CASCADE,
    FOREIGN KEY (Doc_id) REFERENCES Doctor(Doc_id),
    FOREIGN KEY (Ssn) REFERENCES Patient(Ssn) ON DELETE CASCADE
);

CREATE TABLE Room (
    Room_no INT NOT NULL AUTO_INCREMENT,
    Room_type VARCHAR(20) NOT NULL,
    Room_cost INT,
    Status VARCHAR(100),
    PRIMARY KEY (Room_no)
);

CREATE TABLE Admit (
    Ssn INT NOT NULL,
    Room_no INT NOT NULL,
    Date_number INT NOT NULL,
    Fee INT,
    PRIMARY KEY (Ssn, Room_no),
    FOREIGN KEY (Ssn) REFERENCES Patient(Ssn) ON DELETE CASCADE,
    FOREIGN KEY (Room_no) REFERENCES Room(Room_no)
);

CREATE TABLE Nurse (
    Nur_id INT NOT NULL AUTO_INCREMENT,
    Nur_name VARCHAR(50) NOT NULL,
    Nur_type VARCHAR(20) NOT NULL,
    Age INT,
    Shift VARCHAR(10),
    PRIMARY KEY (Nur_id)
);
-- Set up starting value
ALTER TABLE Nurse AUTO_INCREMENT = 120001;

CREATE TABLE Nur_belong (
    Dept_id INT NOT NULL,
    Nur_id INT NOT NULL,
    PRIMARY KEY (Dept_id, Nur_id),
    FOREIGN KEY (Dept_id) REFERENCES Department(Dept_id) ON DELETE CASCADE,
    FOREIGN KEY (Nur_id) REFERENCES Nurse(Nur_id) ON DELETE CASCADE
);

CREATE TABLE Care (
    Ssn INT NOT NULL,
    Nur_id INT NOT NULL,
    PRIMARY KEY (Ssn, Nur_id),
    FOREIGN KEY (Ssn) REFERENCES Patient(Ssn) ON DELETE CASCADE,
    FOREIGN KEY (Nur_id) REFERENCES Nurse(Nur_id)
);
