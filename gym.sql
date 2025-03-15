create database gym ;
use gym;
-- Trainee Table
CREATE TABLE Trainee (
    Trainee_ID INT PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Phone_Number VARCHAR(20),
    SNN VARCHAR(20),
    AddressTrainee VARCHAR(255),
    AgeTrainee INT
);
-- Membership Plan Table
CREATE TABLE Membership (
    membership_id INT PRIMARY KEY,
    membership_type VARCHAR(50) NOT NULL,
    class_tiers INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
CREATE TABLE Member_Membership (
    member_id INT,
    membership_id INT,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'active',
    PRIMARY KEY (member_id, membership_id),
    FOREIGN KEY (member_id) REFERENCES trainee(trainee_id) ON DELETE CASCADE,
    FOREIGN KEY (membership_id) REFERENCES Membership(membership_id) ON DELETE CASCADE
);
describe membership;

-- Trainer Table
CREATE TABLE Trainer (
    Trainer_ID INT auto_increment PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
   Address_trainers VARCHAR(255),
    PhoneNumber_Trainer VARCHAR(20),
    SNNTrainer VARCHAR(20),
    Salary DECIMAL(10, 2)CHECK (Salary >= 0),
    Specialty VARCHAR(50),
    AgeTrainer INT
);

-- Class Table
CREATE TABLE Class (
    Class_ID INT auto_increment PRIMARY KEY ,
    Class_Name VARCHAR(50),
    Start_Time TIME,
    End_Time TIME,
    Capacity INT CHECK (Capacity > 0),
    Trainer_ID INT,
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID) on delete cascade
);

-- Subscription Table
CREATE TABLE Food_Subscription (
   Subscription_ID INT PRIMARY KEY,
   Subscription_Type VARCHAR(50) not null,
   meal_option varchar(20) not null,
   meal_description text,
   price decimal not null
);

-- Payment Table
CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY,
    Trainee_ID INT ,
    PaymentAmount DECIMAL(10, 2) CHECK (PaymentAmount >= 0),
    Payment_Date DATE,
    PaymentDue_Date DATE,
    PaymentStatus VARCHAR(50),
    Method VARCHAR(50),
    FOREIGN KEY (Trainee_ID) REFERENCES Trainee(Trainee_ID) on delete cascade
);

-- Program Table
CREATE TABLE Program (
    Program_ID INT PRIMARY KEY,
    Program_Name VARCHAR(50),
    Start_DateProgram DATE,
    End_DateProgram DATE ,
    Program_Type VARCHAR(50),
    Trainer_ID INT,
    Trainee_ID INT,
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID)ON DELETE SET NULL,
    FOREIGN KEY (Trainee_ID) REFERENCES Trainee(Trainee_ID)ON DELETE SET NULL
);

-- Schedule Table
CREATE TABLE Train (
    Schedule_ID INT PRIMARY KEY,
    Trainer_ID INT,
    Trainee_ID INT,
    TrainTime TIME,
    FOREIGN KEY (Trainer_ID) REFERENCES Trainer(Trainer_ID),
    FOREIGN KEY (Trainee_ID) REFERENCES Trainee(Trainee_ID)
);

-- Enrollment Table
CREATE TABLE Enrollment (
    PRIMARY KEY (Trainee_ID, Class_ID),
    Trainee_ID INT,
    Class_ID INT,
    Date_Enrollment DATE,
    FOREIGN KEY (Trainee_ID) REFERENCES Trainee(Trainee_ID),
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID) on delete cascade 
);

CREATE TABLE Plan (
    membership_id INT,
    Trainee_ID INT,
    Subscription_ID INT,
    Start_DatePlan DATE,
    End_DatePlan DATE,
    Subscription_Type VARCHAR(50),
    PRIMARY KEY (membership_id, Trainee_ID, Subscription_ID),
    FOREIGN KEY (membership_id) REFERENCES Membership(membership_id),
    FOREIGN KEY (Trainee_ID) REFERENCES Trainee(Trainee_ID),
    FOREIGN KEY (Subscription_ID) REFERENCES Food_Subscription(Subscription_ID)
);

CREATE TABLE Bill (
    Bill_ID INT PRIMARY KEY,
    Trainee_ID INT,
    BillAmount DECIMAL(10, 2)CHECK (BillAmount >= 0),
    Bill_Date DATE,
    Due_Date DATE,
	BillStatus boolean,
    BillMethod VARCHAR(50),
    FOREIGN KEY (Trainee_ID) REFERENCES Trainee(Trainee_ID) on delete cascade
);

-- table to connect the trainee and foodsubscription
create table member_food_subscription(
member_id int,
plan_id int,
start_date date,
end_date date,
primary key(member_id, plan_id),
 FOREIGN KEY (member_id) REFERENCES Trainee(Trainee_ID) on delete cascade,
FOREIGN KEY (plan_id) REFERENCES food_subscription(subscription_id) on delete cascade
);

-- ----------------------------------------------------------


select * from trainer ; 
describe trainer;
SET SQL_SAFE_UPDATES = 0;
delete from trainer;
SET SQL_SAFE_UPDATES = 1;

show tables;
select * from trainer;
describe trainer;

ALTER TABLE Trainer
ADD CONSTRAINT unique_phone UNIQUE (PhoneNumber_Trainer),
ADD CONSTRAINT unique_ssn UNIQUE (SNNTrainer);


ALTER TABLE Trainer MODIFY Specialty VARCHAR(255);



ALTER TABLE train
DROP FOREIGN KEY train_ibfk_1;

ALTER TABLE train
ADD CONSTRAINT train_ibfk_1 FOREIGN KEY (Trainer_ID) REFERENCES trainer(Trainer_ID) ON DELETE CASCADE;
SELECT * FROM class;
SET SQL_SAFE_UPDATES = 0;
delete from class;
SET SQL_SAFE_UPDATES = 1;


INSERT INTO Trainee (Trainee_ID, First_Name, Last_Name, Phone_Number, SNN, AddressTrainee, AgeTrainee)
VALUES 
(1, 'John', 'Doe', '1234567890', '111-22-3333', '123 Elm Street', 25),
(2, 'Jane', 'Smith', '0987654321', '222-33-4444', '456 Oak Street', 30),
(3, 'Emily', 'Clark', '5647382910', '321-43-8765', '789 Birch St', 28);

INSERT INTO Membership (membership_id, membership_type, class_tiers, price)
VALUES 
(1, 'Basic', 5, 50.00),
(2, 'Premium', 10, 100.00),
(3, 'VIP', 20, 200.00);

INSERT INTO Member_Membership (member_id, membership_id, start_date, end_date, status)
VALUES 
(1, 1, '2024-01-01', '2024-12-31', 'active'),
(2, 2, '2024-01-01', '2024-12-31', 'active'),
(3, 3, '2024-01-01', '2024-12-31', 'inactive');


INSERT INTO Trainer (Trainer_ID, First_Name, Last_Name, Address_trainers, PhoneNumber_Trainer, SNNTrainer, Salary, Specialty, AgeTrainer)
VALUES 
(1, 'David', 'Williams', '456 Pine St', '9988776655', '777889999', 55000.00, 'Yoga', 38),
(2, 'Olivia', 'Taylor', '789 Walnut St', '4433221100', '222334444', 58000.00, 'Crossfit', 32),
(3, 'Michael', 'Johnson', '123 Cedar St', '5566778899', '111223344', 50000.00, 'Cardio', 40);

INSERT INTO Class (Class_ID, Class_Name, Start_Time, End_Time, Capacity, Trainer_ID)
VALUES 
(1, 'Yoga', '09:00:00', '10:00:00', 20, 1),
(2, 'Crossfit', '11:00:00', '12:00:00', 18, 2),
(3, 'Cardio', '08:00:00', '09:00:00', 25, 3);

INSERT INTO Food_Subscription (Subscription_ID, Subscription_Type, meal_option, meal_description, price)
VALUES 
(1, 'Vegan', 'Low-Calorie', 'Low-calorie meals for weight management', 100.00),
(2, 'Keto', 'Low-Carb', 'Low-carb meals for ketogenic diets', 120.00),
(3, 'Gluten-Free', 'Allergen-Free', 'Meals suitable for gluten-sensitive individuals', 110.00);

INSERT INTO Payment (Payment_ID, Trainee_ID, PaymentAmount, Payment_Date, PaymentDue_Date, PaymentStatus, Method)
VALUES 
(1, 1, 50.00, '2024-01-10', '2024-01-15', 'Paid', 'Credit Card'),
(2, 2, 100.00, '2024-01-12', '2024-01-17', 'Unpaid', 'Bank Transfer'),
(3, 3, 200.00, '2024-01-15', '2024-01-20', 'Paid', 'Cash');


INSERT INTO Program (Program_ID, Program_Name, Start_DateProgram, End_DateProgram, Program_Type, Trainer_ID, Trainee_ID)
VALUES 
(1, 'Yoga Basics', '2024-02-01', '2024-04-01', 'Beginner', 1, 1),
(2, 'Advanced Crossfit', '2024-03-01', '2024-05-01', 'Advanced', 2, 2),
(3, 'Cardio Blast', '2024-04-01', '2024-06-01', 'Intermediate', 3, 3);


INSERT INTO Train (Schedule_ID, Trainer_ID, Trainee_ID, TrainTime)
VALUES 
(1, 1, 1, '15:00:00'),
(2, 2, 2, '16:00:00'),
(3, 3, 3, '17:00:00');


INSERT INTO Enrollment (Trainee_ID, Class_ID, Date_Enrollment)
VALUES 
(1, 1, '2024-01-15'),
(2, 2, '2024-01-20'),
(3, 3, '2024-01-25');

INSERT INTO Plan (membership_id, Trainee_ID, Subscription_ID, Start_DatePlan, End_DatePlan, Subscription_Type)
VALUES 
(1, 1, 1, '2024-01-01', '2024-12-31', 'Basic'),
(2, 2, 2, '2024-01-01', '2024-12-31', 'Premium'),
(3, 3, 3, '2024-01-01', '2024-12-31', 'VIP');

INSERT INTO Bill (Bill_ID, Trainee_ID, BillAmount, Bill_Date, Due_Date, BillStatus, BillMethod)
VALUES 
(1, 1, 50.00, '2024-01-10', '2024-01-15', TRUE, 'Credit Card'),
(2, 2, 100.00, '2024-01-12', '2024-01-17', FALSE, 'Bank Transfer'),
(3, 3, 200.00, '2024-01-15', '2024-01-20', TRUE, 'Cash');


INSERT INTO member_food_subscription (member_id, plan_id, start_date, end_date)
VALUES 
(1, 1, '2024-01-01', '2024-12-31'),
(2, 2, '2024-01-01', '2024-12-31'),
(3, 3, '2024-01-01', '2024-12-31');







