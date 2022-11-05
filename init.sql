CREATE TABLE Urls
(
    id SERIAL PRIMARY KEY,
    shop VARCHAR(255),
    name VARCHAR(255),
    url VARCHAR,
    last_prices REAL,
    prices REAL,
    category INT,
    image INT,
    character VARCHAR

);

CREATE TABLE Shops
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    key VARCHAR(255),
    type_key VARCHAR(255),
    image_key VARCHAR(255),
    image_type_key VARCHAR
);

CREATE TABLE Tabs
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);