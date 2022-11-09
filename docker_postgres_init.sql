CREATE TABLE Shops
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    key VARCHAR(255),
    type_key VARCHAR(255),
    image_key VARCHAR(255),
    image_type_key VARCHAR
);

CREATE TABLE Urls
(
    id SERIAL PRIMARY KEY,
    shop VARCHAR(255),
    name VARCHAR INTEGER REFERENCES Shops (name) ON DELETE CASCADE,
    url VARCHAR,
    last_prices REAL,
    prices REAL,
    category INT,
    image INT,
    character VARCHAR

);


CREATE TABLE Tabs
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE Prices
(
    id SERIAL PRIMARY KEY,
    id_product INTEGER REFERENCES Urls (id) ON DELETE CASCADE,
    price REAL,
    timestamp timestamp default current_timestamp
);


INSERT INTO shops (id, name, key, type_key, image_key, image_type_key) VALUES (2, 'Ozon', 'v0n', 'span', null, null);
INSERT INTO shops (id, name, key, type_key, image_key, image_type_key) VALUES (1, 'Wildberries', 'price-block__final-price', 'ins', 'img', 'photo-zoom__preview j-zoom-image hide');
INSERT INTO shops (id, name, key, type_key, image_key, image_type_key) VALUES (6, 'Mvideo', 'price__main-value', 'span', 'img', 'zoomable-image__image');
