-- TEAM NAMES: Ryan Canete & Benjamin Rifleman
-- GROUP 65 - Planet Express

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- Create tables
-- Creates the planets table

CREATE OR REPLACE TABLE Planets(
    planet_id INT NOT NULL AUTO_INCREMENT,
    planet_name varchar(60) NOT NULL UNIQUE,
    distance_from_hq FLOAT NOT NULL,
    description varchar(145) NOT NULL,
    PRIMARY KEY (planet_id)
);

-- Creates the Customers table
CREATE OR REPLACE TABLE Customers (
customer_id INT NOT NULL AUTO_INCREMENT,
customer_name varchar(145) NOT NULL,
customer_email varchar(145) NOT NULL,
planet_id INT NULL,
PRIMARY KEY (customer_id),
FOREIGN KEY (planet_id) REFERENCES Planets(planet_id)
);

-- Creates Shipment types table
CREATE OR REPLACE TABLE Shipment_types (
    shipment_type_id INT NOT NULL AUTO_INCREMENT,
    shipment_time varchar(145) NOT NULL,
    is_active INT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (shipment_type_id)
);

-- Creates the Shipment invoices table
CREATE OR REPLACE TABLE Shipment_invoices (
    invoice_id INT NOT NULL AUTO_INCREMENT,
    cost FLOAT NOT NULL,
    planet_id INT NOT NULL,
    customer_id INT,
    shipment_type_id INT NOT NULL,
    PRIMARY KEY (invoice_id),
    FOREIGN KEY (planet_id) REFERENCES Planets(planet_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (shipment_type_id) REFERENCES Shipment_types(shipment_type_id) ON DELETE CASCADE
);

-- Creates the Packages table
CREATE OR REPLACE TABLE Packages (
    package_id INT NOT NULL AUTO_INCREMENT,
    weight FLOAT NOT NULL,
    hazards varchar(45) DEFAULT NULL,
    invoice_id INT NOT NULL,
    recipient varchar(145) DEFAULT NULL,
    PRIMARY KEY (package_id),
    FOREIGN KEY (invoice_id) REFERENCES Shipment_invoices(invoice_id) ON DELETE CASCADE
);

-- Insert Sample data
-- Planet Data
INSERT INTO Planets (planet_name, distance_from_hq, description)
VALUES
    ('Earth', 0, 'Home planet of the Planet Express crew'),
    ('Mars', 0.38, 'The red planet'),
    ('Uranus', 19.2, 'The coldest planet in the solar system'),
    ('Pluto', 39.5, 'The smallest planet in the solar system'),
    ('Saturn', 9.5, 'The planet with the most rings'),
    ('Jupiter', 5.2, 'The largest planet in the solar system'),
    ('Neptune', 30.1, 'The planet with the strongest winds'),
    ('Mercury', 0.39, 'The closest planet to the sun'),
    ('Venus', 0.72, 'The hottest planet in the solar system'),
    ('Moon', 0.00257, 'The only natural satellite of Earth');

-- Customer Data
INSERT INTO Customers (customer_name, customer_email, planet_id)
VALUES
    ('Zapp Brannigan', 'zapbran@doop.com', (SELECT planet_id FROM Planets WHERE planet_name = 'Earth')),
    ('Amy Wong', 'amy.wong@femputer.com', (SELECT planet_id FROM Planets WHERE planet_name = 'Mars')),
    ('Hermes Conrad', 'hermes.conrad@bureaucrat.com', (SELECT planet_id FROM Planets WHERE planet_name = 'Earth')),
    ('Turanga Leela', 'leela_t@mutantsforjustice.org', (SELECT planet_id FROM Planets WHERE planet_name = 'Earth')),
    ('Philip Fry', "fry_2000@mail.com", (SELECT planet_id FROM Planets WHERE planet_name = 'Earth')),
    ('Bender Bending Rodriguez', "bender_moon_base@momsrobots.com", (SELECT planet_id FROM Planets WHERE planet_name = 'Moon'));

-- Insert Shipment types data
INSERT INTO Shipment_types (shipment_time, is_active)
VALUES
    ('1 day', 1),
    ('2 days', 1),
    ('3 days', 1),
    ('4 days', 1),
    ('5 days', 1),
    ('6 days', 0),
    ('7 days', 1);

-- Insert Shipment invoices data
INSERT INTO Shipment_invoices (cost, planet_id, customer_id, shipment_type_id)
VALUES
    (300, (SELECT planet_id FROM Planets WHERE planet_name = 'Mars'), (SELECT customer_id FROM Customers WHERE customer_name = 'Zapp Brannigan'), (SELECT shipment_type_id FROM Shipment_types WHERE shipment_time = '1 day')),
    (225, (SELECT planet_id FROM Planets WHERE planet_name = 'Earth'), (SELECT customer_id FROM Customers WHERE customer_name = 'Amy Wong'), (SELECT shipment_type_id FROM Shipment_types WHERE shipment_time = '2 days')),
    (100, (SELECT planet_id FROM Planets WHERE planet_name = 'Venus'), (SELECT customer_id FROM Customers WHERE customer_name = 'Hermes Conrad'), (SELECT shipment_type_id FROM Shipment_types WHERE shipment_time = '3 days')),
    (50, (SELECT planet_id FROM Planets WHERE planet_name = 'Earth'), (SELECT customer_id FROM Customers WHERE customer_name = 'Turanga Leela'), (SELECT shipment_type_id FROM Shipment_types WHERE shipment_time = '4 days')),
    (150, (SELECT planet_id FROM Planets WHERE planet_name = 'Moon'), (SELECT customer_id FROM Customers WHERE customer_name = 'Philip Fry'), (SELECT shipment_type_id FROM Shipment_types WHERE shipment_time = '7 days'));

-- Insert Packages data
INSERT INTO Packages (weight, hazards, invoice_id, recipient)
VALUES
    (10, NULL, (SELECT invoice_id FROM Shipment_invoices WHERE cost = 300), "Amy Wong"),
    (5, NULL, (SELECT invoice_id FROM Shipment_invoices WHERE cost = 225) , "Hermes Conrad"),
    (2, NULL, (SELECT invoice_id FROM Shipment_invoices WHERE cost = 100), "Femputer"),
    (1, NULL, (SELECT invoice_id FROM Shipment_invoices WHERE cost = 50), "Professor Farnsworth"),
    (20, 'Radiation', (SELECT invoice_id FROM Shipment_invoices WHERE cost = 150), "Bender Bending Rodriguez");



SET FOREIGN_KEY_CHECKS = 1;
COMMIT;