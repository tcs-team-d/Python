CREATE TABLE beers (
    beer_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    unit_price INT NOT NULL CHECK (unit_price > 0)
);

