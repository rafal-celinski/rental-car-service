CREATE TABLE SEGMENT (
    name VARCHAR(20) PRIMARY KEY,
    description TEXT
);

CREATE TABLE BRAND (
    name VARCHAR(20) PRIMARY KEY,
    logo BYTEA
);

CREATE TABLE MODEL (
    model_name VARCHAR(20) NOT NULL,
    brand_name VARCHAR(20) NOT NULL,
    segment_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (model_name, brand_name),
    FOREIGN KEY (brand_name) REFERENCES BRAND(name),
    FOREIGN KEY (segment_name) REFERENCES SEGMENT(name)
);

CREATE TABLE PRICE_LIST (
    model_name VARCHAR(20) NOT NULL,
    brand_name VARCHAR(20) NOT NULL,
    price NUMERIC NOT NULL,
    PRIMARY KEY (model_name, brand_name),
    FOREIGN KEY (model_name, brand_name) REFERENCES MODEL(model_name, brand_name)
);

CREATE TABLE CAR (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(20) NOT NULL,
    brand_name VARCHAR(20) NOT NULL,
    production_date DATE,
    mileage INTEGER NOT NULL,
    license_plate VARCHAR(9),
    VIN VARCHAR(17) NOT NULL,
    photo BYTEA,
    is_rented BOOLEAN NOT NULL DEFAULT FALSE,
    segment_name VARCHAR(20) NOT NULL,
    FOREIGN KEY (model_name, brand_name) REFERENCES MODEL(model_name, brand_name),
    FOREIGN KEY (segment_name) REFERENCES SEGMENT(name)
);

CREATE TABLE CLIENT (
    id SERIAL PRIMARY KEY,
    address TEXT NOT NULL
);

CREATE TABLE PERSON (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    pesel VARCHAR(20) NOT NULL,
    FOREIGN KEY (id) REFERENCES CLIENT(id)
);

CREATE TABLE COMPANY (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    nip VARCHAR(20) NOT NULL,
    FOREIGN KEY (id) REFERENCES CLIENT(id)
);

CREATE TABLE RENTAL (
    id SERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price NUMERIC NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    car_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    FOREIGN KEY (car_id) REFERENCES CAR(id),
    FOREIGN KEY (client_id) REFERENCES CLIENT(id)
);

CREATE TABLE INVOICE (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    date DATE NOT NULL,
    price_sum_netto NUMERIC,
    tax NUMERIC,
    FOREIGN KEY (client_id) REFERENCES CLIENT(id)
);

CREATE TABLE INVOICE_ELEMENT (
    invoice_id INTEGER NOT NULL,
    element_number INTEGER NOT NULL,
    rental_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    price NUMERIC NOT NULL,
    PRIMARY KEY (invoice_id, element_number),
    FOREIGN KEY (invoice_id) REFERENCES INVOICE(id),
    FOREIGN KEY (rental_id) REFERENCES RENTAL(id),
    FOREIGN KEY (car_id) REFERENCES CAR(id)
);
