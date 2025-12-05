CREATE DATABASE client_db;
\c client_db;

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    contact_info TEXT,
    registration_date DATE NOT NULL,
    notes TEXT
);
