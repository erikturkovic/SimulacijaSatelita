CREATE TABLE satellites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,  
    x FLOAT NOT NULL,           
    y FLOAT NOT NULL,           
    z FLOAT NOT NULL,           
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE satellites
ADD COLUMN orbital_period FLOAT NOT NULL DEFAULT 5400;


SELECT * FROM satellites

INSERT INTO satellites (name, x, y, z)
VALUES (
    'LEO',
    6771,  -- 6371 km (Earth radius) + 400 km (orbit altitude)
    0,
    0
);

UPDATE satellites
SET orbital_period = 5400 
WHERE id = 1;  