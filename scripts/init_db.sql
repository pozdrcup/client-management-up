CREATE DATABASE codac;
\c codac;

CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    contact_info TEXT,
    registration_date DATE NOT NULL,
    notes TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
    description TEXT,
    amount NUMERIC(10, 2) NOT NULL DEFAULT 0.00
);

-- Индексы (рекомендованы для поиска и связи)
CREATE INDEX idx_orders_client_id ON orders(client_id);
CREATE INDEX idx_clients_full_name ON clients(full_name);


