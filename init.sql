CREATE DATABASE IF NOT EXISTS mydb;

USE mydb;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    department VARCHAR(100) NOT NULL,
    salary DECIMAL(10,2) NOT NULL
);


USE mydb;

INSERT INTO employees (name, email, department, salary)
VALUES
('Dinesh', 'dinesh@gmail.com', 'IT', 250000),
('Rahul', 'rahul@gmail.com', 'HR', 45000),
('Priya', 'priya@gmail.com', 'Finance', 55000),
('Arun', 'arun@gmail.com', 'Development', 65000),
('Sneha', 'sneha@gmail.com', 'Testing', 50000);
