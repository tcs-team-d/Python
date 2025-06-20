CREATE TABLE sale_records (
    id SERIAL PRIMARY KEY,
    sale_date DATE NOT NULL,
    beer_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    total_sales INT,
    comment VARCHAR(255),
    FOREIGN KEY (beer_id) REFERENCES beers(beer_id)
);