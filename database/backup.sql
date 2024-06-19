--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: create_invoice(integer, date, date); Type: PROCEDURE; Schema: public; Owner: projekt
--

CREATE PROCEDURE public.create_invoice(IN p_client_id integer, IN p_start_date date, IN p_end_date date)
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_rental_id INTEGER;
    v_rental_price NUMERIC;
    v_element_num INTEGER;
    v_invoice_id INTEGER;
    v_total_price NUMERIC := 0;
    v_car_id INTEGER;
BEGIN
    v_element_num := 1;

    -- Calculate the total price of the rentals
    FOR v_rental_id, v_rental_price IN
        (SELECT id, price
         FROM RENTAL
         WHERE active = FALSE
           AND client_id = p_client_id
           AND end_date BETWEEN p_start_date AND p_end_date)
        LOOP
            v_total_price := v_total_price + v_rental_price;
        END LOOP;

    -- Raise an exception if the total price is zero or below the threshold
    IF v_total_price <= 0 THEN
        RAISE EXCEPTION 'Total price for invoice must be greater than zero. Total price: %', v_total_price;
    END IF;

    -- Create the invoice
    INSERT INTO INVOICE (client_id, date, price_sum_netto, tax)
    VALUES (p_client_id, CURRENT_DATE, v_total_price, v_total_price * 0.08)
    RETURNING id INTO v_invoice_id;

    -- Insert the invoice elements
    FOR v_rental_id, v_car_id, v_rental_price in
        (SELECT id, car_id, price
         FROM RENTAL
         WHERE active = FALSE
           AND client_id = p_client_id
           AND end_date BETWEEN p_start_date AND p_end_date)
        LOOP
            INSERT INTO INVOICE_ELEMENT (invoice_id, element_number, rental_id,car_id, price)
            VALUES (v_invoice_id, v_element_num, v_rental_id,v_car_id, v_rental_price);
            v_element_num := v_element_num + 1;
        END LOOP;
END;
$$;


ALTER PROCEDURE public.create_invoice(IN p_client_id integer, IN p_start_date date, IN p_end_date date) OWNER TO projekt;

--
-- Name: disallow_rental_reactivation(); Type: FUNCTION; Schema: public; Owner: projekt
--

CREATE FUNCTION public.disallow_rental_reactivation() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.active = TRUE THEN
        RAISE EXCEPTION 'Cannot reactivate rental';
    ELSIF NEW.active = FALSE AND NEW.active = OLD.active THEN
        RAISE EXCEPTION 'Rental with id % is already not active', NEW.id;
    END IF;
    RETURN NEW; -- Ensure the function returns the new record
END;
$$;


ALTER FUNCTION public.disallow_rental_reactivation() OWNER TO projekt;

--
-- Name: end_rent(integer); Type: PROCEDURE; Schema: public; Owner: projekt
--

CREATE PROCEDURE public.end_rent(IN p_rent_id integer)
    LANGUAGE plpgsql
    AS $$
        DECLARE
            v_active BOOLEAN;
            v_start_date DATE;
            v_estimated_end_date DATE;
            v_end_date DATE;
            v_estimated_price NUMERIC;
            v_estimated_duration INTEGER;
            v_duration INTEGER;
            v_price_per_day NUMERIC;
            v_price NUMERIC;
            v_car_id INTEGER;
        BEGIN
            SELECT start_date, end_date, price, active, car_id
            INTO v_start_date, v_estimated_end_date, v_estimated_price, v_active, v_car_id
            FROM RENTAL
            WHERE id = p_rent_id;

            IF v_active = FALSE THEN
                RAISE EXCEPTION 'Rent with id % is not active', p_rent_id;
            END IF;

            v_estimated_duration := v_estimated_end_date - v_start_date;
            v_price_per_day = v_estimated_price / v_estimated_duration;

            v_end_date = current_date;
            v_duration = v_end_date - v_start_date;
            IF v_duration > v_estimated_duration THEN
                -- in case of a rental extension, add a price according to the current car price
                v_price = v_estimated_price + (v_duration - v_estimated_duration) * get_car_price(v_car_id);
            ELSIF v_duration < v_estimated_duration THEN
                v_price = v_estimated_price - (v_estimated_duration - v_duration) * v_price_per_day;
            ELSE
                v_price = v_estimated_price;
            END IF;

            UPDATE RENTAL
                SET
                    end_date = v_end_date,
                    price = v_price,
                    active = FALSE
                WHERE id = p_rent_id;
        END;
    $$;


ALTER PROCEDURE public.end_rent(IN p_rent_id integer) OWNER TO projekt;

--
-- Name: get_car_price(integer); Type: FUNCTION; Schema: public; Owner: projekt
--

CREATE FUNCTION public.get_car_price(car_id integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
        BEGIN
            RETURN (
                SELECT l.price
                    FROM price_list AS l
                    JOIN car AS c
                        ON l.model_name = c.model_name
                           AND l.brand_name = c.brand_name
                    WHERE c.id = car_id);
        END;
    $$;


ALTER FUNCTION public.get_car_price(car_id integer) OWNER TO projekt;

--
-- Name: set_car_rented(); Type: FUNCTION; Schema: public; Owner: projekt
--

CREATE FUNCTION public.set_car_rented() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            IF NEW.active = TRUE THEN
                IF (SELECT is_rented FROM CAR WHERE id = NEW.car_id) = TRUE THEN
                    RAISE EXCEPTION 'Car with id % is already rented.', NEW.car_id;
                ELSE
                    UPDATE CAR
                        SET is_rented = TRUE
                        WHERE id = NEW.car_id;
                END IF;
            ELSE
                UPDATE CAR
                    SET is_rented = FALSE
                    WHERE id = NEW.car_id;
            END IF;

            RETURN NEW;
        END;
    $$;


ALTER FUNCTION public.set_car_rented() OWNER TO projekt;

--
-- Name: set_invoice_element_price(); Type: FUNCTION; Schema: public; Owner: projekt
--

CREATE FUNCTION public.set_invoice_element_price() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Check if the rental is already recorded in another invoice
    IF (SELECT COUNT(*) FROM invoice_element WHERE rental_id = NEW.rental_id) > 0 THEN
        RAISE EXCEPTION 'Rental with id % is already recorded on another invoice', NEW.rental_id;
    END IF;

    -- Set the price and car_id from the RENTAL table
    SELECT price, car_id
    INTO NEW.price, NEW.car_id
    FROM RENTAL
    WHERE id = NEW.rental_id;

    RETURN NEW;
END;
$$;


ALTER FUNCTION public.set_invoice_element_price() OWNER TO projekt;

--
-- Name: set_invoice_price(); Type: FUNCTION; Schema: public; Owner: projekt
--

CREATE FUNCTION public.set_invoice_price() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        DECLARE
            new_price_sum NUMERIC;
            new_tax NUMERIC;
        BEGIN
            IF TG_OP = 'INSERT' THEN
            new_price_sum := (
                SELECT COALESCE(SUM(price), 0)
                    FROM INVOICE_ELEMENT
                    WHERE invoice_id = NEW.invoice_id
            );
        ELSIF TG_OP = 'DELETE' THEN
            new_price_sum := (
                SELECT COALESCE(SUM(price), 0)
                    FROM INVOICE_ELEMENT
                    WHERE invoice_id = OLD.invoice_id
            );
        END IF;
            new_tax := new_price_sum * 0.08;

            UPDATE INVOICE
                SET price_sum_netto = new_price_sum, tax = new_tax
                WHERE id = COALESCE(NEW.invoice_id, OLD.invoice_id);

            RETURN NEW;
        END;
    $$;


ALTER FUNCTION public.set_invoice_price() OWNER TO projekt;

--
-- Name: start_rent(integer, integer, date); Type: PROCEDURE; Schema: public; Owner: projekt
--

CREATE PROCEDURE public.start_rent(IN p_client_id integer, IN p_car_id integer, IN p_estimated_end_date date)
    LANGUAGE plpgsql
    AS $$
        DECLARE
            v_estimated_price NUMERIC;
            v_start_date DATE;
            v_duration INTEGER;
        BEGIN
            v_start_date := current_date;
            v_duration := p_estimated_end_date - v_start_date;
            IF v_duration < 1 THEN
                RAISE EXCEPTION 'Rent cannot be shorter than 1 day';
            END IF;

            v_estimated_price := v_duration * get_car_price(p_car_id);

            INSERT INTO RENTAL (start_date, end_date, price, car_id, client_id) VALUES
                (v_start_date, p_estimated_end_date, v_estimated_price, p_car_id, p_client_id);
        END;
    $$;


ALTER PROCEDURE public.start_rent(IN p_client_id integer, IN p_car_id integer, IN p_estimated_end_date date) OWNER TO projekt;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: brand; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.brand (
    name character varying(20) NOT NULL,
    logo bytea
);


ALTER TABLE public.brand OWNER TO projekt;

--
-- Name: car; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.car (
    id integer NOT NULL,
    model_name character varying(20) NOT NULL,
    brand_name character varying(20) NOT NULL,
    production_date date,
    mileage integer NOT NULL,
    license_plate character varying(9),
    vin character varying(17) NOT NULL,
    photo bytea,
    is_rented boolean DEFAULT false NOT NULL,
    segment_name character varying(20) NOT NULL
);


ALTER TABLE public.car OWNER TO projekt;

--
-- Name: car_id_seq; Type: SEQUENCE; Schema: public; Owner: projekt
--

CREATE SEQUENCE public.car_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.car_id_seq OWNER TO projekt;

--
-- Name: car_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: projekt
--

ALTER SEQUENCE public.car_id_seq OWNED BY public.car.id;


--
-- Name: client; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.client (
    id integer NOT NULL,
    address text NOT NULL
);


ALTER TABLE public.client OWNER TO projekt;

--
-- Name: client_id_seq; Type: SEQUENCE; Schema: public; Owner: projekt
--

CREATE SEQUENCE public.client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_id_seq OWNER TO projekt;

--
-- Name: client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: projekt
--

ALTER SEQUENCE public.client_id_seq OWNED BY public.client.id;


--
-- Name: company; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.company (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    nip character varying(20) NOT NULL
);


ALTER TABLE public.company OWNER TO projekt;

--
-- Name: company_id_seq; Type: SEQUENCE; Schema: public; Owner: projekt
--

CREATE SEQUENCE public.company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.company_id_seq OWNER TO projekt;

--
-- Name: company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: projekt
--

ALTER SEQUENCE public.company_id_seq OWNED BY public.company.id;


--
-- Name: invoice; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.invoice (
    id integer NOT NULL,
    client_id integer NOT NULL,
    date date NOT NULL,
    price_sum_netto numeric,
    tax numeric
);


ALTER TABLE public.invoice OWNER TO projekt;

--
-- Name: invoice_element; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.invoice_element (
    invoice_id integer NOT NULL,
    element_number integer NOT NULL,
    rental_id integer NOT NULL,
    car_id integer NOT NULL,
    price numeric NOT NULL
);


ALTER TABLE public.invoice_element OWNER TO projekt;

--
-- Name: invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: projekt
--

CREATE SEQUENCE public.invoice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invoice_id_seq OWNER TO projekt;

--
-- Name: invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: projekt
--

ALTER SEQUENCE public.invoice_id_seq OWNED BY public.invoice.id;


--
-- Name: model; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.model (
    model_name character varying(50) NOT NULL,
    brand_name character varying(20) NOT NULL,
    segment_name character varying(50) NOT NULL
);


ALTER TABLE public.model OWNER TO projekt;

--
-- Name: person; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.person (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    surname character varying(20) NOT NULL,
    pesel character varying(20) NOT NULL
);


ALTER TABLE public.person OWNER TO projekt;

--
-- Name: person_id_seq; Type: SEQUENCE; Schema: public; Owner: projekt
--

CREATE SEQUENCE public.person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.person_id_seq OWNER TO projekt;

--
-- Name: person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: projekt
--

ALTER SEQUENCE public.person_id_seq OWNED BY public.person.id;


--
-- Name: price_list; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.price_list (
    model_name character varying(20) NOT NULL,
    brand_name character varying(20) NOT NULL,
    price numeric NOT NULL
);


ALTER TABLE public.price_list OWNER TO projekt;

--
-- Name: rental; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.rental (
    id integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    price numeric NOT NULL,
    active boolean DEFAULT true NOT NULL,
    car_id integer NOT NULL,
    client_id integer NOT NULL
);


ALTER TABLE public.rental OWNER TO projekt;

--
-- Name: rental_id_seq; Type: SEQUENCE; Schema: public; Owner: projekt
--

CREATE SEQUENCE public.rental_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rental_id_seq OWNER TO projekt;

--
-- Name: rental_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: projekt
--

ALTER SEQUENCE public.rental_id_seq OWNED BY public.rental.id;


--
-- Name: segment; Type: TABLE; Schema: public; Owner: projekt
--

CREATE TABLE public.segment (
    name character varying(20) NOT NULL,
    description text
);


ALTER TABLE public.segment OWNER TO projekt;

--
-- Name: car id; Type: DEFAULT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.car ALTER COLUMN id SET DEFAULT nextval('public.car_id_seq'::regclass);


--
-- Name: client id; Type: DEFAULT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.client ALTER COLUMN id SET DEFAULT nextval('public.client_id_seq'::regclass);


--
-- Name: company id; Type: DEFAULT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.company ALTER COLUMN id SET DEFAULT nextval('public.company_id_seq'::regclass);


--
-- Name: invoice id; Type: DEFAULT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.invoice ALTER COLUMN id SET DEFAULT nextval('public.invoice_id_seq'::regclass);


--
-- Name: person id; Type: DEFAULT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.person ALTER COLUMN id SET DEFAULT nextval('public.person_id_seq'::regclass);


--
-- Name: rental id; Type: DEFAULT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.rental ALTER COLUMN id SET DEFAULT nextval('public.rental_id_seq'::regclass);


--
-- Data for Name: brand; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.brand VALUES ('Toyota', NULL);
INSERT INTO public.brand VALUES ('Ford', NULL);
INSERT INTO public.brand VALUES ('BMW', NULL);
INSERT INTO public.brand VALUES ('Volkswagen', NULL);
INSERT INTO public.brand VALUES ('Hyundai', NULL);
INSERT INTO public.brand VALUES ('Chrysler', NULL);
INSERT INTO public.brand VALUES ('Chevrolet', NULL);
INSERT INTO public.brand VALUES ('Genesis', NULL);
INSERT INTO public.brand VALUES ('Audi', NULL);
INSERT INTO public.brand VALUES ('Jeep', NULL);
INSERT INTO public.brand VALUES ('INFINITI', NULL);
INSERT INTO public.brand VALUES ('Honda', NULL);
INSERT INTO public.brand VALUES ('Acura', NULL);
INSERT INTO public.brand VALUES ('Buick', NULL);
INSERT INTO public.brand VALUES ('GMC', NULL);
INSERT INTO public.brand VALUES ('Dodge', NULL);
INSERT INTO public.brand VALUES ('Jaguar', NULL);
INSERT INTO public.brand VALUES ('Cadillac', NULL);


--
-- Data for Name: car; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.car VALUES (2, 'Corolla', 'Toyota', '2019-05-22', 30000, 'DEF5678', '1HGBH41JXMN109187', '\xefbbbf636f726f6c6c612e6a7067', true, 'Sedan');
INSERT INTO public.car VALUES (4, 'Focus', 'Ford', '2021-02-20', 10000, 'JKL3456', '1HGBH41JXMN109189', '\xefbbbf666f6375732e6a7067', true, 'Hatchback');
INSERT INTO public.car VALUES (3, 'Mustang', 'Ford', '2018-11-10', 25000, 'GHI9012', '1HGBH41JXMN109188', '\xefbbbf6d757374616e672e6a7067', true, 'Sedan');
INSERT INTO public.car VALUES (27, 'Passat', 'Volkswagen', '1999-12-15', 120000, 'K1 DIS', '1HGBH41JXMN109190', '\x7061737361742e6a7067', false, 'D-segment');
INSERT INTO public.car VALUES (5, 'X5', 'BMW', '2020-07-25', 20000, 'MNO7890', '1HGBH41JXMN109190', '\xefbbbf78352e6a7067', false, 'SUV');
INSERT INTO public.car VALUES (1, 'RAV4', 'Toyota', '2020-01-15', 15000, 'ABC1234', '1HGBH41JXMN109186', '\xefbbbf726176342e6a7067', true, 'SUV');
INSERT INTO public.car VALUES (16, 'RAV4', 'Toyota', '2022-01-01', 25000, 'DEF1235', '1HGBH41JXMN109651', '\xefbbbf726176342e6a7067', false, 'SUV');


--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.client VALUES (3, '289 Oak St, Capital City');
INSERT INTO public.client VALUES (1, '1223 Main St, Springfield');
INSERT INTO public.client VALUES (2, '5363 Elm St, Shelbyville');


--
-- Data for Name: company; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.company VALUES (3, 'Acme Corp', '5678901234');


--
-- Data for Name: invoice; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.invoice VALUES (12, 1, '2024-06-18', 32000, 2560.00);
INSERT INTO public.invoice VALUES (1, 1, '2023-01-11', 3000, 240);


--
-- Data for Name: invoice_element; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.invoice_element VALUES (12, 3, 31, 5, 20000);
INSERT INTO public.invoice_element VALUES (12, 4, 30, 16, 12000);
INSERT INTO public.invoice_element VALUES (1, 1, 1, 1, 3000);


--
-- Data for Name: model; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.model VALUES ('RAV4', 'Toyota', 'SUV');
INSERT INTO public.model VALUES ('Corolla', 'Toyota', 'Sedan');
INSERT INTO public.model VALUES ('Mustang', 'Ford', 'Sedan');
INSERT INTO public.model VALUES ('Focus', 'Ford', 'Hatchback');
INSERT INTO public.model VALUES ('X5', 'BMW', 'SUV');
INSERT INTO public.model VALUES ('Passat', 'Volkswagen', 'D-segment');
INSERT INTO public.model VALUES ('Q3', 'Audi', 'SUV');
INSERT INTO public.model VALUES ('Malibu', 'Chevrolet', 'Sedan');
INSERT INTO public.model VALUES ('Escalade ESV', 'Cadillac', 'SUV');
INSERT INTO public.model VALUES ('Corvette', 'Chevrolet', 'Coupe');
INSERT INTO public.model VALUES ('RLX', 'Acura', 'Sedan');
INSERT INTO public.model VALUES ('Silverado 2500 HD Crew Cab', 'Chevrolet', 'Pickup');
INSERT INTO public.model VALUES ('3 Series', 'BMW', 'Sedan');
INSERT INTO public.model VALUES ('Pacifica', 'Chrysler', 'Van/Minivan');
INSERT INTO public.model VALUES ('Colorado Crew Cab', 'Chevrolet', 'Pickup');
INSERT INTO public.model VALUES ('X3', 'BMW', 'SUV');
INSERT INTO public.model VALUES ('TLX', 'Acura', 'Sedan');
INSERT INTO public.model VALUES ('Silverado 3500 HD Crew Cab', 'Chevrolet', 'Pickup');
INSERT INTO public.model VALUES ('7 Series', 'BMW', 'Sedan');
INSERT INTO public.model VALUES ('Fusion', 'Ford', 'Sedan');
INSERT INTO public.model VALUES ('Envision', 'Buick', 'SUV');
INSERT INTO public.model VALUES ('SQ5', 'Audi', 'SUV');
INSERT INTO public.model VALUES ('R8', 'Audi', 'Coupe');
INSERT INTO public.model VALUES ('Traverse', 'Chevrolet', 'SUV');
INSERT INTO public.model VALUES ('MDX', 'Acura', 'SUV');
INSERT INTO public.model VALUES ('QX80', 'INFINITI', 'SUV');
INSERT INTO public.model VALUES ('Encore', 'Buick', 'SUV');
INSERT INTO public.model VALUES ('Sierra 2500 HD Crew Cab', 'GMC', 'Pickup');
INSERT INTO public.model VALUES ('Insight', 'Honda', 'Sedan');
INSERT INTO public.model VALUES ('XT6', 'Cadillac', 'SUV');
INSERT INTO public.model VALUES ('XT5', 'Cadillac', 'SUV');
INSERT INTO public.model VALUES ('XT4', 'Cadillac', 'SUV');
INSERT INTO public.model VALUES ('Enclave', 'Buick', 'SUV');
INSERT INTO public.model VALUES ('Q5', 'Audi', 'SUV');
INSERT INTO public.model VALUES ('Santa Fe', 'Hyundai', 'SUV');
INSERT INTO public.model VALUES ('EcoSport', 'Ford', 'SUV');
INSERT INTO public.model VALUES ('Escape', 'Ford', 'SUV');
INSERT INTO public.model VALUES ('Sonata', 'Hyundai', 'Sedan');
INSERT INTO public.model VALUES ('Edge', 'Ford', 'SUV');
INSERT INTO public.model VALUES ('Camaro', 'Chevrolet', 'Convertible');
INSERT INTO public.model VALUES ('Kona Electric', 'Hyundai', 'SUV');
INSERT INTO public.model VALUES ('Equinox', 'Chevrolet', 'SUV');
INSERT INTO public.model VALUES ('Sierra 3500 HD Crew Cab', 'GMC', 'Pickup');
INSERT INTO public.model VALUES ('Gladiator', 'Jeep', 'Pickup');
INSERT INTO public.model VALUES ('X7', 'BMW', 'SUV');
INSERT INTO public.model VALUES ('CT6-V', 'Cadillac', 'Sedan');
INSERT INTO public.model VALUES ('A7', 'Audi', 'Sedan');
INSERT INTO public.model VALUES ('Blazer', 'Chevrolet', 'SUV');
INSERT INTO public.model VALUES ('F150 SuperCrew Cab', 'Ford', 'Pickup');
INSERT INTO public.model VALUES ('Suburban', 'Chevrolet', 'SUV');
INSERT INTO public.model VALUES ('Civic', 'Honda', 'Hatchback');
INSERT INTO public.model VALUES ('Compass', 'Jeep', 'SUV');
INSERT INTO public.model VALUES ('Escalade', 'Cadillac', 'SUV');
INSERT INTO public.model VALUES ('Voyager', 'Chrysler', 'Van/Minivan');
INSERT INTO public.model VALUES ('Accord Hybrid', 'Honda', 'Sedan');
INSERT INTO public.model VALUES ('Terrain', 'GMC', 'SUV');
INSERT INTO public.model VALUES ('Spark', 'Chevrolet', 'Hatchback');
INSERT INTO public.model VALUES ('Sierra 1500 Crew Cab', 'GMC', 'Pickup');
INSERT INTO public.model VALUES ('NEXO', 'Hyundai', 'SUV');
INSERT INTO public.model VALUES ('Veloster', 'Hyundai', 'Coupe');
INSERT INTO public.model VALUES ('Silverado 1500 Crew Cab', 'Chevrolet', 'Pickup');
INSERT INTO public.model VALUES ('G70', 'Genesis', 'Sedan');
INSERT INTO public.model VALUES ('CT5', 'Cadillac', 'Sedan');
INSERT INTO public.model VALUES ('Odyssey', 'Honda', 'Van/Minivan');
INSERT INTO public.model VALUES ('Elantra GT', 'Hyundai', 'Hatchback');
INSERT INTO public.model VALUES ('RDX', 'Acura', 'SUV');
INSERT INTO public.model VALUES ('Yukon XL', 'GMC', 'SUV');
INSERT INTO public.model VALUES ('Ranger SuperCab', 'Ford', 'Pickup');
INSERT INTO public.model VALUES ('Expedition MAX', 'Ford', 'SUV');
INSERT INTO public.model VALUES ('Kona', 'Hyundai', 'SUV');
INSERT INTO public.model VALUES ('QX50', 'INFINITI', 'SUV');
INSERT INTO public.model VALUES ('Durango', 'Dodge', 'SUV');
INSERT INTO public.model VALUES ('Yukon', 'GMC', 'SUV');
INSERT INTO public.model VALUES ('Palisade', 'Hyundai', 'SUV');
INSERT INTO public.model VALUES ('Ridgeline', 'Honda', 'Pickup');
INSERT INTO public.model VALUES ('Cherokee', 'Jeep', 'SUV');
INSERT INTO public.model VALUES ('Bolt EV', 'Chevrolet', 'Hatchback');
INSERT INTO public.model VALUES ('Expedition', 'Ford', 'SUV');
INSERT INTO public.model VALUES ('Elantra', 'Hyundai', 'Sedan');
INSERT INTO public.model VALUES ('Passport', 'Honda', 'SUV');
INSERT INTO public.model VALUES ('Charger', 'Dodge', 'Sedan');
INSERT INTO public.model VALUES ('Accord', 'Honda', 'Sedan');
INSERT INTO public.model VALUES ('QX60', 'INFINITI', 'SUV');
INSERT INTO public.model VALUES ('Venue', 'Hyundai', 'SUV');
INSERT INTO public.model VALUES ('Pilot', 'Honda', 'SUV');
INSERT INTO public.model VALUES ('Grand Cherokee', 'Jeep', 'SUV');
INSERT INTO public.model VALUES ('Tahoe', 'Chevrolet', 'SUV');
INSERT INTO public.model VALUES ('Acadia', 'GMC', 'SUV');
INSERT INTO public.model VALUES ('Impala', 'Chevrolet', 'Sedan');
INSERT INTO public.model VALUES ('CR-V', 'Honda', 'SUV');
INSERT INTO public.model VALUES ('Q60', 'INFINITI', 'Coupe');
INSERT INTO public.model VALUES ('Ranger SuperCrew', 'Ford', 'Pickup');
INSERT INTO public.model VALUES ('Trax', 'Chevrolet', 'SUV');
INSERT INTO public.model VALUES ('Ioniq Plug-in Hybrid', 'Hyundai', 'Hatchback');
INSERT INTO public.model VALUES ('E-PACE', 'Jaguar', 'SUV');
INSERT INTO public.model VALUES ('Tucson', 'Hyundai', 'SUV');
INSERT INTO public.model VALUES ('Explorer', 'Ford', 'SUV');
INSERT INTO public.model VALUES ('HR-V', 'Honda', 'SUV');
INSERT INTO public.model VALUES ('I-PACE', 'Jaguar', 'SUV');
INSERT INTO public.model VALUES ('Q50', 'INFINITI', 'Sedan');
INSERT INTO public.model VALUES ('G80', 'Genesis', 'Sedan');
INSERT INTO public.model VALUES ('F-PACE', 'Jaguar', 'SUV');
INSERT INTO public.model VALUES ('Renegade', 'Jeep', 'SUV');
INSERT INTO public.model VALUES ('Accent', 'Hyundai', 'Sedan');


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.person VALUES (1, 'John', 'Doe', '12345678901');
INSERT INTO public.person VALUES (2, 'Jane', 'Smith', '23456789012');


--
-- Data for Name: price_list; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.price_list VALUES ('Mustang', 'Ford', 4000);
INSERT INTO public.price_list VALUES ('X5', 'BMW', 5000);
INSERT INTO public.price_list VALUES ('Passat', 'Volkswagen', 500);
INSERT INTO public.price_list VALUES ('Focus', 'Ford', 3800.0);
INSERT INTO public.price_list VALUES ('Corolla', 'Toyota', 2500.0);
INSERT INTO public.price_list VALUES ('RAV4', 'Toyota', 3000.0);


--
-- Data for Name: rental; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.rental VALUES (31, '2024-06-14', '2024-06-18', 20000, false, 5, 1);
INSERT INTO public.rental VALUES (30, '2024-06-14', '2024-06-18', 12000, false, 16, 1);
INSERT INTO public.rental VALUES (36, '2024-06-18', '2024-06-21', 9000, true, 1, 1);
INSERT INTO public.rental VALUES (3, '2023-03-01', '2023-03-10', 36000, true, 3, 3);
INSERT INTO public.rental VALUES (2, '2023-02-01', '2023-02-15', 35000, true, 2, 2);
INSERT INTO public.rental VALUES (1, '2023-01-01', '2023-01-02', 3000, false, 1, 1);
INSERT INTO public.rental VALUES (35, '2024-06-18', '2024-06-23', 19000, true, 4, 1);


--
-- Data for Name: segment; Type: TABLE DATA; Schema: public; Owner: projekt
--

INSERT INTO public.segment VALUES ('SUV', 'Sport Utility Vehicle');
INSERT INTO public.segment VALUES ('Sedan', 'Passenger car in a three-box configuration');
INSERT INTO public.segment VALUES ('Hatchback', 'Passenger car with a hatch-type rear door');
INSERT INTO public.segment VALUES ('D-segment', ' European segments for passenger cars');
INSERT INTO public.segment VALUES ('Convertible', NULL);
INSERT INTO public.segment VALUES ('Van/Minivan', NULL);
INSERT INTO public.segment VALUES ('Coupe', NULL);
INSERT INTO public.segment VALUES ('Pickup', NULL);


--
-- Name: car_id_seq; Type: SEQUENCE SET; Schema: public; Owner: projekt
--

SELECT pg_catalog.setval('public.car_id_seq', 27, true);


--
-- Name: client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: projekt
--

SELECT pg_catalog.setval('public.client_id_seq', 14, true);


--
-- Name: company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: projekt
--

SELECT pg_catalog.setval('public.company_id_seq', 1, false);


--
-- Name: invoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: projekt
--

SELECT pg_catalog.setval('public.invoice_id_seq', 12, true);


--
-- Name: person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: projekt
--

SELECT pg_catalog.setval('public.person_id_seq', 1, false);


--
-- Name: rental_id_seq; Type: SEQUENCE SET; Schema: public; Owner: projekt
--

SELECT pg_catalog.setval('public.rental_id_seq', 36, true);


--
-- Name: brand brand_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.brand
    ADD CONSTRAINT brand_pkey PRIMARY KEY (name);


--
-- Name: car car_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT car_pkey PRIMARY KEY (id);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (id);


--
-- Name: invoice_element invoice_element_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.invoice_element
    ADD CONSTRAINT invoice_element_pkey PRIMARY KEY (invoice_id, element_number);


--
-- Name: invoice invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (id);


--
-- Name: model model_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.model
    ADD CONSTRAINT model_pkey PRIMARY KEY (model_name, brand_name);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- Name: price_list price_list_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.price_list
    ADD CONSTRAINT price_list_pkey PRIMARY KEY (model_name, brand_name);


--
-- Name: rental rental_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.rental
    ADD CONSTRAINT rental_pkey PRIMARY KEY (id);


--
-- Name: segment segment_pkey; Type: CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.segment
    ADD CONSTRAINT segment_pkey PRIMARY KEY (name);


--
-- Name: rental car_rented_trigger; Type: TRIGGER; Schema: public; Owner: projekt
--

CREATE TRIGGER car_rented_trigger AFTER INSERT ON public.rental FOR EACH ROW EXECUTE FUNCTION public.set_car_rented();


--
-- Name: rental check_rental_updates; Type: TRIGGER; Schema: public; Owner: projekt
--

CREATE TRIGGER check_rental_updates BEFORE UPDATE OF active ON public.rental FOR EACH ROW EXECUTE FUNCTION public.disallow_rental_reactivation();


--
-- Name: invoice_element invoice_price_trigger_on_delete; Type: TRIGGER; Schema: public; Owner: projekt
--

CREATE TRIGGER invoice_price_trigger_on_delete AFTER DELETE ON public.invoice_element FOR EACH ROW EXECUTE FUNCTION public.set_invoice_price();


--
-- Name: invoice_element invoice_price_trigger_on_insert; Type: TRIGGER; Schema: public; Owner: projekt
--

CREATE TRIGGER invoice_price_trigger_on_insert BEFORE INSERT ON public.invoice_element FOR EACH ROW EXECUTE FUNCTION public.set_invoice_element_price();


--
-- Name: rental update_car_rented_trigger; Type: TRIGGER; Schema: public; Owner: projekt
--

CREATE TRIGGER update_car_rented_trigger AFTER UPDATE OF active ON public.rental FOR EACH ROW EXECUTE FUNCTION public.set_car_rented();


--
-- Name: car car_model_name_brand_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT car_model_name_brand_name_fkey FOREIGN KEY (model_name, brand_name) REFERENCES public.model(model_name, brand_name);


--
-- Name: car car_segment_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.car
    ADD CONSTRAINT car_segment_name_fkey FOREIGN KEY (segment_name) REFERENCES public.segment(name);


--
-- Name: company company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_id_fkey FOREIGN KEY (id) REFERENCES public.client(id) ON DELETE CASCADE;


--
-- Name: invoice invoice_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.invoice
    ADD CONSTRAINT invoice_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: invoice_element invoice_element_car_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.invoice_element
    ADD CONSTRAINT invoice_element_car_id_fkey FOREIGN KEY (car_id) REFERENCES public.car(id);


--
-- Name: invoice_element invoice_element_invoice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.invoice_element
    ADD CONSTRAINT invoice_element_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES public.invoice(id);


--
-- Name: invoice_element invoice_element_rental_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.invoice_element
    ADD CONSTRAINT invoice_element_rental_id_fkey FOREIGN KEY (rental_id) REFERENCES public.rental(id);


--
-- Name: model model_brand_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.model
    ADD CONSTRAINT model_brand_name_fkey FOREIGN KEY (brand_name) REFERENCES public.brand(name);


--
-- Name: model model_segment_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.model
    ADD CONSTRAINT model_segment_name_fkey FOREIGN KEY (segment_name) REFERENCES public.segment(name);


--
-- Name: person person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_id_fkey FOREIGN KEY (id) REFERENCES public.client(id) ON DELETE CASCADE;


--
-- Name: price_list price_list_model_name_brand_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.price_list
    ADD CONSTRAINT price_list_model_name_brand_name_fkey FOREIGN KEY (model_name, brand_name) REFERENCES public.model(model_name, brand_name);


--
-- Name: rental rental_car_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.rental
    ADD CONSTRAINT rental_car_id_fkey FOREIGN KEY (car_id) REFERENCES public.car(id);


--
-- Name: rental rental_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: projekt
--

ALTER TABLE ONLY public.rental
    ADD CONSTRAINT rental_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- PostgreSQL database dump complete
--

