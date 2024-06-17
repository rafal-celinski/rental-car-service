-- Trigger zabraniający ponownej aktywacji oraz deaktywacji nieaktywnego wypożyczenia
CREATE OR REPLACE FUNCTION disallow_rental_reactivation()
    RETURNS TRIGGER AS $$
        BEGIN
           IF NEW.active = TRUE THEN
               RAISE EXCEPTION 'Cannot reactivate rental';
           ELSIF NEW.ACTIVE = FALSE AND NEW.active = OLD.active THEN
               RAISE EXCEPTION 'Rental with id % is already not active', NEW.id;
           END IF;
        END;
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_rental_updates
    BEFORE UPDATE OF active ON RENTAL
    FOR EACH ROW
    EXECUTE FUNCTION disallow_rental_reactivation();

-- Trigger, który w momencie dodania lub aktualizacji rekordu do tabeli ‘Rental’ zmienia stan samochodu w tabeli ‘Car’
CREATE OR REPLACE FUNCTION set_car_rented()
    RETURNS TRIGGER AS $$
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
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER car_rented_trigger
    AFTER INSERT ON RENTAL
    FOR EACH ROW
    EXECUTE FUNCTION set_car_rented();

CREATE OR REPLACE TRIGGER update_car_rented_trigger
    AFTER UPDATE OF active ON RENTAL
    FOR EACH ROW
    EXECUTE FUNCTION set_car_rented();

-- Trigger, który przy dodawaniu rekordu w ‘Invoice Element’ sam przepisze cenę oraz car_id z tabeli ‘Rental’
CREATE OR REPLACE FUNCTION set_invoice_element_price()
    RETURNS TRIGGER AS $$
        BEGIN
            IF (select count(*) from invoice_element where rental_id = 1) > 0 THEN
                RAISE EXCEPTION 'Rental with id % is already recorded on the other invoice', NEW.rental_id;
            END IF;

            SELECT price, car_id
                INTO NEW.price, NEW.car_id
                FROM RENTAL
                WHERE id = NEW.rental_id;
            RETURN NEW;
        END;
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER invoice_element_price_trigger
    BEFORE INSERT ON invoice_element
    FOR EACH ROW
    EXECUTE FUNCTION set_invoice_element_price();

-- Trigger, który przy każdym dodaniu i usunięciu ‘Invoice Element’ zaktualizuje ‘price_sum_netto’ oraz ’tax’ w tabeli ‘Invoice’
CREATE OR REPLACE FUNCTION set_invoice_price()
    RETURNS TRIGGER AS $$
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
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER invoice_price_trigger_on_insert
    AFTER INSERT ON INVOICE_ELEMENT
    FOR EACH ROW
    EXECUTE FUNCTION set_invoice_price();

CREATE OR REPLACE TRIGGER invoice_price_trigger_on_delete
    AFTER DELETE ON INVOICE_ELEMENT
    FOR EACH ROW
    EXECUTE FUNCTION set_invoice_price();

-- Procedura generująca faktury.
create procedure create_invoice(IN p_client_id integer, IN p_start_date date, IN p_end_date date)
    language plpgsql
as
$$
DECLARE
    v_rental_id INTEGER;
    v_rental_price NUMERIC;
    v_element_num INTEGER;
    v_invoice_id INTEGER;
    v_total_price NUMERIC := 0;
    v_car_id INTEGER;
BEGIN
    v_element_num := 1;

    FOR v_rental_id, v_rental_price IN
        (SELECT id, price
         FROM RENTAL
         WHERE active = FALSE
           AND client_id = p_client_id
           AND end_date BETWEEN p_start_date AND p_end_date)
        LOOP
            v_total_price := v_total_price + v_rental_price;
        END LOOP;

    IF v_total_price <= 0 THEN
        RAISE EXCEPTION 'Total price for invoice must be greater than zero. Total price: %', v_total_price;
    END IF;

    INSERT INTO INVOICE (client_id, date, price_sum_netto, tax)
    VALUES (p_client_id, CURRENT_DATE, v_total_price, v_total_price * 0.08)
    RETURNING id INTO v_invoice_id;

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
    $$ LANGUAGE plpgsql;


-- Procedury które obsługują wypożycznia i zwroty.
CREATE OR REPLACE FUNCTION get_car_price(car_id INTEGER)
    RETURNS INTEGER
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
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE start_rent(p_client_id INTEGER, p_car_id INTEGER, p_estimated_end_date DATE)
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
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE end_rent(p_rent_id INTEGER)
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
    $$ LANGUAGE plpgsql
