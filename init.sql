CREATE TABLE Urls
(
    id SERIAL PRIMARY KEY,
    shop VARCHAR(255),
    name VARCHAR(255),
    url VARCHAR(1000),
    last_prices REAL,
    prices REAL,
    category INT

);

CREATE TABLE Shops
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    key VARCHAR(255),
    type_key VARCHAR(255)
);

CREATE TABLE Tabs
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);