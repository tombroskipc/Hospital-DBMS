-- INSERT data
INSERT INTO Insurance_company
VALUES (1, 'American Health', '2157 Swain Rd, Eaton, Ohio', 9374562728),
       (2, 'Health Star', '250 Lone Pine Rd, Saint Landry, Louisiana', 3188382464);

INSERT INTO Patient
VALUES (292567083, 'Dare Lucas', 'M', '1980-02-14',    41, '7416 Ireland Ct, El Paso, Texas', 9452170294, 'lucas123@gmail.com', 1,    '2020-12-19', '2022-12-18'),
       (415310368, 'Raynor Kylee', 'F', '1982-01-02', 39, '10926 Highwood Way, El Paso, Texas', 9702197670, 'kylee0201@hotmail.com', NULL, NULL, NULL),
       (575419103, 'Olson Tracy', 'F', '1956-11-25', 65, '730 Field Ave, Taft, Texas', NULL, NULL, 2, '2020-11-19', '2024-11-18'),
       (847593274, 'Stacy Trump', 'F', '1971-12-11', 50, '178 Kingston Dr, Texas', 9402513283, NULL, 2, '2021-02-10', '2025-02-09'),
       (347195617, 'Watfort Gates', 'M', '1976-05-29', 45, '230 Amberjack Dr, Texas', NULL, NULL, 2, '2020-06-13','2024-06-12'),
       (195672894, 'James Lucas', 'M', '1982-03-21',   39, '718 Ward Street, Sealy, Texas', 9452170294, 'lucas123@gmail.com', 1, '2020-12-19', '2022-12-18'),
       (104769374, 'Antolony Andariel', 'F', '1990-09-24',    31, '7416 Ireland Ct, El Paso, Texas', 9452170294, 'rooneyfam1990@gmail.com', 2, '2020-12-19', '2022-06-28'),
       (937683104, 'Gabriel Rooney', 'M', '1985-08-15',    36, '7416 Ireland Ct, El Paso, Texas', 9452170294, 'rooneyfam1985@gmail.com', 1,    '2020-10-11', '2022-10-10');
INSERT INTO Accountant
VALUES (130001, 'Stokes Ashlee', 'ashleelee@gmail.com', 6012484710, '123'),
       (130002, 'Parisian Helen', 'helen321@hotmail.com', 5805694574, '123');
INSERT INTO Accountant
VALUES (130003, 'Stokes Ashlee', 'ashleelee@gmail.com', 6012484710, '123'),
       (130004, 'Parisian Helen', 'helen321@hotmail.com', 5805694574, '123');

INSERT INTO Bill
VALUES (61461265, '2021-06-06',	100, 50, 1,	50,	292567083, '2021-06-06', 'cash', 130001),
       (98347142, '2021-06-11',    100, 100, NULL,    0, 415310368, '2021-06-11',    'cheque', 130002),
       (93759227, '2021-08-26',    5000, 100, 2, 4900,    575419103, '2021-08-26', 'cash', 130001),
       (17394762, '2021-01-29',    500, 100, 2, 400,    847593274, '2021-01-29', 'cash', 130001),
       (32175973, '2021-02-22',    350, 100, 2, 250,    347195617, '2021-02-22', 'cheque', 130001),
       (49571947, '2021-05-16',    300, 180, 2, 120,    195672894, '2021-05-16', 'cash', 130001),
       (37832842, '2021-06-21',    700, 100, 2, 600,    104769374, '2021-06-21', 'cheque', 130001),
       (27492744, '2021-02-14',    350, 350, 2, 4900,    937683104, '2021-02-14', 'cash', 130001);

INSERT INTO Department
VALUES (1, 'cardiology'),
       (2, 'general internal medicine'),
       (3, 'dematologist');

INSERT INTO Doctor
VALUES (110001, 'Ziemann Timothy', 'ENT specialist', 28, '303 Valmar, Kemah, Texas', 5753361371, '123'),
       (110002,    'White Warren',    'orthopaedic surgeon', 33, '1105 Clover Dr, Burkburnett, Texas', 5805694580, '123'),
       (110003,    'Wehner Nico', 'cardiologist', 40, '369 Arnold Dr, Gordonville, Texas',    5809202612, '123'),
(110004,'Mary James', 'dematologist', 40, '369 Arnold Dr, Gordonville, Texas',    5809202612, '123'),
(110005,    'Thiago James', 'dematologist', 48, '2252 Kolt Ct, El Paso, Texas',    5829471738, '123'),
(110006,    'Richard Johnson', 'Endocrinologists', 37, '311640 Great Abaco Ct, El Paso,  Texas',    5809202612, '123'),
(110007,    'Wehner Nico', 'Gastroenterologists', 41, '369 Arnold Dr, Gordonville, Texas',    5809202612, '123'),
(110008,    'Mave Helen', 'Internists', 52, '112 Richard Dr, Gordonville, Texas',    5809202612, '123'),
(110009,    'Bill Ashley', 'cardiologist', 56, '252 Pueblo Dr, Gordonville, Texas',    5809202612, '123');
INSERT INTO Doc_belong
VALUES (2, 110001),
       (2, 110002),
       (1 ,110003),
    (3 ,110004),
    (3 ,110005),
    (2 ,110006),
    (2 ,110007),
    (2 ,110008),
    (1 ,110009);


INSERT INTO Report
VALUES (41614184, 'test', 'Re-examination next 2 weeks', '2021-06-06', 110001, 292567083),
       (86116642, 'consult', 'Just need to use medicine', '2021-06-11',    110001, 415310368),
       (19782716, 'operation', 'Recoverd, re-examine next month', '2021-08-26',    110003, 575419103),
       (83918364, 'test', 'Re-examination next 2 weeks', '2021-03-12',    110006, 347195617),
       (84375627, 'consult', 'Use medicine frequently', '2021-03-12',    110007, 347195617),
       (36582659, 'test', 'Re-examination next 3 weeks', '2021-06-11',    110003, 104769374),
       (30937583, 'consult', 'Just need to use medicine', '2021-06-11',    110003, 104769374),
       (21946528, 'operation', 'Recovering', '2021-08-12',    110001, 847593274),
       (21946529, 'consult', 'Eat and drink a lot of juice and beef', '2021-08-12',    110004, 195672894),
       (40598723, 'consult', 'Bounteous Protein', '2020-12-31', 110006, 937683104)
;

INSERT INTO Medicine
VALUES (10001, 'aspirin', 4, '2020-12-15', '2022-12-15', 200, 'Pfizer'),
       (10002, 'acetaminophen',    5, '2021-01-01', '2023-01-01', 300,    'Johnson & Johnson'),
       (10003, 'acetaminophen', 3, '2021-03-01', '2023-03-01', 400, 'Pfizer'),
       (10004, 'Gastrointestinal', 3, '2021-06-01', '2023-06-01', 400, 'Antacids'),
       (10005, 'Gastrointestinal', 3, '2021-08-04', '2023-08-04', 400, 'Proton Pump Inhibitors'),
       (10006, 'tylenol', 3, '2021-03-12', '2023-03-12', 250, 'Androgens');

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
VALUES (1, 110001, 292567083, '2021-06-06', 10);

INSERT INTO Operation
VALUES (1, 'heart operation', 3, '11:00:00');

INSERT INTO Operate
VALUES (1, 110003, 575419103, '2021-06-06 10:10:10', '2021-06-06 20:10:10', 500);

INSERT INTO Appointment
VALUES (1, '1:00:00');

INSERT INTO Consult
VALUES (1, 110001, 415310368, '2021-06-11', 200);

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

INSERT INTO Care
VALUES (575419103, 120001),
       (575419103, 120003);
