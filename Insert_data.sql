-- INSERT data
INSERT INTO Insurance_company
VALUES (1, 'American Health', '2157 Swain Rd, Eaton, Ohio', 9374562728),
       (2, 'Health Star', '250 Lone Pine Rd, Saint Landry, Louisiana', 3188382464);

INSERT INTO Patient
VALUES (292567083, 'Dare Lucas', 'M', '1980-02-14',	41, '7416 Ireland Ct, El Paso, Texas', 9452170294, 'lucas123@gmail.com', 1,	'2020-12-19', '2022-12-18'),
       (415310368, 'Raynor Kylee', 'F', '1982-01-02', 39, '10926 Highwood Way, El Paso, Texas', 9702197670, 'kylee0201@hotmail.com', NULL, NULL, NULL),
       (575419103, 'Olson Tracy', 'F', '1956-11-25', 65, '730 Field Ave, Taft, Texas', NULL, NULL, 2, '2020-11-19',	'2024-11-18');

INSERT INTO Accountant
VALUES (130001, 'Stokes Ashlee', 'ashleelee@gmail.com', 6012484710, '123'),
       (130002, 'Parisian Helen', 'helen321@hotmail.com', 5805694574, '123');

INSERT INTO Bill
VALUES (61461265, '2021-06-06',	100, 50, 1,	50,	292567083, '2021-06-06', 'cash', 130001),
       (98347142, '2021-06-11',	100, 100, NULL,	0, 415310368, '2021-06-11',	'cheque', 130002),
       (91479336, '2021-08-26',	5000, 100, 2, 4900,	575419103, '2021-08-26', 'cash', 130001);

INSERT INTO Department
VALUES (1, 'cardiology'),
       (2, 'general internal medicine');

INSERT INTO Doctor
VALUES (110001, 'Ziemann Timothy', 'ENT specialist', 28, '303 Valmar, Kemah, Texas', 5753361371, '123'),
       (110002,	'White Warren',	'orthopaedic surgeon', 33, '1105 Clover Dr, Burkburnett, Texas', 5805694580, '123'),
       (110003,	'Wehner Nico', 'cardiologist', 40, '369 Arnold Dr, Gordonville, Texas',	5809202612, '123');

INSERT INTO Doc_belong
VALUES (2, 110001),
       (2, 110002),
       (1 ,110003);

INSERT INTO Report
VALUES (41614184, 'test', 'Re-examination next 2 weeks', '2021-06-06', 110001, 292567083),
       (86116642, 'consult', 'Just need to use medicine', '2021-06-11',	110001, 415310368),
       (19782716, 'operation', 'Recoverd, re-examine next month', '2021-08-26',	110003, 575419103);

INSERT INTO Medicine
VALUES (10001, 'aspirin', 4, '2020-12-15', '2022-12-15', 200, 'Pfizer'),
       (10002, 'acetaminophen',	5, '2021-01-01', '2023-01-01', 300,	'Johnson & Johnson'),
       (10003, 'tylenol', 3, '2021-03-01', '2023-03-01', 400, 'Pfizer');

INSERT INTO Include
VALUES (86116642, 10001, 10);

INSERT INTO Disease
VALUES (1, 'Cold and Flu', 'Viruses cause both colds and flu by increasing inflammation of the membranes in the nose and throat.'),
       (2, 'Headaches',	'Affects a specific point of the head, often the eye, and is characterized by sharp, piercing pain.');

INSERT INTO Dis_treatment
VALUES (1, 'Drink lots of clear fluids (e.g., water, tea)'),
       (2, 'Ice pack held over the eyes or forehead'),
       (2, 'Sleep, or at least resting in a dark room');

INSERT INTO Cure
VALUES (10001, 2),
       (10002, 2),
       (10003, 1);

INSERT INTO Test
VALUES (1, 'ear checking', 100);

INSERT INTO Do_test
VALUES (1, 110001, 292567083, '2021-08-17', '2000');

INSERT INTO Operation
VALUES (1, 'heart operation', 3, '08:00:00');

INSERT INTO Operate
VALUES (1, 110003, 575419103, '2021-08-17 11:00:00', '2021-08-17 19:00:00', 999999);

INSERT INTO Appointment
VALUES ('2021-06-11', '08:00:00');

INSERT INTO Consult
VALUES ('2021-06-11', 110001, 415310368, 2000);

INSERT INTO Room
VALUES (1, 'recovery', 50, 'available'),
       (2, 'recovery', 100,	'available'),
       (3, 'surgery', NULL,	'used for surgery');

INSERT INTO Admit
VALUES (575419103, 2 ,10, 1000);

INSERT INTO Nurse
VALUES (120001, 'Willms Amy', 'cardiac', 40, 'day', '123'),
       (120002, 'Schmitt Erica', 'registered', 30, 'day', '123'),
       (120003, 'Blick Ken', 'registered', 34, 'night', '123');

INSERT INTO Nur_belong
VALUES (2, 120001),
       (2, 120002),
       (1 ,120003);

INSERT INTO Care
VALUES (575419103, 120001),
       (575419103, 120003);