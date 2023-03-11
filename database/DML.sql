-- Database Manipulation queries Project Step 3 Draft

-- ALL THE READ/SELECT STATEMENTS 

-- get all Customers information to populate page
SELECT Customers.customer_id, customer_name, customer_email, Planets.planet_name AS home 
FROM Customers INNER JOIN Planets ON Customers.planet_id = Planets.planet_id
ORDER BY customer_name ASC;

-- get all planet data for planet page
SELECT planet_id, planet_name, description, distance_from_hq FROM Planets;

-- get all shipment types
SELECT shipment_type_id, shipment_time, is_active FROM Shipment_types;

-- get all packages
SELECT package_id, weight, hazards, Shipment_invoices.invoice_id, recipient
FROM Packages INNER JOIN Shipment_invoices ON Packages.invoice_id = Shipment_invoices.invoice_id;

-- get all shipment Inovices
SELECT invoice_id, cost, Planets.planet_name AS destination, Customers.customer_name AS sender, Shipment_types.shipment_time AS shipping
FROM Shipment_invoices 
INNER JOIN Planets ON Shipment_invoices.planet_id = Planets.planet_id
INNER JOIN Customers ON Shipment_invoices.customer_id = Customers.customer_id
INNER JOIN Shipment_types ON Shipment_invoices.shipment_type_id = Shipment_types.shipment_type_id;

-- get drow down menu queries
--planets
SELECT planet_id, planet_name FROM Planets

-- customers
SELECT customer_id, customer_name FROM Customers

-- shipment types
SELECT shipment_type_id, shipment_time FROM Shipment_types



-- ALL THE CREATE/ADD STATEMENTS
-- All queries to add will be marked with a : character which will denote
-- the variables that will have data from the backend programming language


-- Add Cusomter
INSERT INTO Customers(customer_name,customer_email, planet_id)
VALUES (:customer_name_Input, :customer_email_Input, :planet_id_from_dropdown_Input);

-- Add planet
INSERT INTO Planets(planet_name, distance_from_hq, description)
VALUES (:planet_name_Input, :distance_from_hq_Input, :discription_Input);

-- Add Shipment types
INSERT INTO Shipment_types(shipment_time, is_active)
VALUES (:shipment_time_Input, :is_active_Input);

-- Add Packages
INSERT INTO Packages(weight, hazards, invoice_id, recipient)
VALUES (:weight_Input, :hazards_Input, :invoice_id_Input, :recipient_Input);

-- Add Shipment Invoices
INSERT INTO Shipment_invoices(cost, planet_id, customer_id, shipment_type_id)
VALUES (:cost_Input, :planet_id_dropdown_Input:, :customer_id_Input, :shipment_type_id_Input)

-- ALL THE UPDATE STATEMENTS
-- All queries to add will be marked with a : character which will denote
-- the variables that will have data from the backend programming language
-- These will be inplemented where the UI will take populate the correct FK by looking up the information given.

-- Update a customers data
UPDATE Customers 
SET customer_name = :customer_name_Input, customer_email = :customer_email_Input, planet_id = :planet_id_from_dropdown_Input
WHERE customer_id = :customer_id_from_update_form;

-- Updates shipment_invoices
Update Shipment_invoices
SET cost = :cost_Input, planet_id = :planet_id_dropdown_Input, customer_id = :customer_id_Input, shipment_type_id = :shipment_type_id_Input
WHERE invoice_id = :invoice_id_Input;



-- ALL THE DELETE STATEMENTS
-- All queries to add will be marked with a : character which will denote
-- the variables that will have data from the backend programming language

-- Deletes a customer
DELETE FROM Customers WHERE customer_id = :customer_id_selected_from_customer_page;

-- Deletes a Shipment_invoice
-- This also deletes that packages that are associated with this, but might want to chage to null instead.
DELETE FROM Shipment_invoices WHERE invoice_id = :invoice_id_selected_from_shipment_invoices_page;

-- Deletes a Planet
-- Deletes any customers that are tied to this planet, might want to change this at a later date
DELETE FROM Planets WHERE planet_id = :planet_id_selected_from_planets_page;