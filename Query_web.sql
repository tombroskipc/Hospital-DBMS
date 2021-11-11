SELECT * FROM Patient WHERE LOWER(Pat_name) LIKE '%dare%';

SELECT Medicine.Mdc_id, Mdc_name, Dis_name, Price, MFG, EXP, Quantity, Manufacturer
FROM Medicine, Disease, Cure
WHERE Mdc_name LIKE '%' AND Medicine.Mdc_id = Cure.Mdc_id AND Cure.Dis_id = Disease.Dis_id;

SELECT Report.Re_id, Pat_name, Doc_name, Category, Description,
FROM Report, Doctor, Patient
WHERE (Date BETWEEN '2021-05-10' AND '2021-11-10') AND Report.Ssn = Patient.Ssn AND Report.Doc_id = Doctor.Doc_id;

SELECT * FROM Patient WHERE Start_date = '2021-11-01';

SELECT Patient.Ssn, Patient.Pat_name, Patient.Sex, Patient.DOB, Patient.Age, Patient.Address, Patient.Tel_no, Patient.Email, Insurance_company.InsCo_name, Patient.Start_date, Patient.End_date
FROM Patient, Insurance_company
WHERE Patient.Ssn LIKE '%292567083%' AND Patient.InsCo_id = Insurance_company.InsCo_id;


SELECT EXISTS(SELECT * FROM Report WHERE Re_id = 19782716);