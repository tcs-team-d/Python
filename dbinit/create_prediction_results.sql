CREATE TABLE prediction_results (
    id SERIAL PRIMARY KEY,
    prediction_date DATE NOT NULL,
    beer_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    FOREIGN KEY (beer_id) REFERENCES beers(beer_id)
);
