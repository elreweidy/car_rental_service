CREATE DATABASE car_rental_system;
USE car_rental_system;

CREATE TABLE vehicles (
  vehicle_id INT NOT NULL AUTO_INCREMENT,
  category VARCHAR(20) NOT NULL,
  available VARCHAR(20) DEFAULT 'Yes',
  CHECK (available IN ('Yes', 'No')),
  PRIMARY KEY (vehicle_id)
);

CREATE TABLE customers (
  customer_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL,
  address VARCHAR(100),
  PRIMARY KEY (customer_id)
);


CREATE TABLE bookings (
  booking_id INT NOT NULL AUTO_INCREMENT,
  customer_id INT NOT NULL,
  vehicle_id INT NOT NULL,
  hire_date DATE NOT NULL,
  return_date DATE NOT NULL,
  PRIMARY KEY (booking_id),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);

CREATE TABLE invoices (
  invoice_id INT NOT NULL AUTO_INCREMENT,
  booking_id INT NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (invoice_id),
  UNIQUE (booking_id),
  FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);


-- To insert data into tables, we can use the INSERT INTO statement

-- Insert vehicles
INSERT INTO vehicles (category) VALUES 
('Small Car'),
('Small Car'),
('Small Car'),
('Family Car'),
('Family Car'),
('Van');

-- Insert customers
INSERT INTO customers (name, email) VALUES 
('John Doe', 'john.doe@example.com'),
('Jane Doe', 'jane.doe@example.com'),
('Bob Smith', 'bob.smith@example.com');

-- Make a booking
-- We assume that customer with customer_id = 1 wants to rent a Small Car (vehicle_id = 1) from today (2023-03-10) to 2023-03-17
INSERT INTO bookings (customer_id, vehicle_id, hire_date, return_date) VALUES 
(1, 1, '2023-03-10', '2023-03-17');

-- Create an invoice for the booking
-- We assume that the amount to be paid is $150.00
INSERT INTO invoices (booking_id, amount) VALUES 
(1, 150.00);



