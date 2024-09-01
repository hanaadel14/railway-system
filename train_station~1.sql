CREATE TABLE Station (
    Station_ID NUMBER PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    Location VARCHAR2(255) NOT NULL
);


CREATE TABLE Train (
    Train_ID NUMBER PRIMARY KEY,
    Capacity NUMBER NOT NULL,
    Type VARCHAR2(50) NOT NULL
);

-- Creating the SCHEDULE table
CREATE TABLE Train_Schedule (
    Schedule_ID NUMBER PRIMARY KEY,
    Train_ID NUMBER NOT NULL,
    DepartureTime TIMESTAMP NOT NULL,
    ArrivalTime TIMESTAMP NOT NULL,
    OriginStation_ID NUMBER NOT NULL,
    DestinationStation_ID NUMBER NOT NULL,
    FOREIGN KEY (Train_ID) REFERENCES Train(Train_ID),
    FOREIGN KEY (OriginStation_ID) REFERENCES Station(Station_ID),
    FOREIGN KEY (DestinationStation_ID) REFERENCES Station(Station_ID)
);

-- Creating the TICKET table
CREATE TABLE Ticket (
    Ticket_ID NUMBER PRIMARY KEY,
    Passenger_ID NUMBER NOT NULL,
    Schedule_ID NUMBER NOT NULL,
    Price NUMBER(10, 2) NOT NULL,
    SeatNumber VARCHAR2(10) NOT NULL,
    FOREIGN KEY (Passenger_ID) REFERENCES Passenger(Passenger_ID),
    FOREIGN KEY (Schedule_ID) REFERENCES Train_Schedule(Schedule_ID)
);

-- Creating the PASSENGER table
CREATE TABLE Passenger (
    Passenger_ID NUMBER PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    ContactInfo VARCHAR2(255)
);

-- Creating the EMPLOYEE table
CREATE TABLE Employee (
    Employee_ID NUMBER PRIMARY KEY,
    Name VARCHAR2(100) NOT NULL,
    Role VARCHAR2(100) NOT NULL,
    Station_ID NUMBER NOT NULL,
    FOREIGN KEY (Station_ID) REFERENCES Station(Station_ID)
);












-- Insert data into Station table
INSERT INTO Station (Station_ID, Name, Location) VALUES (1, 'Central Station', 'City Center');
INSERT INTO Station (Station_ID, Name, Location) VALUES (2, 'North Station', 'North District');
INSERT INTO Station (Station_ID, Name, Location) VALUES (3, 'South Station', 'South District');

-- Insert data into Train table
INSERT INTO Train (Train_ID, Capacity, Type) VALUES      (101, 200, 'Express');
INSERT INTO Train (Train_ID, Capacity, Type)  VALUES     (102, 150, 'Local');
INSERT INTO Train (Train_ID, Capacity, Type)   VALUES    (103, 180, 'High-Speed');

-- Insert data into Train_Schedule table
INSERT INTO Train_Schedule (Schedule_ID, Train_ID, DepartureTime, ArrivalTime, OriginStation_ID, DestinationStation_ID) VALUES  (1001, 101, TO_TIMESTAMP('2023-01-01 08:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2023-01-01 10:30:00', 'YYYY-MM-DD HH24:MI:SS'), 1, 2);
INSERT INTO Train_Schedule (Schedule_ID, Train_ID, DepartureTime, ArrivalTime, OriginStation_ID, DestinationStation_ID) VALUES  (1002, 102, TO_TIMESTAMP('2023-01-01 09:30:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2023-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 2, 3);
INSERT INTO Train_Schedule (Schedule_ID, Train_ID, DepartureTime, ArrivalTime, OriginStation_ID, DestinationStation_ID) VALUES   (1003, 103, TO_TIMESTAMP('2023-01-01 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2023-01-01 15:00:00', 'YYYY-MM-DD HH24:MI:SS'), 3, 1);

-- Insert data into Passenger table
INSERT INTO Passenger (Passenger_ID, Name, ContactInfo) VALUES (10001, 'John Doe', 'john.doe@example.com');
INSERT INTO Passenger (Passenger_ID, Name, ContactInfo) VALUES (10002, 'Jane Smith', 'jane.smith@example.com');
INSERT INTO Passenger (Passenger_ID, Name, ContactInfo) VALUES (10003, 'Bob Johnson', 'bob.johnson@example.com');

-- Insert data into Employee table
INSERT INTO Employee (Employee_ID, Name, Role, Station_ID) VALUES (2001, 'Alice Brown', 'Ticket Clerk', 1);
INSERT INTO Employee (Employee_ID, Name, Role, Station_ID) VALUES (2002, 'Charlie Davis', 'Conductor', 2);
INSERT INTO Employee (Employee_ID, Name, Role, Station_ID) VALUES (2003, 'Eva White', 'Station Manager', 3);

-- Insert data into Ticket table
INSERT INTO Ticket (Ticket_ID, Passenger_ID, Schedule_ID, Price, SeatNumber) VALUES (5001, 10001, 1001, 25.00, 'A101');
INSERT INTO Ticket (Ticket_ID, Passenger_ID, Schedule_ID, Price, SeatNumber) VALUES (5002, 10002, 1002, 20.00, 'B202');
INSERT INTO Ticket (Ticket_ID, Passenger_ID, Schedule_ID, Price, SeatNumber) VALUES (5003, 10003, 1003, 30.00, 'C303');





select * from station;

-- Granting necessary privileges to the user
GRANT SELECT, INSERT, UPDATE, DELETE ON Station TO system;
GRANT SELECT, INSERT, UPDATE, DELETE ON EMPLOYEE TO system;
GRANT SELECT, INSERT, UPDATE, DELETE ON PASSENGER TO system;
GRANT SELECT, INSERT, UPDATE, DELETE ON TICKET TO system;
GRANT SELECT, INSERT, UPDATE, DELETE ON TRAIN TO system;
GRANT SELECT, INSERT, UPDATE, DELETE ON TRAIN_SCHEDULE TO system;


COMMIT;

